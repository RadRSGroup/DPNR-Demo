# DPNR Project

This project uses Docker Compose to manage multiple services including a main application, database, cache, and monitoring stack.

## Services

- Main Application (Port 3000)
- PostgreSQL Database (Port 5432)
- Redis Cache (Port 6379)
- Whisper ASR Service (Port 9000)
- Prometheus Monitoring (Port 9090)
- Grafana Dashboard (Port 3002)
- Redis Exporter (Port 9121)
- PostgreSQL Exporter (Port 9187)

## Setup

1. Build the application:
```bash
docker-compose build
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access services:
- Main App: http://localhost:3000
- Grafana: http://localhost:3002
- Prometheus: http://localhost:9090

## Development

- The main application code is in the `app` directory
- Database migrations are in `app/migrations`
- Configuration files are in their respective service directories 