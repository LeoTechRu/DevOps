"""ITSM service layer orchestrating Flowable processes and Flowable runtime."""
from __future__ import annotations

import logging
import uuid
from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .. import (
    FlowableClient,
    FlowableConfig,
    ITSMRepository,
    ITSMTicket,
    ITSMTicketStatus,
    TicketQuery,
)
from ..config import build_flowable_config, settings
from ..db import async_session
from .schemas import ITSMTicketCreate, ITSMTicketUpdate

log = logging.getLogger(__name__)


class ITSMService:
    """Facade managing ITSM tickets and Flowable runtime."""

    def __init__(
        self,
        session: Optional[AsyncSession] = None,
        *,
        flowable: Optional[FlowableClient] = None,
        flowable_config: Optional[FlowableConfig] = None,
    ) -> None:
        self.session = session
        self._external = session is not None
        config = flowable_config or build_flowable_config(settings)
        self.flowable = flowable or FlowableClient(config)
        self._repository: ITSMRepository | None = None

    async def __aenter__(self) -> "ITSMService":
        if self.session is None:
            self.session = async_session()
        self._repository = ITSMRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # pragma: no cover
        if not self._external and self.session is not None:
            try:
                if exc_type is None:
                    await self.session.commit()
                else:
                    await self.session.rollback()
            finally:
                await self.session.close()

    def _repo(self) -> ITSMRepository:
        if self.session is None:
            raise RuntimeError("ITSMService session is not initialised")
        if self._repository is None:
            self._repository = ITSMRepository(self.session)
        return self._repository

    async def create_ticket(
        self,
        payload: ITSMTicketCreate,
        *,
        created_by_subject: Optional[uuid.UUID],
        created_by_name: Optional[str],
    ) -> ITSMTicket:
        """Создаёт тикет и запускает Flowable-процесс (если он включён)."""
        repo = self._repo()
        ticket = await repo.create_ticket(
            payload,
            created_by_subject=created_by_subject,
            created_by_name=created_by_name,
        )

        process_variables = {
            "ticketPublicId": str(ticket.public_id),
            "priority": ticket.priority.value,
            "creator": created_by_name or "",
        }
        if payload.para_container_type:
            process_variables["paraContainerType"] = payload.para_container_type
        if payload.para_container_id is not None:
            process_variables["paraContainerId"] = str(payload.para_container_id)

        process_id = await self.flowable.start_process(variables=process_variables)
        if process_id:
            ticket = await repo.attach_flowable_process(
                ticket,
                process_id,
                actor_subject=created_by_subject,
                actor_name=created_by_name,
                target_status=ITSMTicketStatus.in_progress,
            )
        return ticket

    async def list_tickets(
        self,
        *,
        subject_filter: Optional[uuid.UUID] = None,
        limit: int = 100,
    ) -> Sequence[ITSMTicket]:
        query = TicketQuery(subject_filter=subject_filter, limit=limit)
        return await self._repo().list_tickets(query)

    async def get_ticket_by_public_id(
        self, public_id: uuid.UUID
    ) -> Optional[ITSMTicket]:
        return await self._repo().get_ticket_by_public_id(public_id)

    async def get_ticket_by_flowable_id(self, process_id: str) -> Optional[ITSMTicket]:
        return await self._repo().get_ticket_by_flowable_id(process_id)

    async def update_ticket(
        self,
        ticket: ITSMTicket,
        payload: ITSMTicketUpdate,
        *,
        actor_subject: Optional[uuid.UUID],
        actor_name: Optional[str],
    ) -> ITSMTicket:
        return await self._repo().update_ticket(
            ticket,
            payload,
            actor_subject=actor_subject,
            actor_name=actor_name,
        )

    async def apply_flowable_event(
        self,
        process_instance_id: str,
        *,
        event_type: str,
        status: Optional[ITSMTicketStatus],
        comment: Optional[str],
        actor_subject: Optional[uuid.UUID],
        actor_name: Optional[str],
        variables: Optional[dict[str, object]] = None,
    ) -> ITSMTicket | None:
        ticket = await self.get_ticket_by_flowable_id(process_instance_id)
        if ticket is None:
            return None

        normalized_event = event_type.upper()
        target_status = status

        if target_status is None:
            if normalized_event == "PROCESS_COMPLETED":
                target_status = ITSMTicketStatus.resolved
            elif normalized_event in {"PROCESS_CANCELLED", "PROCESS_TERMINATED"}:
                target_status = ITSMTicketStatus.cancelled

        return await self._repo().apply_flowable_event(
            ticket,
            event_type=event_type,
            status=target_status,
            comment=comment,
            actor_subject=actor_subject,
            actor_name=actor_name,
            variables=variables,
        )
