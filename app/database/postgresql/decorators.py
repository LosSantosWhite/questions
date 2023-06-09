from functools import wraps
from typing import Callable


def transaction(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        commit = kwargs.pop("_commit", True)
        result = await func(*args, **kwargs)

        self = args[0]

        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return result

    return wrapper
