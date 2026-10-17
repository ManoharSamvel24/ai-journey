import asyncio
import time

import pytest

from src.async_demo import fetch_fake


@pytest.mark.asyncio
async def test_fetch_fake_returns():
    result = await fetch_fake("a", 0.01)
    assert result == "a done"


@pytest.mark.asyncio
async def test_concurrent_is_fast():
    start = time.perf_counter()
    await asyncio.gather(
        fetch_fake("a", 1.0),
        fetch_fake("b", 1.0),
        fetch_fake("c", 1.0),
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0