from typing import Callable, TYPE_CHECKING
from functools import wraps


if TYPE_CHECKING:
    from app.modules.questions.services import QuestionServices


def redis_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        self: "QuestionServices" = args[0]
        async with self.redis_client.pipeline() as pipeline:
            result = await func(*args, **kwargs)
            return result

    return wrapper
