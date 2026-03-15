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

from .jsonplaceholder_requests import fetch_posts_data, fetch_users_data
from .models import Base, Post, Session, User, engine


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )

    async with Session() as session:
        user_objects = [
            User(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                email=user["email"],
            )
            for user in users_data
        ]
        session.add_all(user_objects)
        await session.commit()

        post_objects = [
            Post(
                id=post["id"],
                user_id=post["userId"],
                title=post["title"],
                body=post["body"],
            )
            for post in posts_data
        ]
        session.add_all(post_objects)
        await session.commit()

    await engine.dispose()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
