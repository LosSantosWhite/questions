from fastapi import APIRouter, Depends

from app.modules.questions.services import QuestionServices, get_questions_services
from app.modules.questions.services.schemas import QuestionBase


router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=QuestionBase)
async def questions_request(
    count: int, questions: QuestionServices = Depends(get_questions_services)
):
    return await questions.main(count)
