import asyncio


async def say_after(delay: float, what: str) -> str:
    await asyncio.sleep(delay)
    return what
