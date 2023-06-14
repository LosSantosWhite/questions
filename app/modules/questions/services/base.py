from redis.asyncio import Redis
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
    async def insert_question_id(self, question_id: str):
        await self.redis_client.set(question_id, 1)

    async def check_question_id(self, question_id: int | str) -> bool:
        return str(question_id).encode() in await self.redis_client.keys()

    async def set_last_record(self, value: dict):
        return await self.redis_client.hmset("last_record", value)

    async def get_last_record(self) -> dict[str, int | str]:
        values = await self.redis_client.hmget(
            "last_record", keys=["question_id", "text", "answer", "created_at"]
        )
        return dict(
            question_id=values[0],
            text=values[1],
            answer=values[2],
            created_at=values[3],
        )

    # [PostgreSQL + Redis]
    @redis_session
    async def insert_questions(self, count: int, *args, **kwargs) -> dict:
        questions_list: list[dict] = await request_questions(count)
        duplicates: int = 0
        last_record = await self.get_last_record()

        for question in questions_list:
            if not await self.check_question_id(question["question_id"]):
                try:
                    q = await self.create(schema=QuestionCreate(**question))
                except Exception:
                    duplicate += 1
                print(f"{q=}")
                await self.insert_question_id(question["question_id"])
                await self.set_last_record(question)
            else:
                duplicates += 1
        if duplicates:
            await self.insert_questions(duplicates, *args, **kwargs)
        return last_record
