"""SQLAlchemy модели для ITSM тикетов и событий."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, synonym

from shared.db.base import Base

from .enums import ITSMEventType, ITSMTicketPriority, ITSMTicketStatus


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ITSMTicket(Base):
    """Тикет, синхронизируемый с Flowable."""

    __tablename__ = "itsm_tickets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(
        PG_UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(
        Enum(ITSMTicketStatus, name="itsm_ticket_status", native_enum=False),
        nullable=False,
        default=ITSMTicketStatus.draft,
    )
    priority = Column(
        Enum(ITSMTicketPriority, name="itsm_ticket_priority", native_enum=False),
        nullable=False,
        default=ITSMTicketPriority.medium,
    )
    flowable_process_id = Column(String(128))
    para_container_type = Column(String(32))
    para_container_id = Column(BigInteger)
    created_by_subject = Column(PG_UUID(as_uuid=True))
    created_by_name = Column(String(255))
    due_at = Column(DateTime(timezone=True))
    metadata_payload = Column("metadata", JSON, default=dict)
    meta = synonym("metadata_payload")
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    events = relationship(
        "ITSMTicketEvent",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="ITSMTicketEvent.created_at",
    )

    __table_args__ = (
        UniqueConstraint("public_id", name="ux_itsm_ticket_public_id"),
        Index("ix_itsm_ticket_status", "status"),
        Index("ix_itsm_ticket_flowable", "flowable_process_id"),
    )


class ITSMTicketEvent(Base):
    """Запись таймлайна тикета (статус, комментарии, Flowable)."""

    __tablename__ = "itsm_ticket_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_id = Column(BigInteger, ForeignKey("itsm_tickets.id"), nullable=False)
    event_type = Column(
        Enum(ITSMEventType, name="itsm_ticket_event_type", native_enum=False),
        nullable=False,
        default=ITSMEventType.status_change,
    )
    payload = Column(JSON, default=dict)
    created_by_subject = Column(PG_UUID(as_uuid=True))
    created_by_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    ticket = relationship("ITSMTicket", back_populates="events")

    __table_args__ = (
        Index("ix_itsm_ticket_events_ticket", "ticket_id", "created_at"),
    )


__all__ = ["ITSMTicket", "ITSMTicketEvent"]
