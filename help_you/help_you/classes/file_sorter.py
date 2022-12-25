"""
    TODO: logging

    USAGE:
        class Filter(
                destiantion:    -   string,
                extensions:     -   "space separated string" | [list of strings],
                functions:      -   "space separated string" | [list of strings]
            )
        class Task(
            path:   - Path to sort
        )
        For example see function main()

        All excpetions store in Task's deque attribute - _status
        In threaded mode no exception raised, except in construction methods
"""


from copy import deepcopy
from queue import Queue
from pathlib import Path

import os
import shutil
import threading



class Filter:

    translation = None
    
    @classmethod
    def _make_translation(cls) -> dict:
        """Create translation table from cyrillic to latin. Also replace all other character with symbol - '_' except digits"""
        translation_table = {}
        latin = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

        # Make cyrillic tuplet
        cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        cyrillic_list = []
        for c in cyrillic_symbols:
            cyrillic_list.append(c)

        cyrillic = tuple(cyrillic_list)

        # Fill tranlation table
        for c, l in zip(cyrillic, latin):
            translation_table[ord(c)] = l
            translation_table[ord(c.upper())] = l.upper()

        # From symbol [NULL] to '/'. See ASCI table for more details.
        for i in range(0, 48):
            translation_table[i] = '_'
        # From ':' to '@'. See ASCI table for more details.
        for i in range(58, 65):
            translation_table[i] = '_'
        # From symbol '[' to '`'. See ASCI table for more details.
        for i in range(91, 97):
            translation_table[i] = '_'
        # From symbol '{' to [DEL]. See ASCI table for more details.
        for i in range(123, 128):
            translation_table[i] = '_'
        return translation_table


    def __init__(self, destination: Path, extensions, functions, normalize = True, overwrite= True):

        self.path           = None          #   Root directory. Sets with adding Filter to Task.
        self.destination    = destination   #   Destination directory.
        self.normalize      = normalize     #   Normalize files' names.
        self.overwrite      = overwrite     #   Overwrite files in destination directory.
        self._functions      = []           #   List of functions' objects.

        if isinstance(extensions, str):
            self.extensions = extensions.lower().split()
        else:
            self.extensions = list(map(lambda x: x.lower(),extensions))
        
        if isinstance(functions, str):
            self.functions = functions.lower().split()
        else:
            self.functions = list(map(lambda x: x.lower(),functions))

        #   Fill list with function objects.
        for name in self.functions:
            function = getattr(self, "_" + name)
            self._functions.append(function)


    def __call__(self,name: Path):
        """Call all functions in list."""
        for function in self._functions:
            try:
                result = function(name)
                yield result
            except Exception as e:
                yield e
        return self

    def _make_destination(self, name: Path, split = True) -> Path:
        """Create destination path with normalization, if normalization is on."""
        file_name   = name.stem
        file_ext    = ''
        if split:
            file_ext    = name.suffix
        
        if self.normalize:
            file_name = file_name.translate(Filter.translation)
        
        file_name += file_ext

        destination  = Path(self.path) / self.destination
        if not destination.exists():
            destination.mkdir()
        return  destination / file_name


    def _copy(self, name: Path) -> Path:
        destination = self._make_destination(name)

        if self.overwrite or not destination.exists():
            shutil.copy2(name, destination)
            return destination
        return None
    

    def _remove(self, name: Path) -> Path:
        if name.exists():
            name.unlink(True)
            return name
        return None


    def _remove_checked(self, name: Path) -> Path:
        """Remove archive if it is unpacked."""
        destination = self._make_destination(name, False)
        if destination.exists():
            name.unlink()
            return name
        
        return None


    def _move(self, name: Path) -> Path:
        destination = self._make_destination(name)

        if self.overwrite or not destination.exists():
            shutil.move(name, destination)
            return destination
        return None


    def _unpack(self, name: Path) -> Path:
        destination = self._make_destination(name, False)
        if not destination.exists():
            destination.mkdir()
        
        if self.overwrite or not any(destination.iterdir()):
            try:
                shutil.unpack_archive(name, destination)
                return destination
            except Exception as e: #shutil.ReadError as e:
                destination.rmdir()
                raise
        return None

Filter.translation = Filter._make_translation()


