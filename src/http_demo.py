import httpx


def get_github_user(username: str) -> dict:
    response = httpx.get(
        f"https://api.github.com/users/{username}",
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()


def get_github_user_safe(username: str) -> dict | None:
    try:
        response = httpx.get(
            f"https://api.github.com/users/{username}",
            timeout=5.0,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        raise