# FinAssistant

A personal financial assistant for portfolio management, news analysis, and market sentiment tracking.

## Tech Stack

- **Backend**: Python, FastAPI, uv
- **Frontend**: Vue 2
- **Database**: SQLite (configurable)

## Project Structure

```
finassistant/
├── backend/           # Python FastAPI backend
│   └── app/
│       ├── api/       # API endpoints
│       ├── core/      # Core functionality
│       ├── models/    # Data models
│       └── services/  # Business logic
├── frontend/          # Vue 2 frontend
│   └── src/
│       ├── components/
│       ├── views/
│       ├── router/
│       └── assets/
├── data/              # Local data storage
├── notebooks/         # Jupyter notebooks
└── tests/             # Test files
```

## Setup

### Backend

```bash
cd backend
uv sync
python -m app.main
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Features

- Portfolio management
- News collection and analysis
- Market sentiment tracking
