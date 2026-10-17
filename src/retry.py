import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)


async def get_with_retry(
    url: str,
    max_attempts: int = 3,
    base_delay: float = 0.5,
) -> httpx.Response:
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            response = await _client_get(url)
            if response.status_code in (429, 500, 502, 503, 504):
                logger.warning("attempt %d got %d", attempt, response.status_code)
                last_error = httpx.HTTPStatusError(
                    f"status {response.status_code}",
                    request=response.request,
                    response=response,
                )
            else:
                response.raise_for_status()
                return response
        except httpx.TimeoutException as e:
            logger.warning("attempt %d timed out", attempt)
            last_error = e

        if attempt < max_attempts:
            delay = base_delay * (2 ** (attempt - 1))
            await asyncio.sleep(delay)

    assert last_error is not None
    raise last_error


async def _client_get(url: str) -> httpx.Response:
    async with httpx.AsyncClient(timeout=5.0) as client:
        return await client.get(url)