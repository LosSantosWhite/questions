import asyncio
from datetime import datetime
import json
import httpx


async def request_questions(count: int) -> list[dict]:
    url = "https://jservice.io/api/random"
    async with httpx.AsyncClient() as client:
        result = await client.get(url, params={"count": count})
        questions = json.loads(result.text)
        result = [
            dict(
                question_id=question["id"],
                text=question["question"],
                created_at=datetime.strptime(
                    question["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).strftime("%Y-%m-%d %H:%M:%S.%f"),
                answer=question["answer"],
            )
            for question in questions
        ]
        return result
