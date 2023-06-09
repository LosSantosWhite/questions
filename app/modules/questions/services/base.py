import asyncio

from datetime import datetime
from functools import wraps

from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgresql.decorators import transaction
from app.database.redis.decorators import redis_session

from app.clients.questions import request_questions
from app.modules.questions.crud import QuestionCRUD, QuestionRedisCRUD
from app.modules.questions.crud.models import Question
from app.modules.questions.services.schemas import QuestionCreate

from app.utils.decorators import duplicate


class QuestionServices:
    def __init__(self, session: AsyncSession, redis_client: Redis):
        self.session = session
        self.questions = QuestionCRUD(session=self.session)
        self.redis_client = QuestionRedisCRUD()

    # [PostgreSQL]
    @transaction
    @duplicate(detail="This question already exists")
    async def create(self, schema: QuestionCreate, _commit: bool = True) -> Question:
        return await self.questions.insert(data=schema.dict())

    @transaction
    async def bulk_create(
        self, schemas_list: list[QuestionCreate], _commit: bool = True
    ):
        for schema in schemas_list:
            await self.create(schema)

    # [Redis]
    @redis_session
    async def main(self, count: int, *args, **kwargs) -> dict:
        questions_list: list[dict] = await request_questions(count)
        duplicates: int = 0
        last_record = self.redis_client.get_last_record()

        for question in questions_list:
            if not self.redis_client.check_id(question):
                q = await self.create(schema=QuestionCreate(**question))
                print(q)
                self.redis_client.append_question_id(question["question_id"])
                self.redis_client.set_last_record(question)
            else:
                duplicates += 1
        if duplicates:
            await self.main(duplicates, *args, **kwargs)
        print(f"{last_record=}")
        return last_record
