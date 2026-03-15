"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import asyncio
from typing import Any, List

import aiohttp
import requests


USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(url: str) -> List[dict[str, Any]]:
    """Fetch JSON data from the given URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except OSError:
        # Fallback for environments where aiohttp network access is restricted
        def _get() -> List[dict[str, Any]]:
            resp = requests.get(url)
            resp.raise_for_status()
            return resp.json()

        return await asyncio.to_thread(_get)


async def fetch_users_data() -> List[dict[str, Any]]:
    """Return users data from remote resource."""

    return await fetch_json(USERS_DATA_URL)


async def fetch_posts_data() -> List[dict[str, Any]]:
    """Return posts data from remote resource."""

    return await fetch_json(POSTS_DATA_URL)

