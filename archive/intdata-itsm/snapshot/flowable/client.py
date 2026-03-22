"""Клиент Flowable, переиспользуемый Nexus и CRM."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx

log = logging.getLogger(__name__)


@dataclass(slots=True)
class FlowableConfig:
    base_url: str | None
    username: str | None
    password: str | None
    process_key: str | None = None
    timeout: float = 10.0

    def is_enabled(self) -> bool:
        return bool(self.base_url and self.username and self.password)


class FlowableClient:
    """Небольшой REST-клиент Flowable."""

    def __init__(self, config: FlowableConfig) -> None:
        self.config = config

    async def start_process(
        self,
        *,
        process_key: str | None = None,
        variables: dict[str, Any] | None = None,
    ) -> str | None:
        """Запуск процесса Flowable, возвращает идентификатор экземпляра."""
        if not self.config.is_enabled():
            log.debug("Flowable disabled (missing config)")
            return None

        payload = {
            "processDefinitionKey": process_key or self.config.process_key,
            "variables": [
                {"name": key, "value": value} for key, value in (variables or {}).items()
            ],
        }
        base_url = self.config.base_url.rstrip("/")  # type: ignore[union-attr]
        auth = (self.config.username, self.config.password)  # type: ignore[arg-type]
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                resp = await client.post(
                    f"{base_url}/runtime/process-instances",
                    json=payload,
                    auth=auth,
                )
                resp.raise_for_status()
        except httpx.HTTPError as exc:
            log.warning("Flowable start_process failed: %s", exc)
            return None

        data = resp.json()
        process_id = data.get("id")
        if process_id:
            log.debug("Flowable process started: %s", process_id)
        else:
            log.warning("Flowable response missing process id: %s", data)
        return process_id


__all__ = ["FlowableClient", "FlowableConfig"]
