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
    # Add data like request headers and IP for users
    send_default_pii=True,
)

# Print Sentry status
if os.getenv("SENTRY_DSN"):
    print("✅ Sentry monitoring enabled")
else:
    print("⚠️  Sentry monitoring disabled (set SENTRY_DSN to enable)")

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
            description TEXT,
            category TEXT,
            severity TEXT,
            developer_action TEXT,
            confidence REAL,
            similar_reports TEXT,
            sentry_event_id TEXT
        )
    """)
    conn.commit()
    conn.close()


# AI Enrichment Functions

async def enrich_with_gemini(report_data: dict) -> dict:
    """
    Use Gemini AI to help user communicate problem better and help developer understand faster.
    
    For USER: Expands minimal input into detailed context
    For DEVELOPER: Categorizes, prioritizes, and suggests solutions
    """
    if not gemini_model:
        return {}
    
    try:
        with sentry_sdk.start_span(op="ai.inference", description="gemini_enrichment"):
            # Enhanced prompt to help both user and developer
            prompt = f"""You are helping with bug reporting. The user submitted a quick report.

USER INPUT:
- Type: {report_data['type']}
- Message: "{report_data['message']}"
- Platform: {report_data.get('platform', 'unknown')}

YOUR TASK:
1. Expand the user's message into a clear problem description (2-3 sentences)
2. Categorize: crash/performance/bug/feature_request/ui_issue/network
3. Assess severity: critical/high/medium/low
4. Suggest what the developer should check first (1 sentence)
5. Give confidence score (0.0-1.0)

Respond in this exact format:
DESCRIPTION: [expanded description]
CATEGORY: [category]
SEVERITY: [severity]
DEVELOPER_ACTION: [what to check]
CONFIDENCE: [score]"""
            
            response = gemini_model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Parse response
            enrichment = {}
            for line in result_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    enrichment[key] = value
            
            # Add to Sentry context for better issue grouping
            sentry_sdk.set_context("ai_analysis", {
                "description": enrichment.get('description', ''),
                "category": enrichment.get('category', ''),
                "severity": enrichment.get('severity', 'medium'),
                "developer_action": enrichment.get('developer_action', ''),
                "confidence": enrichment.get('confidence', '0.5'),
            })
            
            return {
                'description': enrichment.get('description', report_data['message']),
                'category': enrichment.get('category', 'unknown'),
                'severity': enrichment.get('severity', 'medium'),
                'developer_action': enrichment.get('developer_action', 'Investigate issue'),
                'confidence': float(enrichment.get('confidence', '0.5')),
            }
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"Gemini AI enrichment failed: {e}")
        return {}


async def send_to_sentry_for_grouping(report_data: dict, ai_enrichment: dict):
    """
    Send report to Sentry so Yellowcake can group similar issues automatically.
    
    Yellowcake (Sentry's similarity engine) will:
    - Group similar errors together
    - Detect duplicate issues
    - Show related problems in dashboard
    """
    try:
        # Create a custom exception with enriched context
        with sentry_sdk.push_scope() as scope:
            # Add all context for Yellowcake to analyze
            scope.set_tag("report_type", report_data['type'])
            scope.set_tag("platform", report_data.get('platform', 'unknown'))
            scope.set_tag("ai_category", ai_enrichment.get('category', 'unknown'))
            scope.set_tag("severity", ai_enrichment.get('severity', 'medium'))
            
            # Add user context
            scope.set_context("report", {
                "original_message": report_data['message'],
                "ai_description": ai_enrichment.get('description', ''),
                "developer_action": ai_enrichment.get('developer_action', ''),
                "app_version": report_data.get('app_version', '1.0.0'),
            })
            
            # Set fingerprint for Yellowcake grouping
            # Reports with same type and similar AI category will be grouped
            scope.fingerprint = [
                report_data['type'],
                ai_enrichment.get('category', 'unknown'),
                report_data.get('platform', 'unknown')
            ]
            
            # Capture as message (not error) for user reports
            sentry_sdk.capture_message(
                f"User Report: {ai_enrichment.get('description', report_data['message'])}",
                level=ai_enrichment.get('severity', 'info')
            )
            
    except Exception as e:
        print(f"Failed to send to Sentry: {e}")


async def find_similar_reports(report_data: dict, conn) -> List[str]:
    """
    Find similar reports in local database by category and type.
    Note: Sentry's Yellowcake does the real similarity detection in the dashboard.
    """
    try:
        with sentry_sdk.start_span(op="db.query", description="find_similar_local"):
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, message, category FROM reports 
                WHERE type = ? AND category IS NOT NULL
                ORDER BY created_at DESC 
                LIMIT 10
            """, (report_data['type'],))
            
            existing_reports = cursor.fetchall()
            similar_ids = []
            
            # Simple keyword matching (real similarity is in Sentry's Yellowcake)
            for report_id, message, category in existing_reports:
                if category == report_data.get('category'):
                    similar_ids.append(report_id)
                
                if len(similar_ids) >= 3:
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


@app.get("/sentry-debug")
async def sentry_debug():
    """Official Sentry verification endpoint"""
    division_by_zero = 1 / 0
    return {"status": "This should never return"}


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
        
        # Span 2: AI Enrichment with Gemini (helps user communicate better)
        ai_enrichment = {}
        if gemini_model:
            ai_enrichment = await enrich_with_gemini(report.dict())
            transaction.set_tag("ai_enriched", True)
            transaction.set_tag("ai_category", ai_enrichment.get('category', 'unknown'))
            transaction.set_tag("ai_severity", ai_enrichment.get('severity', 'medium'))
        
        # Span 3: Send to Sentry for Yellowcake grouping
        await send_to_sentry_for_grouping(report.dict(), ai_enrichment)
        
        # Span 4: Find similar reports in local DB
        conn = sqlite3.connect(DB_NAME)
        similar_reports = await find_similar_reports({**report.dict(), **ai_enrichment}, conn)
        if similar_reports:
            transaction.set_tag("has_local_duplicates", True)
            transaction.set_data("similar_count", len(similar_reports))
        
        # Span 5: Store in database
        with sentry_sdk.start_span(op="db.query", description="store_report_db"):
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO reports (
                        id, created_at, type, message, platform, app_version, status,
                        description, category, severity, developer_action, confidence, similar_reports
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    report_id, created_at, report.type, report.message, 
                    report.platform, report.app_version, "received",
                    ai_enrichment.get('description'),
                    ai_enrichment.get('category'),
                    ai_enrichment.get('severity'),
                    ai_enrichment.get('developer_action'),
                    ai_enrichment.get('confidence'),
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
                "description": row.get("description"),
                "category": row.get("category"),
                "severity": row.get("severity"),
                "developer_action": row.get("developer_action"),
                "confidence": row.get("confidence"),
                "similar_reports": row.get("similar_reports"),
            })
        
        return {"reports": reports, "count": len(reports)}
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve reports")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
