# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-20

### Added
* Initial project structure and Docker Compose orchestration for FastAPI and PostgreSQL with `pgvector`[cite: 1].
* Universal ingestion endpoint `POST /tickets` to accept standard JSON payloads from any external help desk[cite: 1].
* SQLAlchemy models (`Ticket` and `Cluster`) mapping to the minimum viable data schema[cite: 1].
* Database-level and API-level idempotency checks on `external_id` and `source_system` to safely handle duplicate webhook deliveries[cite: 1].
* `GET /version` endpoint to expose the current API release tag[cite: 1].
