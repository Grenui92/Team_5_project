def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as exc:
            return exc.args[0]
        except KeyError as exc:
            return exc.args[0]
        except ValueError as exc:
            return exc.args[0]
        except TypeError as exc:
            return exc.args[0]
        except FileExistsError as exc:
            return exc.args[0]
        except FileNotFoundError as exc:
            return exc.args[0]
        except Warning as exc:
            return exc.args[0]
        except StopIteration as exc:
            return exc.args[0]
    return wrapper