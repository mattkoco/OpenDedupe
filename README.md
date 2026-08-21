# OpenDedupe

```text
  _______                   ______            __                   
 |   _   .-----.-----.-----|   _  \ .-----.--|  .--.--.-----.-----.
 |.  |   |  _  |  -__|     |.  |   \|  -__|  _  |  |  |  _  |  -__|
 |.  |   |   __|_____|__|__|.  |    |_____|_____|_____|   __|_____|
 |:  1   |__|              |:  1    /                 |__|         
 |::.. . |                 |::.. . /                               
 `-------'                 `------'                                
```

![Version](https://img.shields.io/badge/version-v0.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An open-source ticket deduplication and clustering layer for IT help desks.

Most help desk tools do not automatically detect when multiple incoming tickets describe the exact same problem. During an outage, agents are forced to manually find and merge dozens of duplicate tickets under time pressure. OpenDedupe sits alongside your existing help desk to automatically group duplicate tickets into clusters using text embeddings and time proximity.

**Note:** OpenDedupe is not a help desk replacement. It never auto-closes or auto-merges tickets without a human confirming the action on the dashboard first.

## Features

* **Universal Ingestion:** Accepts a standard JSON payload from any help desk system via a single API endpoint.
* **Idempotent Webhooks:** Safely handles duplicate deliveries to prevent bad data.
* **Semantic Clustering:** Uses machine learning (`sentence-transformers`) to understand the actual meaning of a ticket, grouping "Cannot access email" and "Outlook is down" together automatically.
* **Vector Storage:** Uses PostgreSQL and `pgvector` to store tickets and their mathematical text embeddings in the same database.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed and running.
* Python 3.11+ (if you want to run the local test scripts).
* `curl` or an API client (Postman, Insomnia, etc.) for manual testing.

## Quick Start

1. Clone the repository:
   ```bash
   git clone [https://github.com/mattkoco/opendedupe.git](https://github.com/mattkoco/opendedupe.git)
   cd opendedupe
   ```

2. Build and start the API and database containers:
   ```bash
   docker-compose up --build -d
   ```

3. The API will be available at `http://localhost:8000`.

## Testing the Clustering Engine

You can test the machine learning grouping logic by firing a batch of synthetic tickets at the API.

1. Set up a local Python virtual environment and install the required HTTP library:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests
   ```

2. Run the seed script:
   ```bash
   python seed.py
   ```
   This will submit a mix of duplicate and unique issues to the API and output the final grouped clusters.

## Tuning the AI

Every IT environment defines a "duplicate" differently. You can adjust how strictly OpenDedupe groups tickets by changing the similarity threshold.

1. Open `clustering.py`.
2. Locate `SIMILARITY_THRESHOLD = 0.85`.
3. Change this value (closer to `1.0` means it requires an almost exact text match; closer to `0.5` allows for much looser interpretations).
4. Restart your Docker containers to apply the change.

## Changelog

For a more detailed changelog, see [CHANGELOG.md](./CHANGELOG.md).

## License

MIT; see [LICENSE](./LICENSE) for details.