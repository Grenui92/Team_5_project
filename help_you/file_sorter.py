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

import shutil
import threading
from copy import deepcopy
from pathlib import Path
from queue import Queue


class Filter:

    @staticmethod
    def make_translation() -> dict:
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

    def __init__(self, destination: Path, extensions, functions, normalize=True, overwrite=True):

        self.path = None  # Root directory. Sets with adding Filter to Task.
        self.destination = destination  # Destination directory.
        self.normalize = normalize  # Normalize files' names.
        self.overwrite = overwrite  # Overwrite files in destination directory.
        self._functions = []  # List of functions' objects.

        if isinstance(extensions, str):
            self.extensions = extensions.lower().split()
        else:
            self.extensions = list(map(lambda x: x.lower(), extensions))

        if isinstance(functions, str):
            self.functions = functions.lower().split()
        else:
            self.functions = list(map(lambda x: x.lower(), functions))

        #   Fill list with function objects.
        for name in self.functions:
            function = getattr(self, "_" + name)
            self._functions.append(function)

    def __call__(self, name: Path):
        """Call all functions in list."""
        for function in self._functions:
            try:
                result = function(name)
                yield result
            except Exception as e:
                yield e
        return self

    def _make_destination(self, name: Path, split=True) -> Path:
        """Create destination path with normalization, if normalization is on."""
        file_name = name.stem
        file_ext = ''
        if split:
            file_ext = name.suffix

        if self.normalize:
            file_name = file_name.translate(Filter._translation)

        file_name += file_ext

        destination = Path(self.path) / self.destination
        if not destination.exists():
            destination.mkdir()
        return destination / file_name

    def _copy(self, name: Path) -> Path:
        destination = self._make_destination(name)

        if self.overwrite or not destination.exists():
            shutil.copy2(name, destination)
            return destination

    def _remove(self, name: Path) -> Path:
        if name.exists():
            name.unlink(True)
            return name

    def _remove_checked(self, name: Path) -> Path:
        """Remove archive if it is unpacked."""
        destination = self._make_destination(name, False)
        if destination.exists():
            name.unlink()
            return name

    def _move(self, name: Path) -> Path:
        destination = self._make_destination(name)

        if self.overwrite or not destination.exists():
            shutil.move(name, destination)
            return destination

    def _unpack(self, name: Path) -> Path:
        destination = self._make_destination(name, False)
        if not destination.exists():
            destination.mkdir()

        if self.overwrite or not any(destination.iterdir()):
            try:
                shutil.unpack_archive(name, destination)
                return destination
            except Exception as e:  # shutil.ReadError as e:
                destination.rmdir()
                raise

    _translation = make_translation()


class Task(threading.Thread):

    def __init__(self, path, filter: Filter = None, keep_empty_dir=False):
        threading.Thread.__init__(self)
        self._status = Queue()

        self.keep_empty_dir = keep_empty_dir
        if isinstance(path, str):
            if not len(path):
                path = Path().cwd()
            else:
                path = Path(path)
        if path.exists():
            self.path = path
        else:  # Before running protection
            raise FileExistsError(f"Path: '{path}' doesn't exists.")

        self._filters = {}  # Destination path to Filter mapping ex. {"archives": Filter()}.
        self._ext2filter = {}  # File extension to Filter mapping ex. {"zip": Filter()}.
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
    def filters(self, filters: list):
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

    def _file_processing(self, pathname):

        ext = pathname.suffix.replace('.', '').lower()  # Get file extesion
        #   Find filter by extension
        if len(self._ext2filter) == 1 and '*' in self._ext2filter:
            filter_ = self._ext2filter['*']
        elif not ext in self._ext2filter and "other" in self._filters:  # If file extesions not found in filters' list and present Filter("other")
            filter_ = self._filters["other"]
        else:
            filter_ = self._ext2filter[ext]

        if filter_:  # Filter found
            generator = filter_(pathname)  # Call every filter.
            while True:
                try:
                    result = next(generator)  # Call filter and then check for return value
                    if isinstance(result, Exception):
                        self._status.put(result)  # Store all exceptions for filter functions' call
                        continue
                except StopIteration:
                    break

    #   Store exceptiona from imported modules
    #   As I can't garanty that filsystem can't be modified between 'os' module calls.
    #   I'm catch and store all its excetions.
    def sort(self, path=None):

        if not path:  # for root level, may be used without path parameter
            path = self.path

        #   Get dir entity type
        try:
            is_dir = path.is_dir()
            is_file = path.is_file()
        except Exception as e:
            self._status.put(e)

        if is_file:
            self._file_processing(path)
        elif is_dir:
            for path in path.iterdir():
                #   Get dir entity type
                try:
                    is_dir = path.is_dir()
                    is_file = path.is_file()
                except Exception as e:
                    self._status.put(e)

                if is_dir:
                    #   Exclude destination directories aka [archives, videos, audios nad etc. destination dirs].
                    if path.name in self._filters:
                        continue

                    self.sort(path)  # Going to recusion

                    #   Remove empty dirs
                    if not self.keep_empty_dir and path.exists() and not any(path.iterdir()):
                        try:
                            path.rmdir()
                        except Exception as e:
                            self._status.put(e)

                elif is_file:  # Processing files
                    self._file_processing(path)
                else:
                    continue

        # If exceptions is been and execution is in Main Thread, raise it all as Quequ object
        if not self._status.empty() \
                and threading.current_thread() == threading.main_thread() \
                and path == self.path:
            raise Exception(self._status)

    def run(self):
        self.sort()


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
            try:  # Catch all exception in thread
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


def sort_targets(path_to_target, threaded=False):
    sorter = FileSorter()

    if isinstance(path_to_target, str):
        pathes = path_to_target.split()
    elif isinstance(path_to_target, list):
        pathes = path_to_target
    else:
        raise ValueError(f"{path_to_target} value error.")
    for path in pathes:
        task = Task(pathes)
        task += Filter("archives", ["zip", "tar", "tgz", "gz", "7zip", "7z", "iso", "rar"], ["unpack", "move"])
        task += Filter("audios", ["wav", "mp3", "ogg", "amr"], ["move"])
        task += Filter("images", ["jpeg", "png", "jpg", "svg"], ["move"])
        task += Filter("videos", ["avi", "mp4", "mov", "mkv"], ["move"])
        task += Filter("documents", ["doc", "docx", "txt", "pdf", "xls", "xlsx", "ppt", "pptx", "rtf", "xml", "ini"], ["move"])
        task += Filter("softwares", ["exe", "msi", "bat", "dll"], ["move"])
        task += Filter("other", [""], ["move"])

        sorter += task

    if threaded:
        sorter.start()  # Start tasks as separated threads. All exceptions store in Task's _status(Queue()) attribute
    else:  # Will raise excetion if it has been
        try:
            sorter.sort()  # Start tasks in main thread.
        except Exception as e:
            pass


if __name__ == "__main__":
    sort_targets("D:/edu/test D:/edu/test1")
