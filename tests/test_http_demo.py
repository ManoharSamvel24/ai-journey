import pytest

from src.http_demo import get_github_user, get_github_user_safe


@pytest.mark.integration
def test_get_real_user():
    data = get_github_user("torvalds")
    assert data["login"] == "torvalds"


@pytest.mark.integration
def test_404_returns_none():
    result = get_github_user_safe("this-user-definitely-does-not-exist-xyz123")
    assert result is None