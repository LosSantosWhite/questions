import asyncio
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
                created_at=question["created_at"],
                answer=question["answer"],
            )
            for question in questions
        ]
        return questions


if __name__ == "__main__":
    print(asyncio.run(request_questions(3)))
