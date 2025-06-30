class ErrorWrapper:
    def __init__(self, error):
        self.error = error

    def not_ok(self):
        return self.error is not None

    def ok(self):
        return self.error is None

    def is_type(self, exc_type):
        return isinstance(self.error, exc_type)

    def get_error(self):
        return self.error

    def __bool__(self):
        return self.error is None

    def __str__(self):
        return str(self.error)


def try_catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), ErrorWrapper(None)
    except Exception as err:
        return None, ErrorWrapper(err)
