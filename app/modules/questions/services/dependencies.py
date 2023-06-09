from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgresql.dependencies import get_async_session
from app.database.redis.dependencies import get_redis_client
from app.modules.questions.services import QuestionServices


async def get_questions_services(
    session: AsyncSession = Depends(get_async_session),
    redis_client=Depends(get_redis_client),
) -> QuestionServices:
    return QuestionServices(session=session, redis_client=redis_client)
