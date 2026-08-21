from datetime import datetime, timezone
import os
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Ticket

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgrespassword@localhost:5432/opendedupe")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="OpenDedupe API", version="0.1.0", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TicketIngestSchema(BaseModel):
    external_id: str
    source_system: str
    subject: str
    body: str
    reporter: str
    system_tag: Optional[str] = None
    reported_at: datetime


class TicketResponseSchema(BaseModel):
    id: int
    external_id: str
    source_system: str
    subject: str
    reported_at: datetime
    ingested_at: datetime
    status: str

    class Config:
        from_attributes = True


@app.post("/tickets", response_model=TicketResponseSchema, status_code=status.HTTP_201_CREATED)
def ingest_ticket(ticket_in: TicketIngestSchema, db: Session = Depends(get_db)):
    existing_ticket = (
        db.query(Ticket)
        .filter(
            Ticket.external_id == ticket_in.external_id,
            Ticket.source_system == ticket_in.source_system,
        )
        .first()
    )

    if existing_ticket:
        return TicketResponseSchema(
            id=existing_ticket.id,
            external_id=existing_ticket.external_id,
            source_system=existing_ticket.source_system,
            subject=existing_ticket.subject,
            reported_at=existing_ticket.reported_at,
            ingested_at=existing_ticket.ingested_at,
            status="already_ingested",
        )

    new_ticket = Ticket(
        external_id=ticket_in.external_id,
        source_system=ticket_in.source_system,
        subject=ticket_in.subject,
        body=ticket_in.body,
        reporter=ticket_in.reporter,
        system_tag=ticket_in.system_tag,
        reported_at=ticket_in.reported_at,
        ingested_at=datetime.now(timezone.utc),
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return TicketResponseSchema(
        id=new_ticket.id,
        external_id=new_ticket.external_id,
        source_system=new_ticket.source_system,
        subject=new_ticket.subject,
        reported_at=new_ticket.reported_at,
        ingested_at=new_ticket.ingested_at,
        status="ingested",
    )


@app.get("/version")
def get_version():
    return {"version": "v0.1.0"}