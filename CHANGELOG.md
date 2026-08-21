# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-21

### Added
* Machine learning embedding pipeline using `sentence-transformers` and the `all-MiniLM-L6-v2` model to generate dense text vectors.
* Cosine similarity clustering engine in `clustering.py` to automatically group incoming tickets with a tunable threshold.
* `GET /clusters` endpoint to view deduplicated groups and their associated tickets.
* `seed.py` demo script to simulate IT support traffic and validate the end-to-end clustering logic.

### Changed
* Swapped the standard PostgreSQL Docker image for `pgvector/pgvector:pg15` to natively support vector math.
* Updated `models.py` schema to store 384-dimensional arrays using the `VECTOR` data type.
* Modified the `POST /tickets` endpoint to route data through the embedding and clustering pipeline before saving.

## [0.1.0] - 2026-08-20

### Added
* Initial project structure and Docker Compose orchestration for FastAPI and PostgreSQL with `pgvector`.
* Universal ingestion endpoint `POST /tickets` to accept standard JSON payloads from any external help desk.
* SQLAlchemy models (`Ticket` and `Cluster`) mapping to the minimum viable data schema.
* Database-level and API-level idempotency checks on `external_id` and `source_system` to safely handle duplicate webhook deliveries.
* `GET /version` endpoint to expose the current API release tag.