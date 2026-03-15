"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
from typing import List

try:
    from . import jsonplaceholder_requests as jp_requests
    from .models import Base, Session, User, Post, engine
except ImportError:  # pragma: no cover - fallback for direct execution
    import jsonplaceholder_requests as jp_requests
    from models import Base, Session, User, Post, engine


async def async_main() -> None:
    """Main entry point for asynchronous workflow.

    The function initialises the database, concurrently fetches users and
    posts data from the remote service and stores them in the database in
    batches.  Finally the database engine is properly disposed of.
    """

    # (Re-)create database schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Fetch remote data concurrently
    users_data, posts_data = await asyncio.gather(
        jp_requests.fetch_users_data(),
        jp_requests.fetch_posts_data(),
    )

    # Store in DB in batches
    async with Session() as session:
        users: List[User] = [
            User(name=u["name"], username=u["username"], email=u["email"])
            for u in users_data
        ]
        session.add_all(users)
        await session.commit()

        posts: List[Post] = [
            Post(user_id=p["userId"], title=p["title"], body=p["body"])
            for p in posts_data
        ]
        session.add_all(posts)
        await session.commit()

    # Close engine connections
    await engine.dispose()


def main() -> None:
    """Synchronous entry point used when executing the module as a script."""

    asyncio.run(async_main())


if __name__ == "__main__":
    main()
