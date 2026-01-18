import os
import sqlite3
import uuid
import hashlib
from datetime import datetime
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

# AI imports
try:
    import google.generativeai as genai
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    AI_ENABLED = True
except ImportError:
    AI_ENABLED = False
    print("⚠️  AI libraries not installed. Install with: pip install google-generativeai numpy scikit-learn")

# Load environment variables
load_dotenv()

# Initialize Gemini AI if API key provided
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if AI_ENABLED and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
    print("✅ Gemini AI enabled")
else:
    gemini_model = None
    print("⚠️  Gemini AI disabled (set GEMINI_API_KEY to enable)")

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
            confidence REAL,
            embedding_hash TEXT,
            similar_reports TEXT
        )
    """)
    conn.commit()
    conn.close()


# AI Enrichment Functions

async def enrich_with_ai(report_data: dict) -> dict:
    """
    Use Gemini AI to analyze and categorize the report.
    Returns enrichment data: summary, category, severity, confidence.
    """
    if not gemini_model:
        return {}
    
    try:
        with sentry_sdk.start_span(op="ai.inference", description="gemini_enrichment"):
            prompt = f"""Analyze this user report and provide:
1. A one-line summary (max 10 words)
2. Category (crash/performance/bug/feature_request/ui_issue)
3. Severity (critical/high/medium/low)
4. Confidence score (0.0-1.0)

Report Type: {report_data['type']}
Message: {report_data['message']}
Platform: {report_data.get('platform', 'unknown')}

Respond in this exact format:
SUMMARY: [summary]
CATEGORY: [category]
SEVERITY: [severity]
CONFIDENCE: [score]"""
            
            response = gemini_model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Parse response
            enrichment = {}
            for line in result_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    enrichment[key] = value
            
            return {
                'summary': enrichment.get('summary', ''),
                'category': enrichment.get('category', ''),
                'severity': enrichment.get('severity', 'medium'),
                'confidence': float(enrichment.get('confidence', '0.5')),
            }
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"AI enrichment failed: {e}")
        return {}


def generate_embedding_hash(text: str) -> str:
    """Generate a hash for similarity detection (simplified version of Yellowcake)"""
    # Simple hash-based similarity - in production use proper embeddings
    normalized = text.lower().strip()
    return hashlib.md5(normalized.encode()).hexdigest()[:16]


async def find_similar_reports(report_data: dict, conn) -> List[str]:
    """
    Find similar reports using Yellowcake-inspired similarity detection.
    Returns list of similar report IDs.
    """
    try:
        with sentry_sdk.start_span(op="similarity.search", description="yellowcake_search"):
            # Generate embedding hash for this report
            embedding_hash = generate_embedding_hash(report_data['message'])
            
            # Find reports with similar hashes or same type
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, message, embedding_hash FROM reports 
                WHERE type = ? 
                ORDER BY created_at DESC 
                LIMIT 50
            """, (report_data['type'],))
            
            existing_reports = cursor.fetchall()
            similar_ids = []
            
            # Simple similarity check
            for report_id, message, existing_hash in existing_reports:
                if existing_hash == embedding_hash:
                    similar_ids.append(report_id)
                elif report_data['message'].lower() in message.lower():
                    similar_ids.append(report_id)
                
                if len(similar_ids) >= 3:  # Max 3 similar reports
                    break
            
            return similar_ids
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return []


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
    ai_enriched: bool = False
    category: Optional[str] = None
    severity: Optional[str] = None
    similar_count: int = 0


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
        
        # Span 2: AI Enrichment (Gemini)
        ai_enrichment = {}
        if gemini_model:
            ai_enrichment = await enrich_with_ai(report.dict())
            transaction.set_tag("ai_enriched", True)
            transaction.set_tag("ai_category", ai_enrichment.get('category', 'unknown'))
        
        # Span 3: Similarity Detection (Yellowcake-inspired)
        conn = sqlite3.connect(DB_NAME)
        similar_reports = await find_similar_reports(report.dict(), conn)
        if similar_reports:
            transaction.set_tag("has_duplicates", True)
            transaction.set_data("similar_count", len(similar_reports))
        
        # Generate embedding hash
        embedding_hash = generate_embedding_hash(report.message)
        
        # Span 4: Store in database
        with sentry_sdk.start_span(op="db.query", description="store_report_db"):
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO reports (
                        id, created_at, type, message, platform, app_version, status,
                        summary, category, severity, confidence, embedding_hash, similar_reports
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    report_id, created_at, report.type, report.message, 
                    report.platform, report.app_version, "received",
                    ai_enrichment.get('summary'),
                    ai_enrichment.get('category'),
                    ai_enrichment.get('severity'),
                    ai_enrichment.get('confidence'),
                    embedding_hash,
                    ','.join(similar_reports) if similar_reports else None
                ))
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
                "ai_enriched": str(bool(ai_enrichment)),
            }
        )
        
        return ReportResponse(
            report_id=report_id,
            status="received",
            ai_enriched=bool(ai_enrichment),
            category=ai_enrichment.get('category'),
            severity=ai_enrichment.get('severity'),
            similar_count=len(similar_reports)
        )


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
