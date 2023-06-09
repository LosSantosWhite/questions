from typing import Any

from redis import Redis
from app.database.postgresql.crud import CRUD
from app.database.redis.client import RedisClient
from app.modules.questions.crud.models import Question


class QuestionCRUD(CRUD[Question]):
    table = Question


class QuestionRedisCRUD(RedisClient):
    def set_last_record(self, value: dict):
        return self.conn.hmset("last_record", value)

    def get_last_record(self) -> dict | None:
        values = self.conn.hmget(
            "last_record", keys=["question_id", "text", "answer", "created_at"]
        )
        return dict(
            question_id=values[0],
            text=values[1],
            answer=values[2],
            created_at=values[3],
        )

    def check_id(self, question_id: str) -> bool:
        return question_id in self.get_questions_list()

    def append_question_id(self, value: str) -> None:
        self.append("questions_ids", value)

    def get_questions_list(self) -> list[str]:
        result: list[bytes] = self.get_list("questions_ids")
        return [i.decode() for i in result]
