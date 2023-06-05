from datetime import datetime
from pydantic import BaseModel


class QuestionBase(BaseModel):
    id: int = ""
    question_id: int = ""
    text: str = ""
    answer: str = ""
    created_at: datetime = datetime.utcnow()
