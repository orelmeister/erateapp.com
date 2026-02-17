# E-Rate Open Data Platform

A comprehensive platform for analyzing USAC E-Rate funding data with AI-powered insights, natural language queries, and advanced data enrichment.

## 🎯 Main Application: SkyRate AI

**SkyRate AI** is the primary web application - an advanced AI-powered platform for analyzing USAC E-Rate data with natural language queries, intelligent enrichment, and beautiful visualizations.

### Key Features

- **🤖 AI-Powered Intelligence**: Natural language queries with multi-model AI support (Gemini, Claude, DeepSeek)
- **📧 Email Integration**: Send AI analysis reports directly via Gmail
- **🔍 Advanced Search**: Auto-save queries with recent searches sidebar
- **📊 Data Enrichment**: Automatic NCES school data with validated contact information
- **🎨 Modern UI**: Beautiful design inspired by erateapp.com
- **📈 Visualizations**: Interactive charts and professional PDF reports

### Quick Start

1. **Navigate to the application:**
   ```bash
   cd skyrate-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Windows convenience launchers (repo root)

If you prefer launching from `opendata/` (and avoiding the common “File does not exist: app.py” mistake), use:

- PowerShell: `start_skyrate_ai.ps1`
- CMD: `start_skyrate_ai.bat`

These scripts launch Streamlit pointing at `skyrate-ai/app.py` and default to port 8502.

For detailed setup instructions, see [skyrate-ai/README.md](skyrate-ai/README.md)

## 📚 Additional Components

### USAC MCP Server
Model Context Protocol server for USAC E-Rate data access. See [usac-mcp-server/README.md](usac-mcp-server/README.md)

### Utilities
- `usac_data_fetcher.py` - Core data fetching utilities
- `data_exporter.py` - Data export functionality
- `llm_analyzer.py` - LLM analysis tools

## 📖 Documentation

- **Quick Start Guide**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Deployment**: [docs/DEPLOY_TO_RAILWAY.md](docs/DEPLOY_TO_RAILWAY.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Improvements Summary**: [docs/IMPROVEMENTS_SUMMARY.md](docs/IMPROVEMENTS_SUMMARY.md)
- **Run SkyRate AI (Windows)**: [docs/RUN_SKYRATE_AI.md](docs/RUN_SKYRATE_AI.md)
- **Progress Log (2025-12-25)**: [docs/PROGRESS_2025-12-25.md](docs/PROGRESS_2025-12-25.md)

## 🛠️ Requirements

- Python 3.12+
- Streamlit 1.40+
- API keys for AI services (OpenAI, Anthropic, or DeepSeek)
- Gmail App Password (for email functionality)

## 📝 Project Structure

```
opendata/
├── skyrate-ai/          # Main Streamlit application
│   ├── app.py          # Application entry point
│   ├── pages/          # Additional app pages
│   ├── utils/          # Utility modules
│   └── docs/           # Application documentation
├── usac-mcp-server/    # MCP server for data access
├── docs/               # Project documentation
├── data/               # Data storage
│   └── cache/          # Cached API responses
└── reports/            # Generated reports
```

## 🚀 Getting Started

The fastest way to get started is to use the SkyRate AI application:

1. Clone this repository
2. Navigate to `skyrate-ai` directory
3. Follow the setup instructions in [skyrate-ai/README.md](skyrate-ai/README.md)

## 📄 License

This project is for analyzing publicly available USAC E-Rate data.

## 🤝 Contributing

Contributions are welcome! Please ensure all changes maintain the current code quality and documentation standards.

---

**Need help?** Check the [troubleshooting guide](docs/TROUBLESHOOTING.md) or review the documentation in the `docs/` directory.
