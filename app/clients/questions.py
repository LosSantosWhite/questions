import asyncio
import json
import httpx


async def request_questions(count: int) -> list[dict]:
    url = "https://jservice.io/api/random"
    async with httpx.AsyncClient() as client:
        result = await client.get(url, params={"count": count})
        result = json.loads(result.text)

        return result
