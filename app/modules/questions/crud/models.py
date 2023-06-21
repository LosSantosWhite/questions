from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgresql.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(unique=True)
    text: Mapped[str] = mapped_column(String())
    answer: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return (
            f"<Question(id={self.id}, text={self.text[:10]}..., answer={self.answer})>"
        )
