"""Перечисления домена ITSM, используемые одновременно в Nexus и CRM."""

from enum import Enum


class ITSMTicketStatus(Enum):
    """Состояния жизненного цикла ITSM-тикета."""

    draft = "draft"
    submitted = "submitted"
    in_progress = "in_progress"
    awaiting_input = "awaiting_input"
    resolved = "resolved"
    closed = "closed"
    cancelled = "cancelled"


class ITSMTicketPriority(Enum):
    """Уровни приоритета клиентских обращений."""

    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class ITSMEventType(Enum):
    """Типы событий, фиксируемых в истории тикета."""

    status_change = "status_change"
    comment = "comment"
    attachment = "attachment"
    flowable_event = "flowable_event"
