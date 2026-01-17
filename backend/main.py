import os
import sqlite3
import uuid
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

# Load environment variables
load_dotenv()

# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=float(os.getenv("TRACES_SAMPLE_RATE", "1.0")),
    environment=os.getenv("ENVIRONMENT", "dev"),
    integrations=[
        FastApiIntegration(),
    ],
    # Enable performance monitoring
    enable_tracing=True,
)

# Database setup
DB_NAME = "reports.db"


def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            platform TEXT,
            app_version TEXT,
            status TEXT DEFAULT 'received',
            summary TEXT,
            category TEXT,
            severity TEXT,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed


# Create FastAPI app
app = FastAPI(
    title="Accelerated Report API",
    description="Fast, reliable in-app reporting with Sentry monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ReportCreate(BaseModel):
    type: str  # crash | slow | bug | suggestion
    message: str
    platform: Optional[str] = "web"
    app_version: Optional[str] = "1.0.0"


class ReportResponse(BaseModel):
    report_id: str
    status: str


class Report(BaseModel):
    id: str
    created_at: str
    type: str
    message: str
    platform: Optional[str]
    app_version: Optional[str]
    status: str
    summary: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    confidence: Optional[float] = None


# Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "Accelerated Report API"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/boom")
async def boom():
    """Test endpoint to trigger a Sentry error"""
    # This is intentional for testing Sentry
    raise Exception("💥 Boom! This is a test error for Sentry.")


@app.post("/reports", response_model=ReportResponse)
async def create_report(report: ReportCreate):
    """
    Create a new report.
    This is the CRITICAL EXPERIENCE that must succeed.
    """
    # Start Sentry transaction for critical experience
    with sentry_sdk.start_transaction(
        op="critical.experience",
        name="critical.report_submit"
    ) as transaction:
        
        # Add tags for better filtering in Sentry
        transaction.set_tag("critical_experience", "report_submit")
        transaction.set_tag("report_type", report.type)
        transaction.set_tag("platform", report.platform)
        
        # Add breadcrumb
        sentry_sdk.add_breadcrumb(
            category="report",
            message=f"Submitting {report.type} report",
            level="info",
        )
        
        # Span 1: Validate input
        with sentry_sdk.start_span(op="validate", description="validate_input"):
            if not report.message or len(report.message) < 3:
                raise HTTPException(status_code=400, detail="Message must be at least 3 characters")
            
            valid_types = ["crash", "slow", "bug", "suggestion"]
            if report.type not in valid_types:
                raise HTTPException(status_code=400, detail=f"Type must be one of: {valid_types}")
        
        # Generate report ID
        report_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        # Span 2: Store in database
        with sentry_sdk.start_span(op="db.query", description="store_report_db"):
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO reports (id, created_at, type, message, platform, app_version, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (report_id, created_at, report.type, report.message, report.platform, report.app_version, "received"))
                conn.commit()
                conn.close()
            except Exception as e:
                sentry_sdk.capture_exception(e)
                raise HTTPException(status_code=500, detail="Failed to store report")
        
        # Track metric: report submitted successfully
        sentry_sdk.metrics.incr(
            "reports.submitted",
            tags={
                "type": report.type,
                "platform": report.platform,
            }
        )
        
        return ReportResponse(report_id=report_id, status="received")


@app.get("/reports")
async def list_reports():
    """Get all reports"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports ORDER BY created_at DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in rows:
            reports.append({
                "id": row["id"],
                "created_at": row["created_at"],
                "type": row["type"],
                "message": row["message"],
                "platform": row["platform"],
                "app_version": row["app_version"],
                "status": row["status"],
                "summary": row["summary"],
                "category": row["category"],
                "severity": row["severity"],
                "confidence": row["confidence"],
            })
        
        return {"reports": reports, "count": len(reports)}
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve reports")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
