import httpx
import pytest

from src import retry


@pytest.mark.asyncio
async def test_succeeds_first_try(monkeypatch):
    calls = {"n": 0}

    async def fake_get(url):
        calls["n"] += 1
        return httpx.Response(200, request=httpx.Request("GET", url), json={"ok": True})

    monkeypatch.setattr(retry, "_client_get", fake_get)
    resp = await retry.get_with_retry("http://x")
    assert resp.status_code == 200
    assert calls["n"] == 1


@pytest.mark.asyncio
async def test_retries_on_500_then_succeeds(monkeypatch):
    calls = {"n": 0}

    async def fake_get(url):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(500, request=httpx.Request("GET", url))
        return httpx.Response(200, request=httpx.Request("GET", url), json={"ok": True})

    monkeypatch.setattr(retry, "_client_get", fake_get)
    resp = await retry.get_with_retry("http://x", base_delay=0.01)
    assert resp.status_code == 200
    assert calls["n"] == 3


@pytest.mark.asyncio
async def test_gives_up_after_max_attempts(monkeypatch):
    async def fake_get(url):
        return httpx.Response(503, request=httpx.Request("GET", url))

    monkeypatch.setattr(retry, "_client_get", fake_get)
    with pytest.raises(httpx.HTTPStatusError):
        await retry.get_with_retry("http://x", max_attempts=3, base_delay=0.01)