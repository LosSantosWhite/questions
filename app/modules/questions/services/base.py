from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgresql.decorators import transaction
from app.clients.questions import request_questions
from app.modules.questions.crud import QuestionCRUD
from app.modules.questions.crud.models import Question
from app.modules.questions.services.schemas import QuestionCreate

from app.utils.decorators import duplicate


class QuestionServices:
    last_record = {}

    def __init__(self, session: AsyncSession):
        self.session = session
        self.questions = QuestionCRUD(session=self.session)

    @transaction
    @duplicate(detail="This question already exists")
    async def create(self, schema: QuestionCreate, _commit: bool = True) -> Question:
        return await self.questions.insert(data=schema.dict())

    @transaction
    @duplicate(detail="This question already exists")
    async def bulk_create(
        self, schemas_list: list[QuestionCreate], _commit: bool = True
    ):
        for schema in schemas_list:
            self.last_record = await self.create(schema)

    async def reqeust_questions(self, count: int):
        questions = await request_questions(count)
        count_errors = 0
        try:
            await self.bulk_create(questions)
        except IntegrityError:
            count_errors += 1

        if count_errors:
            await self.reqeust_questions(count_errors)
