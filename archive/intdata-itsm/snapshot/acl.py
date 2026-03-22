"""Перечень разрешений и утилиты проверки доступа к ITSM тикетам."""
from __future__ import annotations

from typing import Collection
from uuid import UUID

from .models import ITSMTicket

PERM_CLIENT_READ = "nexus.itsm:read"
PERM_CLIENT_WRITE = "nexus.itsm:write"
PERM_SPECIALIST_MANAGE = "crm.itsm:manage"
PERM_MANAGER_REPORTS = "crm.itsm:reports"


def _has_scope(scopes: Collection[str], scope: str) -> bool:
    return scope in scopes


def can_view_ticket(
    ticket: ITSMTicket,
    *,
    subject_id: UUID | None,
    scopes: Collection[str],
    superuser: bool = False,
) -> bool:
    if superuser or _has_scope(scopes, PERM_SPECIALIST_MANAGE):
        return True
    if subject_id and ticket.created_by_subject == subject_id:
        return True
    return _has_scope(scopes, PERM_CLIENT_READ)


def can_update_ticket(
    ticket: ITSMTicket,
    *,
    subject_id: UUID | None,
    scopes: Collection[str],
    superuser: bool = False,
) -> bool:
    if superuser or _has_scope(scopes, PERM_SPECIALIST_MANAGE):
        return True
    if subject_id and ticket.created_by_subject == subject_id:
        return _has_scope(scopes, PERM_CLIENT_WRITE)
    return False


__all__ = [
    "PERM_CLIENT_READ",
    "PERM_CLIENT_WRITE",
    "PERM_SPECIALIST_MANAGE",
    "PERM_MANAGER_REPORTS",
    "can_view_ticket",
    "can_update_ticket",
]
