# Transcription UI Proxy Service

This is a proxy service for the transcription UI that handles file uploads and communication with the transcription service.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   NODE_ENV=production
   TRANSCRIPTION_SERVICE_URL=http://transcription-service:3000
   ```

## Running with Docker

To start the services:

```bash
docker-compose up -d
```

This will start:
- The proxy service on port 3003
- The transcription service (as a dependency)

## Development

For local development:

```bash
npm install
npm run dev
```

## API Endpoints

- POST `/upload` - Upload audio files for transcription
- GET `/status/:id` - Check transcription status
- GET `/download/:id` - Download transcribed text

## Volumes

- `./uploads` - Directory for storing uploaded files 