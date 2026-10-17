import asyncio
import time


async def fetch_fake(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"


async def main() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_fake("a", 1.0),
        fetch_fake("b", 1.0),
        fetch_fake("c", 1.0),
    )
    elapsed = time.perf_counter() - start
    print(results)
    print(f"elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())