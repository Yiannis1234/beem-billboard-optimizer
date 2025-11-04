# BritMetrics React Front-end

This Vite + React + Tailwind app replaces the original Streamlit UI with a modern single page application. It consumes the new FastAPI backend that exposes the existing BritMetrics business logic and external data sources (weather, traffic, Google Places, Eventbrite, etc.).

## Prerequisites

- Node.js 18+
- Python 3.10+
- BritMetrics repository cloned locally (this directory lives inside it)

## Backend API (FastAPI)

From the repository root:

```bash
# Install Python dependencies (adds fastapi & uvicorn)
pip install -r requirements.txt

# Run the API with auto reload
uvicorn backend.api_server:app --reload
```

The FastAPI server runs on `http://localhost:8000` and exposes:

- `GET /api/campaigns`
- `GET /api/cities`
- `POST /api/predict`
- `GET /api/health`

## Front-end (Vite + React)

```bash
cd frontend-react
npm install
npm run dev
```

The development server runs on `http://localhost:5173` and calls the API at `http://localhost:8000` (override by creating `.env` with `VITE_API_URL`).

### Build for production

```bash
npm run build
```

Static assets land in `frontend-react/dist/` ready to be served by Nginx or any static host. Proxy `/api` to the FastAPI process.

## Environment Variables

Create `frontend-react/.env` if you need to change the API location:

```
VITE_API_URL=http://localhost:8000
```

## Folder Structure

- `src/components` – UI building blocks (select, metrics, section wrapper)
- `src/lib/api.js` – REST client helper
- `src/App.jsx` – Main dashboard layout and data fetching logic
- `backend/api_server.py` – FastAPI server consumed by the React app

## Linting & Formatting

```bash
npm run lint
npm run build
```

Both commands must succeed before deploying. Tailwind classes are fully tree-shaken by the production build.
