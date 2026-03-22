"""Репозиторий для работы с ITSM тикетами и событиями."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import asc, desc, select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .dto import TicketCreate, TicketQuery, TicketUpdate, TicketsSummary
from .enums import ITSMEventType, ITSMTicketPriority, ITSMTicketStatus
from .models import ITSMTicket, ITSMTicketEvent

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ITSMRepository:
    """Асинхронный доступ к тикетам и событиям ITSM."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    async def list_tickets(self, query: TicketQuery) -> Sequence[ITSMTicket]:
        stmt = (
            select(ITSMTicket)
            .options(selectinload(ITSMTicket.events))
        )
        if query.order_desc:
            stmt = stmt.order_by(desc(ITSMTicket.created_at))
        else:
            stmt = stmt.order_by(asc(ITSMTicket.created_at))

        if query.subject_filter:
            stmt = stmt.where(ITSMTicket.created_by_subject == query.subject_filter)
        if query.statuses:
            stmt = stmt.where(ITSMTicket.status.in_(list(query.statuses)))
        if query.priorities:
            stmt = stmt.where(ITSMTicket.priority.in_(list(query.priorities)))
        if query.flowable_ids:
            stmt = stmt.where(ITSMTicket.flowable_process_id.in_(list(query.flowable_ids)))
        if query.para_container_type:
            stmt = stmt.where(ITSMTicket.para_container_type == query.para_container_type)
        if query.para_container_id is not None:
            stmt = stmt.where(ITSMTicket.para_container_id == query.para_container_id)

        stmt = stmt.offset(max(query.offset, 0)).limit(max(query.limit, 1))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_ticket_by_public_id(self, public_id: UUID) -> ITSMTicket | None:
        stmt = (
            select(ITSMTicket)
            .where(ITSMTicket.public_id == public_id)
            .options(selectinload(ITSMTicket.events))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_ticket_by_flowable_id(self, process_id: str) -> ITSMTicket | None:
        stmt = (
            select(ITSMTicket)
            .where(ITSMTicket.flowable_process_id == process_id)
            .options(selectinload(ITSMTicket.events))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    async def create_ticket(
        self,
        data: TicketCreate,
        *,
        created_by_subject: UUID | None,
        created_by_name: str | None,
    ) -> ITSMTicket:
        ticket = ITSMTicket(
            title=data.title,
            description=data.description,
            priority=data.priority,
            para_container_type=data.para_container_type,
            para_container_id=data.para_container_id,
            created_by_subject=created_by_subject,
            created_by_name=created_by_name,
            due_at=data.due_at,
            meta=data.metadata or {},
            status=ITSMTicketStatus.submitted,
        )
        self.session.add(ticket)
        await self.session.flush()

        self.session.add(
            ITSMTicketEvent(
                ticket=ticket,
                event_type=ITSMEventType.status_change,
                payload={"from": ITSMTicketStatus.draft.value, "to": ticket.status.value},
                created_by_subject=created_by_subject,
                created_by_name=created_by_name,
            )
        )

        if data.initial_comment:
            self.session.add(
                ITSMTicketEvent(
                    ticket=ticket,
                    event_type=ITSMEventType.comment,
                    payload={"comment": data.initial_comment},
                    created_by_subject=created_by_subject,
                    created_by_name=created_by_name,
                )
            )

        await self.session.flush()
        await self.session.refresh(ticket)
        return ticket

    async def update_ticket(
        self,
        ticket: ITSMTicket,
        data: TicketUpdate,
        *,
        actor_subject: UUID | None,
        actor_name: str | None,
    ) -> ITSMTicket:
        status_changed = False
        if data.status and data.status != ticket.status:
            self.session.add(
                ITSMTicketEvent(
                    ticket=ticket,
                    event_type=ITSMEventType.status_change,
                    payload={"from": ticket.status.value, "to": data.status.value},
                    created_by_subject=actor_subject,
                    created_by_name=actor_name,
                )
            )
            ticket.status = data.status
            status_changed = True

        if data.priority and data.priority != ticket.priority:
            ticket.priority = data.priority
        if data.description is not None:
            ticket.description = data.description
        if data.metadata is not None:
            ticket.meta = data.metadata
        if data.due_at is not None:
            ticket.due_at = data.due_at

        if data.comment:
            self.session.add(
                ITSMTicketEvent(
                    ticket=ticket,
                    event_type=ITSMEventType.comment,
                    payload={"comment": data.comment},
                    created_by_subject=actor_subject,
                    created_by_name=actor_name,
                )
            )

        if status_changed or data.comment or data.priority or data.description is not None or data.metadata is not None or data.due_at is not None:
            ticket.updated_at = _utcnow()

        await self.session.flush()
        await self.session.refresh(ticket)
        return ticket

    async def attach_flowable_process(
        self,
        ticket: ITSMTicket,
        process_id: str,
        *,
        actor_subject: UUID | None,
        actor_name: str | None,
        target_status: ITSMTicketStatus | None = None,
    ) -> ITSMTicket:
        ticket.flowable_process_id = process_id
        if target_status and ticket.status != target_status:
            ticket = await self.update_ticket(
                ticket,
                TicketUpdate(status=target_status),
                actor_subject=actor_subject,
                actor_name=actor_name,
            )
        else:
            await self.session.flush()
            await self.session.refresh(ticket)
        return ticket

    async def apply_flowable_event(
        self,
        ticket: ITSMTicket,
        *,
        event_type: str,
        status: ITSMTicketStatus | None,
        comment: str | None,
        actor_subject: UUID | None,
        actor_name: str | None,
        variables: dict[str, Any] | None = None,
    ) -> ITSMTicket:
        update_required = any([status, comment])
        if status or comment:
            update_payload = TicketUpdate(status=status, comment=comment)
            ticket = await self.update_ticket(
                ticket,
                update_payload,
                actor_subject=actor_subject,
                actor_name=actor_name,
            )
        flow_event = ITSMTicketEvent(
            ticket=ticket,
            event_type=ITSMEventType.flowable_event,
            payload={"event_type": event_type, "variables": variables or {}},
            created_by_subject=actor_subject,
            created_by_name=actor_name,
        )
        self.session.add(flow_event)
        if not update_required:
            await self.session.flush()
            await self.session.refresh(ticket)
        else:
            await self.session.flush()
        await self.session.refresh(ticket)
        return ticket

    async def get_tickets_summary(
        self,
        *,
        now: datetime | None = None,
        window_days: int = 7,
    ) -> TicketsSummary:
        """Вычисляет агрегированные метрики по тикетам для CRM отчётности."""

        reference_time = now or _utcnow()
        open_statuses = {
            ITSMTicketStatus.submitted,
            ITSMTicketStatus.in_progress,
            ITSMTicketStatus.awaiting_input,
        }
        resolved_statuses = {
            ITSMTicketStatus.resolved,
            ITSMTicketStatus.closed,
        }
        open_values = [status for status in open_statuses]

        # Количество активных тикетов по статусам
        status_stmt = (
            select(ITSMTicket.status, func.count())
            .where(ITSMTicket.status.in_(open_values))
            .group_by(ITSMTicket.status)
        )
        status_rows = (await self.session.execute(status_stmt)).all()
        open_by_status = {
            (status.value if isinstance(status, ITSMTicketStatus) else str(status)): int(count)
            for status, count in status_rows
        }
        total_open = sum(open_by_status.values())

        # Количество активных тикетов по приоритетам
        priority_stmt = (
            select(ITSMTicket.priority, func.count())
            .where(ITSMTicket.status.in_(open_values))
            .group_by(ITSMTicket.priority)
        )
        priority_rows = (await self.session.execute(priority_stmt)).all()
        open_by_priority = {
            (
                priority.value
                if isinstance(priority, ITSMTicketPriority)
                else str(priority)
            ): int(count)
            for priority, count in priority_rows
        }

        # Просроченные тикеты
        overdue_stmt = (
            select(func.count())
            .where(ITSMTicket.status.in_(open_values))
            .where(ITSMTicket.due_at.is_not(None))
            .where(ITSMTicket.due_at < reference_time)
        )
        overdue = int(await self.session.scalar(overdue_stmt) or 0)

        past_window = reference_time - timedelta(days=window_days)
        resolved_values = [status.value for status in resolved_statuses]

        # Количество тикетов, решённых за последний период
        payload_status_to = ITSMTicketEvent.payload.op("->>")("to")
        resolved_stmt = (
            select(func.count(distinct(ITSMTicketEvent.ticket_id)))
            .where(ITSMTicketEvent.event_type == ITSMEventType.status_change)
            .where(payload_status_to.in_(resolved_values))
            .where(ITSMTicketEvent.created_at >= past_window)
        )
        resolved_last_window = int(await self.session.scalar(resolved_stmt) or 0)

        # Среднее время решения
        resolution_stmt = (
            select(
                ITSMTicketEvent.ticket_id,
                ITSMTicket.created_at.label("ticket_created_at"),
                func.min(ITSMTicketEvent.created_at).label("resolved_at"),
            )
            .join(ITSMTicket, ITSMTicket.id == ITSMTicketEvent.ticket_id)
            .where(ITSMTicketEvent.event_type == ITSMEventType.status_change)
            .where(payload_status_to.in_(resolved_values))
            .group_by(ITSMTicketEvent.ticket_id, ITSMTicket.created_at)
        )
        resolution_rows = (await self.session.execute(resolution_stmt)).all()
        durations_hours: list[float] = []
        for row in resolution_rows:
            resolved_at = row.resolved_at
            created_at = row.ticket_created_at
            if resolved_at and created_at:
                delta = resolved_at - created_at
                durations_hours.append(max(delta.total_seconds(), 0.0) / 3600.0)

        avg_resolution = (
            sum(durations_hours) / len(durations_hours) if durations_hours else None
        )

        return TicketsSummary(
            generated_at=reference_time,
            total_open=total_open,
            open_by_status=open_by_status,
            open_by_priority=open_by_priority,
            overdue=overdue,
            resolved_last_7_days=resolved_last_window,
            avg_resolution_time_hours=avg_resolution,
        )


__all__ = ["ITSMRepository"]
