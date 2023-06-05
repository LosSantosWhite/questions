from fastapi import FastAPI

from app.modules.questions.api.v1 import router as question_router


def create_app():
    app = FastAPI()

    app.include_router(question_router)

    return app
