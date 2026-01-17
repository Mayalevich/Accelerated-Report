# HACKATHON CHECKLIST ✅

Complete guide from setup to submission.

---

## 🎯 PHASE 1: SETUP (Day 1 - First 2 Hours)

### Everyone Together (30 minutes)

- [ ] **Create Sentry Project**
  - Go to https://sentry.io
  - Create new project (Python/FastAPI)
  - Copy DSN
  - Share DSN securely with team

- [ ] **Clone/Setup Repository**
  - Clone this repo or set it up locally
  - Run setup script: `./setup.sh` (Mac) or `.\setup.ps1` (Windows)
  - Each person: verify they can run backend

- [ ] **Agree on API Contract**
  - Review POST /reports format
  - Confirm everyone understands the structure
  - No changes without telling the team

- [ ] **Create Team Communication Channel**
  - Discord/Slack/WhatsApp group
  - Share Sentry DSN here (privately!)
  - Share any API keys here

### Person 1: Backend + Sentry (30 minutes)

- [ ] Set up Python virtual environment
- [ ] Install dependencies
- [ ] Add Sentry DSN to `.env`
- [ ] Start backend: `uvicorn main:app --reload`
- [ ] Test `/boom` endpoint → verify error in Sentry
- [ ] Test POST /reports with curl/Postman

### Person 2: Frontend (30 minutes)

- [ ] Open `frontend/index.html` in browser
- [ ] Verify form loads
- [ ] Try submitting (should fail if backend not ready)
- [ ] Once backend ready: submit test report
- [ ] Verify success message appears

### Person 3: Intelligence (30 minutes)

- [ ] Research Gemini API documentation
- [ ] Get Gemini API key (if available)
- [ ] Research Yellowcake API (if applicable)
- [ ] Design enrichment output format
- [ ] Write initial enrichment function stub

---

## 🚀 PHASE 2: CORE FEATURES (Day 1 - Next 4-6 Hours)

### Person 1: Backend + Sentry (Priority Tasks)

- [ ] **Critical Experience Instrumentation** ⭐ MOST IMPORTANT
  - [ ] Transaction: `critical.report_submit`
  - [ ] Tags: `critical_experience`, `report_type`, `platform`
  - [ ] Spans: `validate_input`, `store_report_db`
  - [ ] Breadcrumbs for key actions
  
- [ ] **Metrics** ⭐ IMPORTANT
  - [ ] `reports.submitted` counter
  - [ ] `reports.failed` counter
  - [ ] `report.submit.latency_ms` distribution

- [ ] **Error Handling**
  - [ ] All exceptions captured by Sentry
  - [ ] Proper error responses
  - [ ] Context added to errors

- [ ] **Database**
  - [ ] SQLite setup working
  - [ ] Reports saving correctly
  - [ ] GET /reports returning data

### Person 2: Frontend (Priority Tasks)

- [ ] **Fast Submission Flow** ⭐ IMPORTANT
  - [ ] Form validation
  - [ ] Clean success messages
  - [ ] Under 10 seconds to submit

- [ ] **Offline Queue** ⭐ MOST IMPORTANT
  - [ ] localStorage queue implementation
  - [ ] Save failed reports
  - [ ] Auto-retry every 5 seconds
  - [ ] Show queue count
  - [ ] Remove on success

- [ ] **Chaos Mode** ⭐ IMPORTANT
  - [ ] Toggle switch
  - [ ] 30% random delay (800ms)
  - [ ] 30% random failure
  - [ ] Works reliably

- [ ] **Developer Dashboard**
  - [ ] Fetch reports from API
  - [ ] Display in cards
  - [ ] Show statistics
  - [ ] Auto-refresh

### Person 3: Intelligence (Optional, but Impressive)

- [ ] **Gemini Integration**
  - [ ] Call Gemini API with report message
  - [ ] Parse JSON response
  - [ ] Extract: summary, category, severity, confidence
  - [ ] Handle errors gracefully

- [ ] **Integration with Backend**
  - [ ] Work with Person 1 to add enrichment call
  - [ ] Update database with enrichment
  - [ ] Never break report submission if AI fails

- [ ] **Yellowcake Integration** (if applicable)
  - [ ] Search for similar reports
  - [ ] Return cluster IDs or similar report IDs
  - [ ] Handle failures

---

## 🎨 PHASE 3: POLISH (Day 2 - 2-3 Hours)

### Everyone

- [ ] **Test Everything Together**
  - [ ] Submit 10 test reports
  - [ ] Toggle Chaos Mode on/off
  - [ ] Verify queue works
  - [ ] Check Sentry shows all data
  - [ ] Verify dashboard displays correctly

- [ ] **Clean Up Code**
  - [ ] Remove debug print statements
  - [ ] Add comments for complex logic
  - [ ] Consistent formatting

- [ ] **Verify No Secrets Committed**
  - [ ] Check `.env` is in `.gitignore`
  - [ ] No API keys in code
  - [ ] No hardcoded DSNs

### Person 1: Backend Polish

- [ ] Add logging for important operations
- [ ] Error messages are clear
- [ ] API responses are consistent
- [ ] Health check endpoint works

### Person 2: Frontend Polish

- [ ] UI looks clean
- [ ] Mobile responsive (basic)
- [ ] No console errors
- [ ] Loading states added

### Person 3: Intelligence Polish

- [ ] Enrichment data displays well
- [ ] Confidence scores make sense
- [ ] Fallback behavior is clear

---

## 🎬 PHASE 4: DEMO PREPARATION (Day 2 - 2 Hours)

### Setup Demo Environment

