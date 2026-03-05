# FinAssistant

A personal financial assistant for portfolio management, news analysis, and market sentiment tracking.

## Tech Stack

- **Backend**: Python, FastAPI, uv, SQLAlchemy
- **Frontend**: Vue 2, Chart.js
- **Database**: SQLite
- **Deployment**: Docker, Kubernetes

## Project Structure

```
finassistant/
├── backend/           # Python FastAPI backend
│   └── app/
│       ├── api/       # API endpoints
│       ├── core/      # Database config
│       ├── models/    # SQLAlchemy models
│       ├── schemas/   # Pydantic schemas
│       └── services/  # Business logic
├── frontend/          # Vue 2 frontend
│   └── src/
│       ├── api/       # API client
│       ├── views/     # Page components
│       ├── router/    # Vue Router
│       └── assets/    # Styles
├── k8s/              # Kubernetes configs
├── docker-compose.yml
└── README.md
```

## Quick Start

### Docker Compose (Recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Manual Setup

#### Backend

```bash
cd backend
uv sync
python -m app.main
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Features

### Portfolio Management
- Create and manage multiple portfolios
- Track accounts across different institutions (banks, brokers)
- Support for 融资融券 (margin trading) positions
- Multi-currency support (CNY, USD, HKD)

### Position Tracking
- Individual asset positions with quantity, cost, current price
- Automatic gain/loss calculation
- Asset allocation visualization (pie chart)
- Historical performance tracking (line chart)

### Import System
- Upload screenshots of portfolio positions
- LLM-powered OCR extraction (vision analysis)
- Review and confirm before import
- Support for 雪球, 同花顺, 招商银行

### API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| Portfolio | `GET/POST /portfolios/` | List/Create portfolios |
| Account | `GET/POST /portfolios/{id}/accounts` | Manage accounts |
| Position | `GET/POST /portfolios/accounts/{id}/positions` | Manage positions |
| Import | `POST /imports/start` | Start import job |
| Import | `POST /imports/{id}/analyze` | Analyze screenshot |
| Import | `POST /imports/{id}/confirm` | Confirm import |
| Upload | `POST /upload/screenshot` | Upload screenshot |
| Prices | `POST /prices/update` | Batch update prices |

## Environment Variables

### Backend
- `DATABASE_URL` - Database connection string (default: sqlite)

### Frontend
- `VUE_APP_API_URL` - Backend API URL

## Deployment

### Docker

```bash
# Build and run
docker-compose up --build

# Or individual services
docker build -t finassistant-backend ./backend
docker build -t finassistant-frontend ./frontend
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

## Development

### Running Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

### Linting

```bash
# Backend
cd backend && ruff check .

# Frontend
cd frontend && npm run lint
```

## License

MIT
