# Quick Start Guide - Accelerated Report App

This guide gets you from zero to running demo in **under 15 minutes**.

---

## ⚡ Prerequisites

- **Python 3.10+** installed
- **Web browser** (Chrome, Firefox, Safari)
- **Sentry account** (free at [sentry.io](https://sentry.io))

---

## 🚀 Step-by-Step Setup

### Step 1: Create Sentry Project (5 minutes)

1. Go to [sentry.io](https://sentry.io) and log in (or create free account)
2. Click **"Create Project"**
3. Choose platform: **Python**
4. Name it: `accelerated-report-app`
5. Click **"Create Project"**
6. **Copy the DSN** (looks like: `https://xxxxx@xxxxx.ingest.sentry.io/xxxxx`)

---

### Step 2: Set Up Backend (5 minutes)

Open terminal and run these commands:

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Now **edit the `.env` file** and paste your Sentry DSN:

```env
SENTRY_DSN=paste_your_dsn_here
ENVIRONMENT=dev
TRACES_SAMPLE_RATE=1.0
```

**Start the backend:**

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ **Test it:** Open [http://localhost:8000/boom](http://localhost:8000/boom) in your browser

This will trigger a test error. Check your Sentry dashboard - you should see it!

---

### Step 3: Open Frontend (2 minutes)

**Option A - Simple (recommended):**
- Open `frontend/index.html` directly in your browser

**Option B - With HTTP server:**
```bash
# In a new terminal window
cd frontend
python -m http.server 3000
```
Then open: [http://localhost:3000](http://localhost:3000)

---

### Step 4: Test the Demo (3 minutes)

1. **Submit a normal report:**
   - Select "Bug" from dropdown
   - Type: "Search not working"
   - Click "Send Report"
   - You should see "✅ Report sent successfully!"

2. **Check Sentry:**
   - Go to your Sentry dashboard
   - Click **Performance** tab
   - You should see `critical.report_submit` transaction
   - Click it to see the spans!

3. **Test Chaos Mode:**
   - Toggle "Chaos Mode" ON
   - Submit 2-3 reports quickly
   - Watch some fail and queue
   - Toggle Chaos Mode OFF
   - Watch queued reports deliver automatically!

4. **View Dashboard:**
   - Click "View Developer Dashboard" link
   - See all your submitted reports

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend opens in browser
- [ ] Test error shows in Sentry
- [ ] Can submit reports successfully
- [ ] Chaos Mode queues failed reports
- [ ] Sentry shows `critical.report_submit` transactions
- [ ] Dashboard displays reports

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # or Windows equivalent
pip install -r requirements.txt
```

### "Connection refused" in frontend
- Make sure backend is running on port 8000
- Check `API_BASE_URL` in `frontend/app.js`

### No data in Sentry
- Double-check your DSN in `backend/.env`
- Make sure you saved the file
- Restart the backend server

### CORS errors
- Already handled in backend
- If still seeing errors, check browser console for specifics

---

## 📚 Next Steps

### Person 1 (Backend + Sentry)
- Read: `backend/README.md`
- Read: `docs/team-division.md` (Person 1 section)
- Task: Verify all Sentry instrumentation is working

### Person 2 (Frontend + UX)
- Read: `frontend/README.md`
- Read: `docs/team-division.md` (Person 2 section)
- Task: Test offline queue thoroughly

### Person 3 (Intelligence)
- Read: `docs/team-division.md` (Person 3 section)
- Task: Research Gemini API
- Create: `backend/enrichment.py`

### Everyone
- Read: `docs/demo-script.md`
- Practice the 60-second demo together

---

## 🎯 Demo Preparation

Before showing to judges:

1. **Have 2-3 test reports already submitted** (so dashboard isn't empty)
2. **Open Sentry dashboard** in a separate tab
3. **Practice the chaos mode toggle**
4. **Know your talking points** (see `docs/demo-script.md`)

---

## 🔗 Important Files

| File | Purpose |
|------|---------|
| `README.md` | Main project overview |
| `backend/README.md` | Backend setup & tasks |
| `frontend/README.md` | Frontend setup & tasks |
| `docs/architecture.md` | System design |
| `docs/demo-script.md` | What to say to judges |
| `docs/team-division.md` | Who does what |

---

## 🆘 Need Help?

**Backend not starting?**
- Check Python version: `python --version` (need 3.10+)
- Check if port 8000 is already in use

**Frontend not connecting?**
- Verify backend is running
- Check browser console for errors

**Sentry not showing data?**
- Verify DSN is correct
- Check Sentry project settings
- Make sure Performance is enabled

---

## 🎉 You're Ready!

If you completed all steps above, you're ready to:
- Develop additional features
- Practice your demo
- Win the hackathon!

**Good luck! 🚀**

---

## Quick Commands Reference

```bash
# Start backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload

# Start frontend (optional)
cd frontend
python -m http.server 3000

# Test backend
curl http://localhost:8000/health

# Test error capture
curl http://localhost:8000/boom
```
