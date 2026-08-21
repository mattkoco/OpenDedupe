from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import models
from embeddings import get_embedding
from clustering import find_best_cluster
from pydantic import BaseModel
import os
import uuid
from datetime import datetime, timezone

# --- Database Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/opendedupe")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Enable pgvector and create tables
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OpenDedupe API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Schemas (Updated for your DB) ---
class TicketCreate(BaseModel):
    subject: str
    body: str

# --- Endpoints ---
@app.post("/tickets")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # 1. Embed subject and body
    text_to_embed = f"{ticket.subject}. {ticket.body}"
    vector = get_embedding(text_to_embed)

    # 2. Fetch existing tickets
    existing_tickets = db.query(models.Ticket).all()

    # 3. Find match
    matched_cluster_id = find_best_cluster(vector, existing_tickets)

    # 4. Create cluster if no match
    if not matched_cluster_id:
        new_cluster = models.Cluster()
        db.add(new_cluster)
        db.commit()
        db.refresh(new_cluster)
        matched_cluster_id = new_cluster.id

    # 5. Save the ticket with ALL your required fields
    db_ticket = models.Ticket(
        external_id=str(uuid.uuid4()), # Mocking an external ticketing system ID
        source_system="demo_script",
        subject=ticket.subject,
        body=ticket.body,
        reporter="test_user@domain.com",
        reported_at=datetime.now(timezone.utc),
        ingested_at=datetime.now(timezone.utc),
        manually_split=False,
        embedding=vector,
        cluster_id=matched_cluster_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return {"id": db_ticket.id, "subject": db_ticket.subject, "cluster_id": db_ticket.cluster_id}

@app.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    clusters = db.query(models.Cluster).all()
    result = []
    for c in clusters:
        result.append({
            "cluster_id": c.id,
            "ticket_count": len(c.tickets),
            "tickets": [{"id": t.id, "subject": t.subject} for t in c.tickets]
        })
    return result

@app.get("/version")
def get_version():
    return {"version": "0.2.0"}