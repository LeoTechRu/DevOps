"""Настройки модуля ITSM.

Используем pydantic-settings, чтобы читать переменные окружения с префиксом
`ITSM_`. При отсутствии кастомных значений используем общие настройки
(`shared.config.settings`).
"""
from __future__ import annotations

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.config import settings as shared_settings


class ITSMSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ITSM_")

    DB_DSN: str | None = None
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 5
    FLOWABLE_BASE_URL: str | None = None
    FLOWABLE_USERNAME: str | None = None
    FLOWABLE_PASSWORD: str | None = None
    FLOWABLE_PROCESS_KEY: str | None = None
    FLOWABLE_TIMEOUT: float = 10.0
    FLOWABLE_WEBHOOK_TOKEN: str | None = None

    def database_dsn(self) -> str:
        """Возвращает строку подключения БД (fallback к shared settings)."""
        if self.DB_DSN:
            return self.DB_DSN
        return shared_settings.DB_DSN

    def model_post_init(self, __context) -> None:
        """Гарантируем обратную совместимость с переменными без префикса."""
        self.FLOWABLE_BASE_URL = self.FLOWABLE_BASE_URL or os.getenv("FLOWABLE_BASE_URL")
        self.FLOWABLE_USERNAME = self.FLOWABLE_USERNAME or os.getenv("FLOWABLE_USERNAME")
        self.FLOWABLE_PASSWORD = self.FLOWABLE_PASSWORD or os.getenv("FLOWABLE_PASSWORD")
        self.FLOWABLE_PROCESS_KEY = self.FLOWABLE_PROCESS_KEY or os.getenv("FLOWABLE_PROCESS_KEY")
        self.FLOWABLE_WEBHOOK_TOKEN = self.FLOWABLE_WEBHOOK_TOKEN or os.getenv(
            "FLOWABLE_WEBHOOK_TOKEN"
        )


def build_flowable_config(settings: ITSMSettings):
    """Формирует конфигурацию Flowable на основе настроек."""
    from itsm.flowable.client import FlowableConfig

    return FlowableConfig(
        base_url=settings.FLOWABLE_BASE_URL,
        username=settings.FLOWABLE_USERNAME,
        password=settings.FLOWABLE_PASSWORD,
        process_key=settings.FLOWABLE_PROCESS_KEY,
        timeout=settings.FLOWABLE_TIMEOUT,
    )


settings = ITSMSettings()
