# Deploy E-Rate Bot to Railway (Free)

## Why Deploy to Cloud?

Your Telegram bot has a **network connection issue** on Windows (Python async + SSL). 
Deploying to cloud solves this AND keeps your bot running 24/7!

## ☁️ Deploy in 5 Minutes

### Step 1: Sign Up for Railway
1. Go to https://railway.app
2. Click "Login" → Sign in with GitHub
3. Authorize Railway

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Click "Configure GitHub App"
4. Select this repository: `erateapp.com/opendata`
5. Click "Deploy Now"

### Step 3: Add Environment Variables
1. In Railway dashboard, click your project
2. Click "Variables" tab
3. Add these variables:
   ```
   TELEGRAM_BOT_TOKEN=8366203179:AAHaH2T5FSRdAUGCpb9AWfMtbAh2sfAGAQA
   DEEPSEEK_API_KEY=your_deepseek_key_here
   ```
4. Click "Add" for each

### Step 4: Deploy!
1. Railway automatically detects Python
2. Reads `requirements.txt`
3. Reads `Procfile`
4. Starts your bot!

### Step 5: Test
1. Open Telegram
2. Search for `@erateappbot`
3. Send `/start`
4. Bot responds! 🎉

---

## 📊 Railway Dashboard

Monitor your bot:
- **Logs**: See all bot activity
- **Metrics**: CPU, memory usage
- **Deployments**: View deployment history
- **Settings**: Restart bot, change config

---

## 💰 Cost

**Free Tier Includes:**
- $5 of usage per month
- Enough for small bots
- No credit card required initially

Your bot uses minimal resources:
- Mostly idle
- Responds to commands
- Should stay within free tier

---

## 🔄 Updates

To update your bot:
1. Make changes locally
2. Push to GitHub:
   ```powershell
   git add .
   git commit -m "Update bot"
   git push
   ```
3. Railway auto-deploys!

---

## 📝 Alternative: Push to GitHub First

If you haven't pushed to GitHub yet:

```powershell
# In your project directory
git init
git add .
git commit -m "Initial commit: E-Rate Telegram Bot"

# Create repo on GitHub (erateapp.com/opendata)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

Then follow Railway steps above.

---

## ✅ Success Indicators

When deployed successfully:
- ✅ Railway shows "Deployed"
- ✅ Logs show: "🤖 Starting E-Rate Telegram Bot..."
- ✅ Logs show: "✅ Bot is running!"
- ✅ Bot responds in Telegram

---

## 🆘 Troubleshooting

### Deployment Failed
- Check Railway logs
- Verify `requirements.txt` exists
- Verify `Procfile` exists

### Bot Not Responding
- Check environment variables are set
- Check Railway logs for errors
- Verify bot token is correct

### Need Help?
- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## 🚀 You're Done!

Your bot now:
- ✅ Runs 24/7
- ✅ No Windows network issues
- ✅ Auto-restarts if crashed
- ✅ Easy to monitor and update

**Start chatting with @erateappbot on Telegram!** 🎉
