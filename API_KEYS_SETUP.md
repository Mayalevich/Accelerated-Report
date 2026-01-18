# 🔑 API Keys Setup Guide

## 📍 File Location

**Edit this file:**
```
backend/.env
```

---

## 🔐 API Keys You Need

### 1. **Sentry DSN** (Required for monitoring)

**Where to get it:**
1. Go to [sentry.io](https://sentry.io)
2. Create a new project (or use existing)
3. Go to **Settings** → **Projects** → **[Your Project]** → **Client Keys (DSN)**
4. Copy the DSN

**Add to `.env`:**
```bash
SENTRY_DSN=https://abc123@o123456.ingest.sentry.io/7890123
```

---

### 2. **Gemini API Key** (Optional - for AI enrichment)

**Where to get it:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

**Add to `.env`:**
```bash
GEMINI_API_KEY=AIzaSyABC123def456GHI789jkl012MNO345pqr
```

> **Note:** AI enrichment is optional. The app works without it, but you won't get:
> - Auto-categorization
> - Severity detection
> - AI-generated summaries

---

## 📝 Complete `.env` File Example

Open `backend/.env` and it should look like this:

```bash
# Sentry Configuration
SENTRY_DSN=https://abc123@o123456.ingest.sentry.io/7890123
ENVIRONMENT=dev
TRACES_SAMPLE_RATE=1.0

# Optional: Enable AI enrichment with Gemini
GEMINI_API_KEY=AIzaSyABC123def456GHI789jkl012MNO345pqr
```

---

## 🚀 After Adding Keys

### Restart the servers:

```bash
./stop.sh
./start.sh
```

### Verify Sentry is working:

1. Visit: http://localhost:3000
2. Submit a test report
3. Check your Sentry dashboard - you should see:
   - Transaction: `critical.report_submit`
   - Tags, spans, metrics

### Verify Gemini is working:

Check the backend logs:
```bash
tail -f backend.log
```

You should see:
```
✅ Gemini AI enabled
```

If you see:
```
⚠️  Gemini AI disabled (set GEMINI_API_KEY to enable)
```

Then the API key is missing or invalid.

---

## 🆓 Free Tiers

### Sentry
- Free tier: 5,000 events/month
- Perfect for hackathon/demo
- [Sign up](https://sentry.io/signup/)

### Gemini
- Free tier: 60 requests/minute
- Perfect for demo
- [Get API key](https://makersuite.google.com/app/apikey)

---

## 🧪 Test Without API Keys

You can still test the app without any keys:

```bash
# Keep SENTRY_DSN empty
SENTRY_DSN=

# App still works, but:
# ❌ No Sentry monitoring
# ❌ No AI enrichment
# ✅ Reports still save to database
# ✅ Offline queue still works
# ✅ UI fully functional
```

---

## ⚠️ Security Note

**Never commit `.env` to git!**

The `.gitignore` file already excludes it:
```
backend/.env
```

✅ Safe to commit: `backend/.env.example`  
❌ Never commit: `backend/.env`

---

## 🐛 Troubleshooting

### Issue: "Sentry not receiving events"

**Check:**
1. DSN is correct in `backend/.env`
2. Backend server restarted after adding DSN
3. Your Sentry project is active

**Test:**
```bash
# Visit this URL to trigger a test error:
curl http://localhost:8000/boom
```

### Issue: "Gemini not working"

**Check:**
1. API key is valid
2. Backend restarted after adding key
3. Check backend logs: `tail -f backend.log`

**Should see:**
```
✅ Gemini AI enabled
```

---

## 📍 Quick Reference

| What | Where | Required? |
|------|-------|-----------|
| **Sentry DSN** | `backend/.env` | ⚠️ Recommended |
| **Gemini Key** | `backend/.env` | ✅ Optional |
| **Restart** | `./stop.sh && ./start.sh` | After changes |
| **Check logs** | `tail -f backend.log` | For debugging |

---

## 🎯 For Hackathon Demo

**Minimum setup (5 minutes):**
1. Add Sentry DSN only
2. Restart servers
3. Submit test reports
4. Show Sentry dashboard with traces

**Full setup (10 minutes):**
1. Add both Sentry DSN + Gemini key
2. Restart servers
3. Submit test reports with quick actions
4. Show AI enrichment in Sentry spans
5. Show similarity detection

---

Need help? Check `QUICKSTART.md` or `TESTING_GUIDE.md`!
