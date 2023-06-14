from app.database.postgresql.crud import CRUD
from app.database.redis.client import RedisClient
from app.modules.questions.crud.models import Question


class QuestionCRUD(CRUD[Question]):
    table = Question


class QuestionRedisCRUD(RedisClient):
    ...