- [ ] **Prepare Demo Data**
  - [ ] Submit 3-5 test reports in advance
  - [ ] Include variety: crash, slow, bug, suggestion
  - [ ] Ensure dashboard isn't empty

- [ ] **Open All Windows**
  - [ ] Frontend: report form
  - [ ] Sentry dashboard (Performance tab)
  - [ ] Sentry dashboard (Issues tab)
  - [ ] Developer dashboard (optional)

- [ ] **Test Demo Flow**
  - [ ] Practice submitting report
  - [ ] Practice toggling Chaos Mode
  - [ ] Practice showing Sentry
  - [ ] Time it: should be 60-90 seconds

### Practice Demo Script

- [ ] **Read `docs/demo-script.md`**
- [ ] **Practice together 3 times**
- [ ] **Assign who speaks when**
  - Person 1: Sentry technical details
  - Person 2: User experience / reliability
  - Person 3: AI enrichment (if implemented)

### Prepare Answers to Common Questions

- [ ] "Why did you build this?"
- [ ] "Where does Sentry fit in?"
- [ ] "What's the critical experience?"
- [ ] "How would real apps use this?"
- [ ] "What about the AI part?"
- [ ] "Can you show Seer?"

---

## 📤 PHASE 5: SUBMISSION (Final Steps)

### GitHub

- [ ] **Push to GitHub**
  - [ ] Follow `GITHUB_SETUP.md`
  - [ ] Repository is public
  - [ ] README displays correctly
  - [ ] No secrets committed

- [ ] **Repository Polish**
  - [ ] Add description
  - [ ] Add topics/tags
  - [ ] Add team members as collaborators

### Documentation Check

- [ ] README.md is complete
- [ ] QUICKSTART.md is accurate
- [ ] All docs/ files are present
- [ ] Code comments are clear

### Final Testing

- [ ] **Clean Install Test**
  - [ ] Clone repo fresh
  - [ ] Run setup script
  - [ ] Verify it works from scratch

- [ ] **Different Browser Test**
  - [ ] Test in Chrome
  - [ ] Test in Firefox (optional)

### Submission Form

- [ ] Submit GitHub URL to hackathon
- [ ] Mention "Sentry: Best Use of Sentry" category
- [ ] Highlight key features:
  - Critical experience monitoring
  - Offline-safe queue
  - Chaos mode demo
  - AI enrichment (if done)

---

## 🏆 PRE-DEMO FINAL CHECK (10 Minutes Before)

### Technical

- [ ] Backend running: `uvicorn main:app --reload`
- [ ] Frontend open in browser
- [ ] Sentry dashboard open
- [ ] Test reports already submitted
- [ ] Chaos Mode toggle OFF initially

### Team

- [ ] Everyone knows their speaking part
- [ ] Confident about technical details
- [ ] Know how to answer questions
- [ ] Backup plan if something breaks

### Backup Plans

- [ ] If backend crashes: show queue working
- [ ] If Sentry doesn't load: show code instrumentation
- [ ] If demo stutters: explain what should happen

---

## 📊 SCORING SELF-CHECK

Grade yourself honestly before submitting:

### Best Use of Sentry (Primary Goal)

- [ ] ⭐ Critical experience defined and monitored
- [ ] ⭐ Full tracing with spans
- [ ] ⭐ Metrics tracked and meaningful
- [ ] ⭐ Errors captured with context
- [ ] ⭐ Can demonstrate Seer (optional)

**Score: ___ / 5**

### Technical Implementation

- [ ] Backend works reliably
- [ ] Frontend is clean and fast
- [ ] Queue + retry works perfectly
- [ ] AI enrichment works (optional)
- [ ] No major bugs

**Score: ___ / 5**

### Demo & Presentation

- [ ] Can demo in 60-90 seconds
- [ ] Demo is impressive (Chaos Mode!)
- [ ] Confident explaining Sentry usage
- [ ] Can answer judge questions
- [ ] Professional presentation

**Score: ___ / 5**

### Documentation

- [ ] README is clear
- [ ] Setup instructions work
- [ ] Code is documented
- [ ] Architecture is explained

**Score: ___ / 4**

**Total: ___ / 19**

**Target: 15+ to be competitive**

---

## 🐛 LAST-MINUTE TROUBLESHOOTING

### Backend won't start
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
python -c "import fastapi; print('OK')"
```

### No data in Sentry
- Check DSN in `.env`
- Restart backend
- Visit `/boom` to force an error
- Check Sentry project settings

### Frontend not connecting
- Backend running on port 8000?
- Check `API_BASE_URL` in `app.js`
- Check browser console for errors

### Queue not working
- Check browser console
- Check localStorage in DevTools
- Verify retry interval is set

---

## ✅ FINAL CONFIDENCE CHECK

Ask yourself:

- [ ] Can I set this up from scratch in 15 minutes?
- [ ] Can I explain why we used Sentry?
- [ ] Can I show the critical experience in Sentry?
- [ ] Can I demonstrate failure recovery?
- [ ] Am I proud of this project?

**If all YES → You're ready! 🚀**

**If any NO → Review that section again**

---

## 🎉 GOOD LUCK!

You've built something impressive. Now:

1. **Trust your preparation**
2. **Show confidence in the demo**
3. **Explain clearly why Sentry matters**
4. **Have fun!**

**You've got this! 🏆**

---

## 📞 Emergency Contacts

**During Hackathon:**
- Person 1 (Backend): [Phone/Discord]
- Person 2 (Frontend): [Phone/Discord]
- Person 3 (AI): [Phone/Discord]

**Sentry Support:**
- Docs: https://docs.sentry.io
- Discord: https://discord.gg/sentry

---

**Last Updated:** Check this list 1 hour before demo time!
