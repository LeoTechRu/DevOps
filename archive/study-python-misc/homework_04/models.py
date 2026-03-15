"""Database models and engine configuration for homework 04.

The module defines an asynchronous SQLAlchemy engine, a declarative base and a
session factory.  Two ORM models are provided: :class:`User` and
:class:`Post`.  They are linked via a standard one-to-many relationship.
"""

from __future__ import annotations

import os
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

# Asynchronous engine and session factory ----------------------------------

engine = create_async_engine(PG_CONN_URI, echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# ORM models ----------------------------------------------------------------


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    user = relationship("User", back_populates="posts")


__all__ = [
    "engine",
    "Base",
    "Session",
    "User",
    "Post",
]

