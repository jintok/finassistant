# FinAssistant

A personal financial assistant for portfolio management, news analysis, and market sentiment tracking.

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, Vite
- **Database**: SQLite (configurable)

## Project Structure

```
finassistant/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Core functionality
│   │   ├── models/    # Data models
│   │   └── services/  # Business logic
│   └── requirements.txt
├── frontend/          # React frontend
│   └── src/
├── data/              # Local data storage
├── notebooks/         # Jupyter notebooks
└── tests/             # Test files
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
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
