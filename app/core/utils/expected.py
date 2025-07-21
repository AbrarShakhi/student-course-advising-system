from typing import Any


class Expected:
    def __init__(self, value=None, error=None) -> None:
        self._value = value
        self._error = error

    def not_ok(self) -> bool:
        """Returns True if an exception was caught."""
        return self._error is not None

    def value(self) -> Any:
        """Returns the value if no exception, else None."""
        return self._value

    def error(self) -> None | Any:
        """Returns the exception if there was one, else None."""
        return self._error


def expected(func, *args, **kwargs) -> Expected:
    try:
        value = func(*args, **kwargs)
        return Expected(value=value)
    except Exception as e:
        return Expected(error=e)
