# Core Persona Development Environment

This is the development environment for the Core Persona assessment platform. It provides a containerized development setup with live reloading and testing capabilities.

## Prerequisites

- Docker
- Docker Compose
- Node.js (for local development, optional)

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd core-persona
```

2. Start the development environment:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

3. Access the application:
- Open http://localhost:3000 in your browser
- The application will automatically reload when you make changes to the frontend files

## Development Workflow

1. Make changes to the frontend files in the `frontend` directory
2. Changes will be automatically reflected in the browser
3. Use the following commands for additional development tasks:

```bash
# Run tests
docker-compose -f docker-compose.dev.yml run app npm test

# Lint code
docker-compose -f docker-compose.dev.yml run app npm run lint

# Format code
docker-compose -f docker-compose.dev.yml run app npm run format
```

## Testing the Text Input Changes

To test the new text input functionality:

1. Start the development environment
2. Navigate through the assessment
3. When you reach the text input phase, verify:
   - Text areas render correctly
   - Character limits are enforced
   - Required field validation works
   - Responses are properly collected and stored
   - UI transitions work smoothly

## Troubleshooting

If you encounter issues:

1. Check the container logs:
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

2. Restart the development environment:
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up --build
```

3. Clear Docker cache if needed:
```bash
docker-compose -f docker-compose.dev.yml down -v
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly in the development environment
4. Submit a pull request

## License

[Your License Here] 