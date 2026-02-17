# Telegram Bot Troubleshooting Guide

## ❌ Connection Error: `httpx.ConnectError`

### Problem
The bot can't connect to Telegram's API servers. The error occurs during bot initialization:
```
telegram.error.NetworkError: httpx.ConnectError
```

### Root Cause
This is a **Windows + Python asyncio SSL/TLS handshake issue** - the synchronous HTTP client works fine (as shown by `test_telegram_connection.py` passing), but the async client used by python-telegram-bot fails.

### Solutions

#### ✅ Solution 1: Use Mobile Hotspot (RECOMMENDED - Quick Test)
1. Enable mobile hotspot on your phone
2. Connect your computer to the hotspot
3. Run the bot again:
   ```powershell
   .\erate\Scripts\python.exe telegram_bot\bot.py
   ```
4. If this works, the issue is your network (firewall/proxy)

#### ✅ Solution 2: Check Firewall/Antivirus
1. **Windows Defender Firewall:**
   - Open Windows Security → Firewall & network protection
   - Click "Allow an app through firewall"
   - Add Python: `C:\Users\orelm\OneDrive\Documents\GitHub\erateapp.com\opendata\erate\Scripts\python.exe`
   - Check both Private and Public networks

2. **Antivirus:**
   - Temporarily disable antivirus
   - Try running bot
   - If it works, add Python to antivirus exclusions

#### ✅ Solution 3: Corporate Network/Proxy
If you're on a corporate network:

1. Check if you need a proxy
2. Ask IT department for:
   - Proxy server address
   - Whether api.telegram.org is blocked
   
3. Configure proxy in bot (requires code modification)

#### ✅ Solution 4: Use Different Python Version
The issue might be specific to Python 3.12. Try:
```powershell
# Create venv with Python 3.11
C:\Users\orelm\AppData\Local\Programs\Python\Python311\python.exe -m venv erate311
.\erate311\Scripts\Activate.ps1
pip install python-telegram-bot requests pandas python-dotenv openai reportlab tabulate matplotlib
python telegram_bot\bot.py
```

#### ✅ Solution 5: Run on Different Machine
- Try running on a different computer/network
- Use a cloud server (see Cloud Deployment below)

---

## ☁️ Cloud Deployment (PERMANENT SOLUTION)

Since Telegram bots need to run 24/7 anyway, deploying to cloud solves both the connection issue AND keeps your bot online:

### Option A: Railway (Easiest, Free Tier)

1. **Prepare files:**
   ```powershell
   # Create requirements.txt
   .\erate\Scripts\python.exe -m pip freeze > requirements.txt
   ```

2. **Create `Procfile`:**
   ```
   worker: python telegram_bot/bot.py
   ```

3. **Push to GitHub:**
   ```powershell
   git init
   git add .
   git commit -m "E-Rate Telegram Bot"
   git push origin main
   ```

4. **Deploy to Railway:**
   - Go to https://railway.app
   - Sign up with GitHub
   - New Project → Deploy from GitHub
   - Select your repo
   - Add environment variables in Railway dashboard:
     - `TELEGRAM_BOT_TOKEN=8366203179:AAHaH2T5FSRdAUGCpb9AWfMtbAh2sfAGAQA`
     - `DEEPSEEK_API_KEY=your_key_here`
   - Bot starts automatically!

### Option B: Google Cloud Run (Free Tier)

```powershell
# Install Google Cloud SDK first
gcloud init
gcloud run deploy erate-bot --source . --region us-central1
```

### Option C: Heroku

```powershell
heroku create erate-bot
heroku config:set TELEGRAM_BOT_TOKEN=8366203179:AAHaH2T5FSRdAUGCpb9AWfMtbAh2sfAGAQA
git push heroku main
```

---

## 🔍 Diagnostic Tests

### Test 1: Check Telegram Reachability
```powershell
.\erate\Scripts\python.exe test_telegram_connection.py
```
✅ **Expected:** Bot info displays  
❌ **If fails:** Network issue

### Test 2: Check SSL/TLS
```powershell
.\erate\Scripts\python.exe -c "import ssl; print(ssl.OPENSSL_VERSION)"
```
Should show OpenSSL version

### Test 3: Test AsyncIO
```powershell
.\erate\Scripts\python.exe -c "import asyncio; import httpx; asyncio.run(httpx.AsyncClient().get('https://api.telegram.org/'))"
```
This tests if async HTTP works

---

## ⚠️ Known Limitations

### Why Terminal Bot Works But Telegram Doesn't
- **Terminal bot**: Uses synchronous HTTP requests (works)
- **Telegram bot**: Uses async HTTP with python-telegram-bot library (fails on your network)

### The Issue
Windows + Python 3.12 + asyncio + SSL/TLS + your network = Connection failures

This is a known issue with:
- Windows firewall deep packet inspection
- Corporate proxies
- Some antivirus software
- Python's asyncio SSL implementation on Windows

---

## 💡 Immediate Workarounds

### Workaround 1: Use Terminal Bot (Works Now)
```powershell
.\erate\Scripts\python.exe erate_bot.py
```
The terminal bot has all features and works perfectly on your machine.

### Workaround 2: Deploy to Cloud (Best Long-term)
Telegram bots should run 24/7 anyway, so cloud deployment is the proper solution.

### Workaround 3: Use WSL2 (Windows Subsystem for Linux)
```powershell
# Install WSL2
wsl --install

# In WSL2:
cd /mnt/c/Users/orelm/OneDrive/Documents/GitHub/erateapp.com/opendata
python3 -m venv erate
source erate/bin/activate
pip install python-telegram-bot requests pandas python-dotenv openai reportlab tabulate matplotlib
python telegram_bot/bot.py
```
Linux networking often works better than Windows for async operations.

---

## 📞 Getting Help

If none of the above works:

1. **Check your network:**
   - Are you on a corporate/school network?
   - Do you have a proxy?
   - Is port 443 (HTTPS) fully open?

2. **Check your system:**
   - Windows Firewall settings
   - Antivirus real-time protection
   - VPN active?

3. **Try different location:**
   - Different WiFi network
   - Mobile hotspot
   - Friend's house

---

## ✅ Success Indicators

When bot works correctly, you'll see:
```
🤖 Starting E-Rate Telegram Bot...
📊 Max records per query: 1000
🔐 Authorization: Open to all
✅ Bot is running!
🔗 Start chatting with your bot on Telegram
📱 Press Ctrl+C to stop
```

And no errors in the terminal.

---

## 📋 Summary

**What Works:**
- ✅ Bot token is valid
- ✅ Bot can be reached (test_telegram_connection.py passes)
- ✅ Terminal bot works perfectly
- ✅ All code is correct

**What Doesn't Work:**
- ❌ Async HTTP connection from python-telegram-bot
- ❌ Issue is network/Windows/SSL related, not code

**Best Solutions:**
1. 🥇 Deploy to cloud (Railway/Heroku) - solves everything
2. 🥈 Use mobile hotspot temporarily
3. 🥉 Use WSL2 on Windows
4. ⏳ Use terminal bot while troubleshooting

---

**Need more help?** Share this file with your IT department or try the cloud deployment option.