class Task(threading.Thread):

    def __init__(self, path: Path, filter: Filter = None, keep_empty_dir = False):
        threading.Thread.__init__(self)
        self._status = Queue()
        
        self.keep_empty_dir = keep_empty_dir
        if isinstance(path, str):
            if not len(path):
                path = Path().cwd()
            else:
                path = Path(path)
        if path.exists():
            self.path    = path
        else:
            raise FileExistsError(f"Path: '{path}' doesn't exists.")
        
        self._filters       = {}    #   Destination path to Filter mapping ex. {"archives": Filter()}.
        self._ext2filter    = {}    #   File extension to Filter mapping ex. {"zip": Filter()}.
        if filter:
            self._filters[filter.destination] = filter
            filter.path = self.path
            for ext in filter.extensions:
                self._ext2filter[ext] = filter
    

    @property
    def filters(self):
        filters = deepcopy(self._filters)
        for f in filters.values():
            f.path = None
        return filters


    @filters.setter
    def filters(self,filters: list):
        self._filters = deepcopy(filters)
        self._ext2filter = {}
        for filter in self._filters.values():
            filter.path = self.path
            for ext in filter.extensions:
                self._ext2filter[ext] = filter


    def __iadd__(self, filter: Filter):
        """Add filter to task."""
        self._filters[filter.destination] = filter
        filter.path = self.path
        for ext in filter.extensions:
            self._ext2filter[ext] = filter
        return self


    def __isub__(self, filter: Filter):
        """Remove filter from task."""
        filter.path = None
        self._filters.pop(filter.destination)
        for ext in filter.extensions:
            self._ext2filter.pop(ext)
        return self


    def sort(self, path = None):

        if not path:
            path = self.path

        for pathname in path.iterdir():
            try:
                if pathname.is_dir():
                    if pathname.name in self._filters:  # Exclude destination directories.
                        continue
                    self.sort(pathname)
                    if not self.keep_empty_dir and pathname.exists() and not any(pathname.iterdir()):
                        pathname.rmdir()
                elif pathname.is_file():
                    ext = pathname.suffix.replace('.', '').lower()
                    if len(self._ext2filter) == 1 and '*' in self._ext2filter:
                        filter_ = self._ext2filter['*']
                    elif not ext in self._ext2filter and "other" in self._filters:  #   If file extesions not found in filters' list and present Filter("other")
                        filter_ = self._filters["other"]
                    else:
                        filter_ = self._ext2filter[ext]
                    if filter_:
                        generator = filter_(pathname)    #   Call filter.
                        while True:
                            try:
                                result = next(generator)
                                if isinstance(result, Exception):
                                    self._status.put(result)#, block=False)
                                    continue
                            except StopIteration:
                                break

            except Exception as e:
                self._status.put(e)#,block= False)
                continue
        else:  # ignore all other filesystem entities.
            pass
        if  not self._status.empty() \
            and threading.current_thread() == threading.main_thread() \
            and path == self.path:

            raise Exception(self._status)

    def run(self):
        try:    #   Catch all exception in thread
            self.sort()
        except Exception as e:
            self._status.put(e)#,block= False)


class FileSorter:

    def __init__(self, task: Task = None):
        self._status = []
        self.tasks = {}
        if task:
            self.tasks[task.path] = task

    def __iadd__(self, task: Task):
        self.tasks[task.path] = task
        return self

    def __isub__(self, task: Task):
        self.tasks.pop(task.path)
        return self

    def start(self):
        for task in self.tasks.values():
            task.start()

    def sort(self):
        for task in self.tasks.values():
            try:    #   Catch all exception in thread
                task.sort()
            except Exception as e:
                exceptions = e.args[0]
                exception = exceptions.get_nowait()
                while exception and not exceptions.empty():
                    self._status.append(str(task.path) + " : " + str(exception))
                    exception = exceptions.get_nowait()
                continue
        if len(self._status):
            raise Exception(self._status)


def sort_targets(path_to_target,threaded = False):
    sorter = FileSorter()

    if isinstance(path_to_target, str):
        pathes = path_to_target.split()
    elif isinstance(path_to_target, list):
        pathes = path_to_target
    else:
        raise ValueError(f"{path} value error.")
    for path in pathes:
        task = Task(path)
        task += Filter("archives",  ["zip", "tar", "tgz", "gz", "7zip", "7z", "iso", "rar"] ,                           ["UNPACK", "REMOVE_checked"])
        task += Filter("audios",    ["wav", "mp3", "ogg", "amr"],                                                       ["move"])
        task += Filter("images",    ["jpeg", "png", "jpg", "svg"],                                                      ["move"])
        task += Filter("videos",    ["avi", "mp4", "mov", "mkv"],                                                       ["move"])
        task += Filter("documents", ["doc", "docx", "txt", "pdf", "xls", "xlsx", "ppt", "pptx", "rtf", "xml", "ini"],   ["move"])
        task += Filter("softwares", ["exe", "msi", "bat", "dll"],                                                       ["move"])
        task += Filter("other",     [""],                                                                               ["move"])

        sorter += task

    if threaded:
        sorter.start()  #   Start tasks as separated threads. All exceptions store in Task's _status(Queue()) attribute
        
    else:
        try:
            sorter.sort()   #   Start tasks in main thread.
        except Exception as e:
            exceptions = e.args[0]
            for exception in exceptions:
                print(exception)

    # try:
    #     task2 = Task("D:/edu/test1")#, Filter("sources", "py", "copy"))
    #     task2.filters = task.filters
    #     sorter += task2
    # except Exception as e:
    #     pass

if __name__ == "__main__":
    sort_targets("D:/edu/test D:/edu/test1")
