-- 2025-10-14: Core tables for the standalone ITSM module (Flowable integration) and wiki documents.

CREATE TABLE IF NOT EXISTS itsm_tickets (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    priority VARCHAR(16) NOT NULL DEFAULT 'medium',
    flowable_process_id VARCHAR(128),
    para_container_type VARCHAR(24),
    para_container_id BIGINT,
    created_by_subject UUID,
    created_by_name TEXT,
    due_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_itsm_tickets_public_id ON itsm_tickets(public_id);
CREATE INDEX IF NOT EXISTS ix_itsm_tickets_status ON itsm_tickets(status);
CREATE INDEX IF NOT EXISTS ix_itsm_tickets_flowable ON itsm_tickets(flowable_process_id);

CREATE TABLE IF NOT EXISTS itsm_ticket_events (
    id BIGSERIAL PRIMARY KEY,
    ticket_id BIGINT NOT NULL REFERENCES itsm_tickets(id) ON DELETE CASCADE,
    event_type VARCHAR(32) NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb,
    created_by_subject UUID,
    created_by_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE INDEX IF NOT EXISTS ix_itsm_ticket_events_ticket ON itsm_ticket_events(ticket_id, created_at DESC);

CREATE TABLE IF NOT EXISTS knowledge_documents (
    id BIGSERIAL PRIMARY KEY,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT,
    para_bucket VARCHAR(16),
    source_path TEXT NOT NULL,
    content_sha256 CHAR(64) NOT NULL,
    summary TEXT,
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_knowledge_documents_slug ON knowledge_documents(slug);
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_category ON knowledge_documents(category);
