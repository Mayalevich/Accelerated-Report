# 🍰 Yellowcake Integration - Find Helpful Resources for Developers

## 🎯 What Yellowcake Does For You

**Yellowcake automatically finds helpful resources to help developers fix problems:**

- 📚 Stack Overflow solutions
- 📖 Official documentation links  
- 🐛 Related GitHub issues
- 📝 Tutorial articles

## 🔄 Complete Flow

```
1. USER taps "🔴 App Crashed"
   ↓
2. GEMINI enriches:
   → "iOS app crashes when loading profile due to memory issue"
   ↓
3. YELLOWCAKE searches:
   → Stack Overflow: "iOS memory crash profile loading"
   → Apple Docs: "Memory management in iOS"
   → GitHub: Similar crash issues
   ↓
4. DEVELOPER gets:
   ✅ Problem description (from Gemini)
   ✅ 3 Stack Overflow links with solutions
   ✅ 2 Official documentation links
   ✅ Related GitHub issues
```

## 🔑 Setup

### 1. Get Yellowcake API Key

1. Go to: https://yellowcake.dev/
2. Click "Get Started"
3. Sign up and get your API key
4. Add to `backend/.env`:

```bash
YELLOWCAKE_API_KEY=your_yellowcake_api_key_here
```

### 2. Install Dependencies (Already Done!)

```bash
cd backend
pip install -r requirements.txt
```

### 3. Test It

```bash
# Start servers
./start.sh

# Submit a crash report
# Check the response - it should include helpful_resources!
```

## 📊 What Developer Sees

### Before (Without Yellowcake):
```json
{
  "report_id": "abc123",
  "category": "crash",
  "severity": "critical",
  "description": "iOS app crashes when loading profile"
}
```

### After (With Yellowcake):
```json
{
  "report_id": "abc123",
  "category": "crash",
  "severity": "critical",
  "description": "iOS app crashes when loading profile",
  "helpful_resources": [
    {
      "type": "stackoverflow",
      "title": "Stack Overflow Solutions",
      "links": [
        "https://stackoverflow.com/questions/...iOS-crash-profile",
        "https://stackoverflow.com/questions/...memory-leak-ios",
        "https://stackoverflow.com/questions/...profile-loading-crash"
      ],
      "description": "Community solutions for similar issues"
    },
    {
      "type": "documentation",
      "title": "iOS Official Documentation",
      "links": [
        "https://developer.apple.com/...memory-management",
        "https://developer.apple.com/...debugging-crashes"
      ],
      "description": "Official platform documentation"
    }
  ]
}
```

## 🎯 Benefits

### For Developers:
- ✅ **Instant Solutions** - Don't need to Google, links are already there
- ✅ **Context-Aware** - Links are specific to the error type and platform
- ✅ **Time Saving** - From hours of searching to instant access
- ✅ **Quality Resources** - Official docs + community solutions

### For Demo:
- 🎪 **Impressive** - "Watch it automatically find Stack Overflow solutions!"
- 🚀 **Unique** - Most bug trackers don't do this
- 💡 **Practical** - Solves real developer pain point

## 🔄 How It Works Technically

### 1. Yellowcake Search
```python
async def find_helpful_resources_with_yellowcake(report_data, ai_enrichment):
    # Build smart search query from AI analysis
    query = f"{category} {platform} error solution"
    
    # Use Yellowcake API to extract from Stack Overflow
    response = await httpx.post(
        "https://api.yellowcake.dev/v1/extract",
        headers={"X-API-Key": YELLOWCAKE_API_KEY},
        json={
            "url": f"https://stackoverflow.com/search?q={query}",
            "prompt": f"Find top 3 relevant solutions for: {description}"
        }
    )
    
    # Returns: Top 3 Stack Overflow links
    return response.json()['results']
```

### 2. Platform-Specific Docs
```python
# Automatically searches platform-specific documentation
docs = {
    'ios': 'https://developer.apple.com',
    'android': 'https://developer.android.com',
    'web': 'https://developer.mozilla.org'
}

# Yellowcake extracts relevant doc pages
```

### 3. Stored with Report
```python
# Saved in database for quick access
{
    "report_id": "...",
    "helpful_resources": [...],  # JSON array
    "category": "crash",
    "severity": "critical"
}
```

## 📈 Integration with Sentry

```python
# Resources are also added to Sentry context
sentry_sdk.set_context("helpful_resources", {
    "resources": helpful_resources,
    "source": "yellowcake"
})

# Developers can see resources directly in Sentry dashboard!
```

## 💰 Pricing

Check https://yellowcake.dev/pricing for current pricing

**For Hackathon:**
- Free tier should be enough for demo
- Shows real value without cost commitment

## 🎪 Demo Script

### Show Without Yellowcake:
1. Submit crash report
2. "Here's the error... but where do I start?"
3. "Developer has to Google for solutions"

### Show With Yellowcake:
1. Enable Yellowcake in .env
2. Submit same crash report
3. "Look! It automatically found:"
   - 3 Stack Overflow solutions
   - 2 Apple documentation links
4. "Developer can click and start fixing immediately!"

### Wow Factor:
- ⚡ "From problem to solution in 5 seconds"
- 🎯 "Context-aware resources, not random Googling"
- 🚀 "This is the future of bug reporting"

## 🔧 Optional: Customize Search

You can modify what Yellowcake searches for:

```python
# In backend/main.py, find_helpful_resources_with_yellowcake()

# Add GitHub issues search
{
    "url": f"https://github.com/search?q={query}",
    "prompt": "Find related GitHub issues"
}

# Add tutorial sites
{
    "url": f"https://medium.com/search?q={query}",
    "prompt": "Find tutorial articles"
}
```

## ⚠️ Notes

- Yellowcake has rate limits - check your plan
- Searches happen async so they don't slow down submission
- Resources are optional - app works without them
- Can enable/disable by setting/unsetting YELLOWCAKE_API_KEY

## 🎯 Summary

**3 APIs Working Together:**

1. **Gemini** - Understands the problem
2. **Yellowcake** - Finds solutions
3. **Sentry** - Groups and tracks everything

**Result:** User taps once, developer gets problem description + solutions + monitoring. Magic! ✨
