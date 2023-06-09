from functools import wraps
from typing import Callable

from sqlalchemy.exc import IntegrityError


def duplicate(detail: str = None):
    def constructor(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return constructor
