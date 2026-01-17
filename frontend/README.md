# Frontend - User Interface

Simple, fast web interface for the Accelerated Report App.

## Files

- `index.html` - Main report submission page
- `dashboard.html` - Developer dashboard showing all reports
- `app.js` - Report form logic with offline queue
- `dashboard.js` - Dashboard logic
- `styles.css` - All styling

## Features

### Report Form (`index.html`)
- One dropdown + one text field (fast!)
- Chaos Mode toggle to simulate failures
- Offline-safe queue with auto-retry
- Recent submissions list

### Developer Dashboard (`dashboard.html`)
- View all submitted reports
- Statistics (total, by type)
- AI enrichment data (when available)
- Auto-refresh every 10 seconds

## How to Use

1. **Make sure backend is running** at `http://localhost:8000`

2. **Open the report form:**
   - Simply open `index.html` in your browser
   - OR use a simple HTTP server:
     ```bash
     python -m http.server 3000
     ```
     Then visit: `http://localhost:3000`

3. **Submit a test report:**
   - Select a type (crash/slow/bug/suggestion)
   - Type a message
   - Click "Send Report"

4. **Test Chaos Mode:**
   - Toggle "Chaos Mode" ON
   - Try submitting reports
   - Watch them queue and retry automatically

5. **View the dashboard:**
   - Click "View Developer Dashboard"
   - See all submitted reports
   - Check stats

## Person 2 (Frontend + UX) Tasks

✅ Initial Setup:
1. Open `index.html` in browser
2. Test form submission (backend must be running)
3. Verify it connects to API

✅ Core Features:
1. Report form UI (✅ done)
2. Form validation
3. API connection
4. Success/error messages

✅ Offline Queue:
1. localStorage queue (✅ done)
2. Auto-retry every 5 seconds
3. Queue status display

✅ Chaos Mode:
1. Toggle switch (✅ done)
2. Random delays (30% chance)
3. Random failures (30% chance)

✅ Dashboard:
1. List all reports
2. Stats cards
3. Auto-refresh

## API Configuration

If your backend runs on a different port, update this line in both `app.js` and `dashboard.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Testing Checklist

- [ ] Submit report successfully
- [ ] Toggle Chaos Mode
- [ ] Submit reports with chaos mode (see failures)
- [ ] Watch queued reports retry
- [ ] View dashboard
- [ ] Check stats update
- [ ] Verify enrichment data shows (when AI is added)

## Notes

- No build step required - pure HTML/CSS/JS
- Works in all modern browsers
- LocalStorage used for queue persistence
- CORS must be enabled in backend (already done)
