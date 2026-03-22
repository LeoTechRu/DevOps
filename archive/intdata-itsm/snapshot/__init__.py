"""Общий ITSM-пакет, доступный модулям Nexus и CRM."""

from .acl import (
    PERM_CLIENT_READ,
    PERM_CLIENT_WRITE,
    PERM_MANAGER_REPORTS,
    PERM_SPECIALIST_MANAGE,
    can_update_ticket,
    can_view_ticket,
)
from .dto import (
    FlowableEvent,
    Ticket,
    TicketCreate,
    TicketEvent,
    TicketQuery,
    TicketUpdate,
    TicketsSummary,
)
from .enums import ITSMEventType, ITSMTicketPriority, ITSMTicketStatus
from .flowable.client import FlowableClient, FlowableConfig
from .models import ITSMTicket, ITSMTicketEvent
from .repository import ITSMRepository

__all__ = [
    "FlowableClient",
    "FlowableConfig",
    "ITSMEventType",
    "ITSMRepository",
    "ITSMTicket",
    "ITSMTicketEvent",
    "ITSMTicketPriority",
    "ITSMTicketStatus",
    "Ticket",
    "TicketCreate",
    "TicketEvent",
    "TicketQuery",
    "TicketUpdate",
    "FlowableEvent",
    "TicketsSummary",
    "PERM_CLIENT_READ",
    "PERM_CLIENT_WRITE",
    "PERM_MANAGER_REPORTS",
    "PERM_SPECIALIST_MANAGE",
    "can_view_ticket",
    "can_update_ticket",
]
