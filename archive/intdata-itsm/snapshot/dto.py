"""Pydantic и прикладные объекты, описывающие домен ITSM."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Collection
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .enums import ITSMEventType, ITSMTicketPriority, ITSMTicketStatus


class TicketEvent(BaseModel):
    """Событие таймлайна ITSM-тикета."""

    event_type: ITSMEventType
    payload: dict[str, Any] | None = None
    created_by_subject: UUID | None = None
    created_by_name: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Ticket(BaseModel):
    """Тикет поддержки с вложенным таймлайном."""

    public_id: UUID
    title: str
    description: str | None
    status: ITSMTicketStatus
    priority: ITSMTicketPriority
    flowable_process_id: str | None
    para_container_type: str | None
    para_container_id: int | None
    created_by_subject: UUID | None
    created_by_name: str | None
    due_at: datetime | None
    metadata: dict[str, Any] | None = Field(default=None, alias="meta")
    created_at: datetime
    updated_at: datetime
    events: list[TicketEvent] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TicketCreate(BaseModel):
    """Данные для создания тикета клиентом или специалистом."""

    title: str
    description: str | None = None
    priority: ITSMTicketPriority = ITSMTicketPriority.medium
    para_container_type: str | None = None
    para_container_id: int | None = None
    due_at: datetime | None = None
    metadata: dict[str, Any] | None = None
    initial_comment: str | None = None

    model_config = ConfigDict(extra="forbid")


class TicketUpdate(BaseModel):
    """Частичное обновление тикета."""

    status: ITSMTicketStatus | None = None
    priority: ITSMTicketPriority | None = None
    description: str | None = None
    due_at: datetime | None = None
    metadata: dict[str, Any] | None = None
    comment: str | None = None

    model_config = ConfigDict(extra="forbid")


@dataclass(slots=True)
class TicketQuery:
    """Параметры выборки тикетов."""

    subject_filter: UUID | None = None
    statuses: Collection[ITSMTicketStatus] | None = None
    priorities: Collection[ITSMTicketPriority] | None = None
    flowable_ids: Collection[str] | None = None
    para_container_type: str | None = None
    para_container_id: int | None = None
    limit: int = 100
    offset: int = 0
    order_desc: bool = True


class FlowableEvent(BaseModel):
    """Payload от Flowable для обновления тикета."""

    event_type: str
    process_instance_id: UUID
    status: ITSMTicketStatus | None = None
    comment: str | None = None
    actor_subject: UUID | None = None
    actor_name: str | None = None
    variables: dict[str, Any] | None = None

    model_config = ConfigDict(extra="forbid")


class TicketsSummary(BaseModel):
    """Сводная аналитика по тикетам для CRM."""

    generated_at: datetime
    total_open: int
    open_by_status: dict[str, int]
    open_by_priority: dict[str, int]
    overdue: int
    resolved_last_7_days: int
    avg_resolution_time_hours: float | None = None

    model_config = ConfigDict(extra="forbid")


__all__ = [
    "Ticket",
    "TicketCreate",
    "TicketUpdate",
    "TicketEvent",
    "TicketQuery",
    "FlowableEvent",
    "TicketsSummary",
]
