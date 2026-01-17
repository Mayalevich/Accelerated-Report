# 🧪 TESTING GUIDE - Is Everything Working?

Follow these steps to verify your Accelerated Report App is working correctly.

---

## ✅ Step 1: GitHub Repository (DONE ✓)

Your code is live at: **https://github.com/Mayalevich/Accelerated-Report**

You can see:
- ✅ All files uploaded
- ✅ README displays correctly  
- ✅ Backend, frontend, and docs folders

---

## ✅ Step 2: Backend Setup (DONE ✓)

Backend dependencies are installed and ready!

---

## 🧪 Step 3: Test the Backend (DO THIS NOW)

### Open a new terminal and run:

```bash
# Navigate to backend
cd /Users/jingyu/Documents/Sentry/backend

# Activate virtual environment
source .venv/bin/activate

# Start the server
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Keep that terminal open and running!

---

## 🧪 Step 4: Test Backend Endpoints

### Open a NEW terminal (keep server running) and test:

#### Test 1: Health Check
```bash
curl http://localhost:8000/health
```
**Expected:** `{"status":"healthy"}`

#### Test 2: Root Endpoint
```bash
curl http://localhost:8000/
```
**Expected:** `{"status":"ok","service":"Accelerated Report API"}`

#### Test 3: Create a Report
```bash
curl -X POST http://localhost:8000/reports \
  -H "Content-Type: application/json" \
  -d '{
    "type": "bug",
    "message": "Test report - checking if system works",
    "platform": "web",
    "app_version": "1.0.0"
  }'
```
**Expected:** `{"report_id":"some-uuid","status":"received"}`

#### Test 4: Get All Reports
```bash
curl http://localhost:8000/reports
```
**Expected:** JSON with your test report(s)

---

## 🧪 Step 5: Test the Frontend

### Open the frontend in your browser:

1. **Option A - Direct file:**
   - Navigate to `/Users/jingyu/Documents/Sentry/frontend/`
   - Double-click `index.html`
   - It should open in your browser

2. **Option B - HTTP server (better):**
   ```bash
   cd /Users/jingyu/Documents/Sentry/frontend
   python3 -m http.server 3000
   ```
   Then open: http://localhost:3000

### Test the form:

1. **Select a type:** "Bug"
2. **Type a message:** "Testing the frontend"
3. **Click "Send Report"**

**Expected:** You should see "✅ Report sent successfully!"

---

## 🧪 Step 6: Test Chaos Mode

1. **Toggle "Chaos Mode" ON** in the frontend
2. **Try submitting 3-4 reports quickly**
3. **Watch what happens:**
   - Some will succeed immediately
   - Some will show "⏳ Queued for retry"
   - After 5 seconds, queued reports will auto-send
   - You'll see "✅ Delivered" when they succeed

**This proves your offline queue works!**

---

## 🧪 Step 7: View Developer Dashboard

1. In the frontend, click **"View Developer Dashboard →"**
2. You should see:
   - All submitted reports
   - Statistics (total count, by type)
   - Report details

---

## 🎯 Step 8: Set Up Sentry (For Full Functionality)

**Important:** To see Sentry monitoring, you need to:

1. **Go to https://sentry.io**
2. **Create account** (free)
3. **Create new project:**
   - Platform: Python
   - Name: accelerated-report-app
4. **Copy the DSN** (looks like: `https://xxxxx@xxxxx.ingest.sentry.io/xxxxx`)

5. **Add DSN to your backend:**
   ```bash
   cd /Users/jingyu/Documents/Sentry/backend
   nano .env
   # or use any text editor
   ```
   
   Edit `.env` to add your DSN:
   ```env
   SENTRY_DSN=your_actual_dsn_here
   ENVIRONMENT=dev
   TRACES_SAMPLE_RATE=1.0
   ```

6. **Restart the backend** (Ctrl+C in terminal, then run uvicorn again)

---

## 🧪 Step 9: Test Sentry Integration

Once Sentry DSN is added:

### Test 1: Force an error
```bash
curl http://localhost:8000/boom
```

**Expected:** Error in browser, BUT check Sentry dashboard - you should see the error there!

### Test 2: Submit a report
```bash
curl -X POST http://localhost:8000/reports \
  -H "Content-Type: application/json" \
  -d '{"type": "crash", "message": "App crashed", "platform": "web", "app_version": "1.0.0"}'
```

**In Sentry:**
1. Go to **Performance** tab
2. You should see transaction: `critical.report_submit`
3. Click it to see the spans breakdown!

---

## ✅ SUCCESS CRITERIA

Your app is working if:

- ✅ Backend starts without errors
- ✅ Health endpoint returns `{"status":"healthy"}`
- ✅ Can create reports via curl
- ✅ Frontend form loads and displays
- ✅ Can submit reports from frontend
- ✅ Chaos Mode queues and retries failed reports
- ✅ Dashboard shows all reports
- ✅ (With Sentry) Errors appear in Sentry dashboard
- ✅ (With Sentry) Transactions appear in Performance tab

---

## 🐛 Troubleshooting

### Backend won't start
```bash
cd /Users/jingyu/Documents/Sentry/backend
source .venv/bin/activate
pip install -r requirements.txt
```

### "Address already in use"
```bash
# Kill process on port 8000
lsof -ti :8000 | xargs kill -9
# Then start server again
```

### Frontend can't connect
- Make sure backend is running on port 8000
- Check browser console (F12) for errors
- Verify `API_BASE_URL` in `frontend/app.js` is `http://localhost:8000`

### No data in Sentry
- Check DSN is correct in `.env`
- Restart backend after changing `.env`
- Try the `/boom` endpoint to force an error
- Check Sentry project settings

---

## 📊 NEXT STEPS

Once everything is working:

1. **Read the documentation:**
   - `START_HERE.md` - Overview
   - `docs/demo-script.md` - Practice your demo
   - `docs/team-division.md` - Divide the work

2. **Practice the demo:**
   - Normal submission
   - Chaos Mode
   - Show Sentry dashboard

3. **Add your team members:**
   - Share the GitHub repo
   - Share the Sentry DSN (securely!)
   - Assign tasks from `docs/team-division.md`

---

## 🏆 YOU'RE READY!

If all tests pass, you have a **fully working hackathon project!**

**What makes it impressive:**
- ✅ Real backend with API
- ✅ Offline-safe frontend
- ✅ Sentry observability
- ✅ Professional documentation
- ✅ Demonstrable reliability (Chaos Mode)

**Good luck! 🚀**
