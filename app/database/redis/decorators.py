from typing import Callable
from functools import wraps


def redis_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        self = args[0]

        identifier = kwargs.get("identifier", False)
        if not identifier:
            identifier = self.redis_client.acquire_lock()
        kwargs["identifier"] = identifier

        try:
            if identifier:
                result = func(*args, **kwargs)
        finally:
            self.redis_client.realise_lock(identifier)
            return await result

    return wrapper
