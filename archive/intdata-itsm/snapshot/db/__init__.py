"""Инфраструктура доступа к базе данных ITSM."""
from .session import async_session, engine

__all__ = ["async_session", "engine"]
