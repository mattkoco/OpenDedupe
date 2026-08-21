# OpenDedupe
```
  _______                   ______            __                   
 |   _   .-----.-----.-----|   _  \ .-----.--|  .--.--.-----.-----.
 |.  |   |  _  |  -__|     |.  |   \|  -__|  _  |  |  |  _  |  -__|
 |.  |   |   __|_____|__|__|.  |    |_____|_____|_____|   __|_____|
 |:  1   |__|              |:  1    /                 |__|         
 |::.. . |                 |::.. . /                               
 `-------'                 `------'                                
```
![Version](https://img.shields.io/badge/version-v0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An open source ticket deduplication and clustering layer for IT help desks.

Most help desk tools do not automatically detect when multiple incoming tickets describe the exact same problem. During an outage, agents are forced to manually find and merge dozens of duplicate tickets under time pressure. OpenDedupe sits alongside your existing help desk to automatically group duplicate tickets into clusters using text embeddings and time proximity.

**Note:** OpenDedupe is not a help desk replacement. It never auto closes or auto merges tickets without a human confirming the action on the dashboard first.

## Features

* **Universal Ingestion:** Accepts a standard JSON payload from any help desk system via a single API endpoint.
* **Idempotent Webhooks:** Safely handles duplicate deliveries to prevent bad data.
* **Vector Storage:** Uses PostgreSQL and `pgvector` to store tickets and their mathematical text embeddings in the same database.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed and running
* `curl` or an API client (Postman, Insomnia, etc.) if you want to test the endpoint manually

## Quick Start

1. Clone the repository:
       git clone https://github.com/mattkoco/opendedupe.git
       cd opendedupe

2. Make sure Docker is running on your machine.

3. Build and start the API and database containers:
       docker-compose up --build -d

4. The API will be available at `http://localhost:8000`.

5. Test it by sending a sample ticket:
       curl -X POST http://localhost:8000/tickets \
         -H "Content-Type: application/json" \
         -d '{
               "external_id": "1001",
               "subject": "VPN not connecting",
               "body": "Cannot connect to VPN from home",
               "reporter": "jdoe",
               "reported_at": "2026-08-20T10:00:00Z"
             }'

   Sending the same request twice should not create a duplicate record, which is the idempotency check working.

## Changelog

For a more detailed changelog, see [CHANGELOG.md](./CHANGELOG.md).

## License

MIT; see [LICENSE](./LICENSE) for details.
