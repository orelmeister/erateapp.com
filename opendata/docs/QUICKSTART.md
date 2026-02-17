# QUICK START GUIDE

## Start the Bot Immediately

### Option 1: Double-click the batch file
```
start_bot.bat
```

### Option 2: Run from PowerShell
```powershell
# Activate virtual environment
.\erate\Scripts\Activate.ps1

# Run the bot
python erate_bot.py
```

## First Time Setup (5 minutes)

### Step 1: Virtual Environment is Ready! ✓
The `erate` virtual environment is already created with all dependencies installed.

### Step 2: (Optional) Add AI Integration
If you want AI-powered analysis, add ONE of these API keys to `.env`:

**For DeepSeek Reasoner** (Best for analytical tasks):
1. Visit: https://platform.deepseek.com/
2. Create account and get API key
3. Open `.env` file
4. Uncomment and add: `DEEPSEEK_API_KEY=your_key_here`

**For OpenAI GPT-4**:
1. Visit: https://platform.openai.com/api-keys
2. Add: `OPENAI_API_KEY=sk-...`

**For Anthropic Claude**:
1. Visit: https://console.anthropic.com/
2. Add: `ANTHROPIC_API_KEY=sk-ant-...`

### Step 3: Run the Bot
```powershell
# Activate virtual environment
.\erate\Scripts\Activate.ps1

# Run the bot
python erate_bot.py
```

## Common Use Cases

### Find Schools That Got Denied Funding in 2024
1. Run the bot
2. Choose AI provider (or skip)
3. Select `1` - Query by funding year
4. Enter: `2024`
5. Select `2` - Filter current data  
6. Choose `4` - Show denied/unfunded only
7. Review results!

### Ask: "Which schools got the most funding in 2023?"
1. Query year `2023` (option 1)
2. Select `3` - Ask AI a question
3. Type: "Which schools got the most funding?"
4. Get AI-powered insights!

### Export Data for Analysis
1. Load and filter data as needed
2. Select `5` - Export current data
3. Open the JSON file in Excel/Python/etc.

## Tips
- **Start small**: Query 1000-5000 records at first
- **Use filters**: Narrow down before asking AI questions
- **No AI needed**: Basic stats work without API keys
- **Cache enabled**: Re-running same query is instant

## Troubleshooting

**"No data loaded"**: Run option 1 first to query by year

**"AI not configured"**: Either add API key to `.env` or select option 6 to reconfigure

**"API Error"**: Check internet connection and try again

## Need Help?
Check `README.md` for detailed documentation.
