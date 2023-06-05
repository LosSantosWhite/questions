from app.database.postgresql.crud import CRUD
from app.modules.questions.crud.models import Question


class QuestionCRUD(CRUD[Question]):
    table = Question
