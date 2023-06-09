from datetime import datetime
from pydantic import BaseModel


class QuestionBase(BaseModel):
    question_id: int | None
    text: str | None
    answer: str | None
    created_at: datetime | None


class QuestionCreate(QuestionBase):
    ...
