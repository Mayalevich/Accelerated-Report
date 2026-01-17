<div align="center">

# ⚡ Accelerated Report App

### *Fast, Reliable In-App Reporting with Sentry Observability*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Sentry](https://img.shields.io/badge/Sentry-Enabled-purple.svg)](https://sentry.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**🏆 Built for Hackathon | Best Use of Sentry**

[Demo](#-demo) • [Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

---

### 📹 Demo

*Submit bug reports in under 10 seconds • Never lose a report • Full observability with Sentry*

![Report Form](https://via.placeholder.com/800x400/6366f1/ffffff?text=Fast+Report+Submission)

</div>

---

## 🎯 The Problem

**Users don't report bugs anymore because:**
- 😫 Traditional reporting takes too long
- 🤔 Users don't know what details to include  
- 😡 Submissions fail silently with no feedback

**Result:** Developers miss critical issues and can't reproduce bugs

---

## 💡 Our Solution

**Accelerated Report App** makes reporting effortless:

- ⚡ **10-Second Submission** - One dropdown + one text field = done
- 🔒 **Never Lose Reports** - Offline queue with automatic retry
- 📊 **Full Observability** - Sentry monitors every critical experience
- 🧠 **Smart Enrichment** - Optional AI categorization & similarity detection
- 🎪 **Demo-Ready** - Chaos Mode proves reliability under failure

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🚀 User Experience
- ⚡ **Lightning Fast** - Submit in 10 seconds
- � **Works Offline** - Queue + auto-retry
- ✅ **Always Confirms** - Never fails silently
- 🎯 **One-Click Reporting** - Minimal friction

</td>
<td width="50%">

### 🔍 Observability
- 📊 **Critical Experience Monitoring**
- 🔎 **Full Request Tracing** with spans
- 📈 **Custom Metrics** (latency, failures)
- 🐛 **Error Tracking** with context
- 🤖 **Seer AI** debugging suggestions

</td>
</tr>
</table>

---

## 🎯 Why Sentry Is Core

<div align="center">

**This project demonstrates Sentry as an observability engine, not just error logging**

</div>

| Sentry Feature | How We Use It | Impact |
|----------------|---------------|--------|
| **Transactions** | `critical.report_submit` tracks every submission | Full visibility into user experience |
| **Spans** | `validate_input`, `store_db`, `ai_enrich` | Pinpoint performance bottlenecks |
| **Metrics** | `reports.submitted`, `reports.failed`, `latency_ms` | Data-driven reliability decisions |
| **Error Tracking** | Capture with tags, breadcrumbs, context | Faster debugging with full context |
| **Seer AI** | Suggest fixes using connected telemetry | AI-powered debugging |

**Result:** We monitor critical experiences end-to-end, detect issues before users complain, and ensure reports never fail silently.

## 🧠 Architecture

```
Demo Web Page
     |
     v
FastAPI Backend
     |
     ├── SQLite (store reports)
     ├── AI enrichment (Gemini)
     ├── Similarity search (Yellowcake)
     |
     v
Sentry (errors • traces • metrics)
```

## 🖥️ Demo

- Web page simulates in-app "Report a problem"
- Developer dashboard shows submitted reports
- Chaos Mode simulates network and service failures
- Sentry dashboard shows traces, errors, and metrics live

## 🛠 Tech Stack

**Backend**
- Python
- FastAPI
- SQLite
- Sentry SDK

**Frontend**
- HTML / CSS / JavaScript
- Fetch API
- LocalStorage (offline queue)

**Observability**
- Sentry (Errors, Performance, Metrics, Tracing)

---

## 🚀 Quick Start

### One-Command Startup ⚡

```bash
# Clone the repository
git clone https://github.com/Mayalevich/Accelerated-Report.git
cd Accelerated-Report

# Start everything (both backend and frontend)
./start.sh
```

That's it! The script will:
- ✅ Install dependencies (first time only)
- ✅ Start backend on http://localhost:8000
- ✅ Start frontend on http://localhost:3000
- ✅ Open browser automatically

**Stop servers:**
```bash
./stop.sh
```

### Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### 1. Setup Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Sentry DSN
uvicorn main:app --reload
```

#### 2. Setup Frontend
```bash
cd frontend
python3 -m http.server 3000
# Or just open index.html in your browser
```

#### 3. Visit
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:3000/dashboard.html

</details>

## 🔐 Environment Variables

Create `backend/.env`:

```env
SENTRY_DSN=your_sentry_dsn_here
ENVIRONMENT=dev
TRACES_SAMPLE_RATE=1.0
```

⚠️ **Do not commit real secrets.**

## 🎯 Hackathon Goal

To show how Sentry can be used to monitor **critical user experiences**, not just collect logs, and how observability can directly improve reliability and user trust.

## 👥 Team

Built by a 3-person team for a hackathon project.

### Team Division

**Person 1 - Backend + Sentry** (Most Important)
- FastAPI setup
- Sentry integration (traces, metrics, errors)
- Critical experience monitoring
- Database (SQLite)
- API endpoints

**Person 2 - Frontend + UX**
- Report submission form
- Offline queue with localStorage
- Chaos Mode toggle
- Developer dashboard
- Clean, fast UI

**Person 3 - Intelligence**
- Gemini API integration
- Yellowcake similarity search
- Confidence scoring
- Enrichment logic
- AI error handling

## 📋 API Contract

### POST /reports
```json
{
  "type": "crash | slow | bug | suggestion",
  "message": "string",
  "platform": "web | ios | android",
  "app_version": "string"
}
```

Response:
```json
{
  "report_id": "string",
  "status": "received"
}
```

### GET /reports
Returns list of all reports with enrichment data.

---

## 🎬 60-Second Demo

<table>
<tr>
<td width="33%">

**1. Fast Submission** ⚡
- Show form
- Submit in 10 seconds
- "✅ Sent"

</td>
<td width="33%">

**2. Sentry Monitoring** 📊
- Open Performance
- Show `critical.report_submit`
- Show spans breakdown

</td>
<td width="33%">

**3. Chaos Mode** 🎪
- Toggle ON
- Submit 3 reports
- Show queue + retry
- Prove reliability

</td>
</tr>
</table>

**Closing Line:** *"We monitor critical experiences end-to-end, not just log errors"*

## 📚 Documentation

See `/docs` folder for:
- Architecture diagram
- Demo script
- Team roles and responsibilities

## 📄 License

MIT
