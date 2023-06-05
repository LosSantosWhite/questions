from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgresql.dependencies import get_async_session
from app.modules.questions.services import QuestionServices


async def get_questions_services(
    session: AsyncSession = Depends(get_async_session),
) -> QuestionServices:
    return QuestionServices(session=session)
