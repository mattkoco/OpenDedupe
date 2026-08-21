from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, index=True)
    representative_ticket_id = Column(Integer, nullable=True)
    ticket_count = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default="open", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    tickets = relationship("Ticket", back_populates="cluster")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=False)
    source_system = Column(String(100), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    reporter = Column(String(255), nullable=False)
    system_tag = Column(String(100), nullable=True)
    
    reported_at = Column(DateTime(timezone=True), nullable=False)
    ingested_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    embedding = Column(Vector(384), nullable=True)
    
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=True)
    manually_split = Column(Boolean, default=False, nullable=False)

    cluster = relationship("Cluster", back_populates="tickets")

    __table_args__ = (
        UniqueConstraint("external_id", "source_system", name="uq_external_source"),
    )