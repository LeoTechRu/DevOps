"""Utilities for fetching data from ``jsonplaceholder.typicode.com``.

The module exposes a small set of asynchronous helper functions used in the
homework.  They download JSON data from the remote service using :mod:`aiohttp`.
"""

from typing import Any
import socket

import aiohttp

# Public URLs of the resources used in the homework
USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    """Fetch ``url`` and return parsed JSON payload.

    A separate helper function makes it easier to reuse the logic for both
    users and posts requests.
    """

    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_users_data() -> Any:
    """Download and return users data from :data:`USERS_DATA_URL`."""

    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        return await fetch_json(session, USERS_DATA_URL)


async def fetch_posts_data() -> Any:
    """Download and return posts data from :data:`POSTS_DATA_URL`."""

    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        return await fetch_json(session, POSTS_DATA_URL)


__all__ = [
    "USERS_DATA_URL",
    "POSTS_DATA_URL",
    "fetch_users_data",
    "fetch_posts_data",
    "fetch_json",
]

