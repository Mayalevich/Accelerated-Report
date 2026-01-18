# Accelerated Report App - Project Story

## Inspiration 💡

Bug reporting is painfully slow. Complex forms make users give up, and QA teams waste hours categorizing reports. We asked: **"What if submitting a bug was as easy as pressing a button?"**

We combined **Sentry's error tracking** with **Gemini AI vision** to create a one-tap bug reporting system that auto-captures screenshots, analyzes context, and finds solutions.

## What it does 🚀

**Accelerated Report App** makes bug reporting instant:

- **One-Tap Buttons**: Crash, Slow, Bug, Suggestion - 80% faster than forms
- **Auto Screenshot Capture**: Uses DisplayMediaCapture API to grab screen automatically
- **AI Vision Analysis**: Gemini analyzes screenshots + context, provides professional QA insights
- **Smart Resources**: Auto-generates Stack Overflow searches, docs, GitHub links
- **Full Sentry Integration**: Triggers real exceptions for automatic grouping
- **Offline-First**: Queue reports when offline, auto-retry

## How we built it 🔧

- **Backend**: FastAPI + Python, Gemini 2.5-flash for vision, Sentry SDK, SQLite
- **Frontend**: Vanilla JS, DisplayMediaCapture for screenshots, offline queue
- **AI Pipeline**: Professional QA analyst prompt with structured output (category, severity, action plan, confidence)
- **6-Span Transaction**: Validation → AI Analysis → Resource Finding → Sentry Grouping → Similarity Check → Storage

## Challenges we ran into 😅

1. **Model Hunt**: Tried 4 Gemini model names before finding `gemini-2.5-flash` worked
2. **Screenshot Integration**: Needed base64 encoding, proper MIME handling, fallback for unsupported browsers
3. **Database Evolution**: Added columns as features grew, learned to convert sqlite3.Row to dict
4. **Yellowcake API**: 404 errors led us to build our own contextual link generator (actually better!)
5. **Prompt Consistency**: Early AI responses varied wildly - solved with strict format templates

## Accomplishments that we're proud of ✨

- **80% faster reporting** - one tap vs multi-field forms
- **Vision-powered analysis** - Gemini extracts context from screenshots automatically
- **Zero API dependencies** for resources - instant contextual links
- **Professional QA output** - standardized, formal analysis every time
- **Real Sentry integration** - triggers actual exceptions for proper grouping

## What we learned 🎓

- AI prompt engineering is critical - clear roles, strict formats, examples
- User experience > features - simplified complex form to 4 buttons
- Vision models are powerful - screenshots boost AI confidence significantly
- Offline-first matters - users report bugs when things break (often offline)
- Keep docs minimal - started with 12 markdown files, cleaned to 4 essential ones

## What's next for Accelerated Report App 🚀

- **Real-time collaboration** - let developers ask AI follow-up questions
- **Trend analysis** - ML clustering for bug patterns, predict critical bugs
- **Multi-modal AI** - analyze videos, voice descriptions, gesture replay
- **Smart prioritization** - ML-based severity prediction and auto-assignment

---

**Built with FastAPI • Gemini AI • Sentry SDK • SQLite • Vanilla JS**
