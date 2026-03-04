# Agent Instructions

## Development Commands

### Backend
- Install: `cd backend && uv sync`
- Run: `cd backend && python -m app.main`
- Format: `cd backend && black .`
- Type check: `cd backend && mypy .`

### Frontend
- Install: `cd frontend && npm install`
- Run: `cd frontend && npm run dev`
- Build: `cd frontend && npm run build`

## Testing
- Backend tests: `cd backend && pytest`
- Frontend tests: `cd frontend && npm test`

## Linting
- Python: `ruff check backend/`
- JavaScript: `cd frontend && npm run lint`
