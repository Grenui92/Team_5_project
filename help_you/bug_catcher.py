import difflib
def erorr_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as exc:
            return f"Wrong information '{exc.args[0]}'."
        except Warning as exc:
            return find_word_with_wrong_key(exc.args[0], exc.args[1])
        except Exception as exc:
            return exc.args[0]
    return wrapper

def find_word_with_wrong_key(srch: str, com: list) -> str:
    result_dict = {}
    for words in com:
        mathcer = difflib.SequenceMatcher(None, srch, words)
        if mathcer.ratio() >= 0.5:
            result_dict[words] = f"{round(mathcer.ratio(), 2)*100}%"

    return f"\nI can't find command '{srch}'.\n" \
           f"Maybe you meant these commands:\n" \
           f"{[f'{k}: {value}' for k, value in result_dict.items()] if result_dict else '<<<I cant find something similar.>>>'}"