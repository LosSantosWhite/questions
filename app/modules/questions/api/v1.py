from fastapi import APIRouter, Depends

from app.modules.questions.services import QuestionServices, get_questions_services
from app.modules.questions.services.schemas import QuestionBase


router = APIRouter(prefix="/questions", tags=["questions"])


@router.on_event("startup")
async def start_app_questions():
    questions = await get_questions_services()
    return await questions.startup_insert_questions_id_in_redis()


@router.post("/", response_model=QuestionBase)
async def questions_request(
    count: int, questions: QuestionServices = Depends(get_questions_services)
):
    return await questions.insert_questions(count)
