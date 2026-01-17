# Backend - Accelerated Report API

This is the FastAPI backend for the Accelerated Report App.

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment:**
   
   macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```
   
   Windows:
   ```powershell
   .\.venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Sentry:**
   
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Sentry DSN:
   ```env
   SENTRY_DSN=your_actual_sentry_dsn_here
   ```

## Run

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### GET /
Health check

### GET /health
Health check endpoint

### GET /boom
Test endpoint that triggers an error (for testing Sentry)

### POST /reports
Create a new report

**Request:**
```json
{
  "type": "crash",
  "message": "App crashes when clicking submit button",
  "platform": "web",
  "app_version": "1.0.0"
}
```

**Response:**
```json
{
  "report_id": "uuid-here",
  "status": "received"
}
```

### GET /reports
Get all reports

## Sentry Integration

The backend is fully instrumented with Sentry:

- **Critical Experience:** `critical.report_submit` transaction
- **Spans:** `validate_input`, `store_report_db`, `ai_enrich` (future)
- **Metrics:** `reports.submitted`, `reports.failed`
- **Tags:** `critical_experience`, `report_type`, `platform`
- **Error Tracking:** All exceptions captured with context

## Person 1 (Backend + Sentry) Tasks

✅ Initial Setup (MUST DO FIRST):
1. Create Sentry project at sentry.io
2. Copy DSN and add to `.env`
3. Set up virtual environment
4. Install dependencies
5. Run server and test `/boom` endpoint in Sentry

✅ Core Features:
1. POST /reports endpoint with Sentry transaction
2. SQLite database setup
3. GET /reports endpoint
4. Critical experience instrumentation
5. Metrics tracking

⏳ Advanced Features (Later):
1. Chaos mode support (optional delay/errors)
2. AI enrichment span (when Person 3 is ready)
3. Auto-protect degraded mode
4. Queue metrics

## Testing Sentry

1. Start the server
2. Visit: `http://localhost:8000/boom`
3. Check Sentry dashboard - you should see the error
4. Submit a report via POST /reports
5. Check Sentry Performance - you should see the `critical.report_submit` transaction
