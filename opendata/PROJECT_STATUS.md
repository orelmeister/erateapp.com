# SkyRate AI - Project Status & Continuation Guide

> **Last Updated:** January 15, 2026  
> **Domain:** skyrate.ai  
> **Deployment Target:** DigitalOcean  
> **Status:** Active Development - Phase 2 (Backend API Completion)

---

## 🎯 Project Overview

SkyRate AI is an E-Rate intelligence platform that helps:
- **Consultants** ($300/month or $3,000/year): Find denied applications, generate appeal strategies, monitor applications
- **Vendors** ($200/month or $2,000/year): Find high-discount schools, track Form 470 opportunities, equipment leads

### Key Differentiators vs Competitors
| Feature | QueryBob | Funds For Learning | SkyRate AI |
|---------|----------|-------------------|------------|
| Form 470 Lead Search | ✅ | ✅ | ✅ |
| Form 471 FRN Search | ✅ | ✅ | ✅ |
| AI-Powered Analysis | ❌ | ❌ | ✅ **Unique** |
| Appeal Strategy Generation | ❌ | ❌ | ✅ **Unique** |
| Denial Reason Parsing | ❌ | ❌ | ✅ **Unique** |
| Funding Predictions | ❌ | ❌ | ✅ **Unique** |
| Application Monitoring | Basic | ✅ | ✅ + AI Alerts |
| Pricing | $250-$3000/yr | Enterprise | $200-$300/mo |

---

## 📁 Repository Structure

```
opendata/
├── skyrate-ai-v2/              # 🎯 ACTIVE - Production Stack
│   ├── backend/                # FastAPI Python Backend
│   │   ├── app/
│   │   │   ├── api/v1/         # REST API Endpoints
│   │   │   ├── core/           # Config, DB, Security
│   │   │   ├── models/         # SQLAlchemy ORM Models
│   │   │   └── services/       # Business Logic (TO BE PORTED)
│   │   └── requirements.txt
│   ├── frontend/               # Next.js 14 + Tailwind
│   │   ├── app/                # App Router Pages
│   │   └── lib/                # API client, auth store
│   └── docker-compose.yml
│
├── skyrate-ai/                 # ⚠️ LEGACY - Streamlit (reference only)
│   └── utils/                  # 🔑 BUSINESS LOGIC TO PORT
│       ├── usac_client.py      # USAC API Client
│       ├── ai_models.py        # AI Model Manager (Gemini, Claude, DeepSeek)
│       ├── denial_analyzer.py  # Denial Reason Parser
│       ├── appeals_strategy.py # Appeal Strategy Generator
│       ├── enrichment.py       # NCES School Enrichment
│       ├── email_sender.py     # Gmail/SMTP Email
│       ├── workspace.py        # Caching & History
│       └── evidence_pack.py    # Document Generation
│
├── usac-mcp-server/            # MCP Server for Claude Desktop
│   └── server.py
│
└── docs/                       # Documentation
    ├── PROGRESS_2026-01-14.md  # Previous handoff
    └── ...
```

---

## 🏗️ Current Implementation Status

### Backend API (`skyrate-ai-v2/backend/`)

| Endpoint | File | Status | Description |
|----------|------|--------|-------------|
| `POST /api/v1/auth/register` | auth.py | ✅ Done | User registration |
| `POST /api/v1/auth/login` | auth.py | ✅ Done | JWT login |
| `GET /api/v1/auth/me` | auth.py | ✅ Done | Current user |
| `POST /api/v1/query` | query.py | ⚠️ Stub | NL query → USAC search |
| `GET /api/v1/query/search` | query.py | ⚠️ Stub | Direct USAC search |
| `POST /api/v1/consultant/analyze` | consultant.py | ⚠️ Stub | AI analysis |
| `GET /api/v1/consultant/denied` | consultant.py | ❌ Missing | Find denied apps |
| `POST /api/v1/consultant/appeal-strategy` | consultant.py | ❌ Missing | Generate appeal |
| `GET /api/v1/vendor/opportunities` | vendor.py | ⚠️ Stub | Form 470 leads |
| `GET /api/v1/vendor/equipment` | vendor.py | ❌ Missing | Equipment search |
| `POST /api/v1/subscriptions/create` | subscriptions.py | ⚠️ Stub | Stripe checkout |
| `POST /api/v1/subscriptions/webhook` | subscriptions.py | ⚠️ Stub | Stripe webhook |
| `GET /api/v1/admin/users` | admin.py | ✅ Done | List users |
| `GET /api/v1/admin/stats` | admin.py | ⚠️ Stub | Dashboard stats |

### Frontend (`skyrate-ai-v2/frontend/`)

| Page | Status | Description |
|------|--------|-------------|
| `/` | ✅ Done | Landing page |
| `/sign-in` | ✅ Done | Login form |
| `/sign-up` | ✅ Done | Registration form |
| `/dashboard` | ⚠️ Basic | Main dashboard shell |
| `/consultant` | ⚠️ Basic | Consultant portal shell |
| `/vendor` | ⚠️ Basic | Vendor portal shell |
| `/admin` | ⚠️ Basic | Admin panel shell |

### Database Models

| Model | Status | Fields |
|-------|--------|--------|
| User | ✅ Done | id, email, password_hash, role, subscription_* |
| Subscription | ✅ Done | id, user_id, plan, status, stripe_* |
| ConsultantProfile | ✅ Done | company, states[], specializations[] |
| VendorProfile | ✅ Done | company, products[], coverage_states[] |
| QueryHistory | ✅ Done | user_id, query_text, results_count |
| Application | ✅ Done | ben, frn, status, analysis cache |
| AppealRecord | ✅ Done | application_id, strategy, documents |

---

## 🚀 Immediate Next Steps (Priority Order)

### Phase 2A: Port Business Logic (3-4 days)
1. Copy `skyrate-ai/utils/` → `skyrate-ai-v2/backend/app/services/`
2. Adapt for FastAPI (async where beneficial)
3. Create service wrappers for each utility

### Phase 2B: Complete API Endpoints (3-4 days)
1. **Query Endpoints**
   - Wire `query.py` to `usac_client.py`
   - Add NL interpretation via `ai_models.py`

2. **Consultant Endpoints**
   - `GET /denied` - Find denied applications with filters
   - `POST /appeal-strategy` - Generate appeal using `appeals_strategy.py`
   - `POST /analyze` - AI analysis of selected records

3. **Vendor Endpoints**
   - `GET /opportunities` - Form 470 leads with filters
   - `GET /equipment` - Equipment/manufacturer search
   - `POST /predictions` - AI predictions for funding likelihood

4. **Subscription Endpoints**
   - Complete Stripe integration
   - Webhook handling for subscription events

### Phase 2C: Frontend Features (5-7 days)
1. Dashboard with query interface
2. Results table with sorting/filtering
3. AI analysis panel
4. Consultant: Denied apps finder, appeal generator
5. Vendor: Opportunity scout, equipment search

### Phase 3: Deploy to DigitalOcean (1-2 days)
1. Set up App Platform or Droplet with Docker
2. Configure PostgreSQL database
3. Set up domain (skyrate.ai)
4. SSL certificate
5. Environment variables

---

## 💰 Pricing Configuration

Already configured in `backend/app/core/config.py`:

```python
# Consultants: $300/month or $3,000/year
CONSULTANT_MONTHLY_PRICE: int = 30000   # cents
CONSULTANT_YEARLY_PRICE: int = 300000   # cents

# Vendors: $200/month or $2,000/year
VENDOR_MONTHLY_PRICE: int = 20000       # cents
VENDOR_YEARLY_PRICE: int = 200000       # cents
```

---

## 🔑 Environment Variables Required

Create `.env` in `skyrate-ai-v2/backend/`:

```env
# App
DEBUG=false
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/skyrate

# AI APIs (at least one required)
GEMINI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
DEEPSEEK_API_KEY=your-key

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_CONSULTANT_MONTHLY_PRICE_ID=price_...
STRIPE_CONSULTANT_YEARLY_PRICE_ID=price_...
STRIPE_VENDOR_MONTHLY_PRICE_ID=price_...
STRIPE_VENDOR_YEARLY_PRICE_ID=price_...

# Email
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

---

## 🏃 Quick Start Commands

### Backend
```bash
cd skyrate-ai-v2/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
# API docs: http://localhost:8001/docs
```

### Frontend
```bash
cd skyrate-ai-v2/frontend
npm install
npm run dev
# App: http://localhost:3000
```

### VS Code Tasks (already configured)
- **Run SkyRate V2 Backend** - Starts FastAPI on port 8001

---

## 🎯 Competitive Features to Build

Based on competitor analysis (QueryBob, Funds For Learning):

### Must Have (Parity)
- [ ] Form 470 search with filters (state, service type, date)
- [ ] Form 471 FRN search with status filters
- [ ] Daily email alerts for new leads
- [ ] Export to CSV/Excel
- [ ] State/territory filtering

### Differentiators (AI-Powered)
- [ ] **Denial Analysis** - Parse FCDL comments, extract violation codes
- [ ] **Appeal Strategy Generator** - AI-written appeal recommendations
- [ ] **Funding Predictions** - Predict approval likelihood based on history
- [ ] **Application Monitoring** - Track applications, alert on status changes
- [ ] **Smart Lead Scoring** - Rank Form 470s by conversion potential
- [ ] **Equipment Recommendations** - Suggest products based on school needs

---

## 📊 Data Sources

| Dataset | Endpoint | Use Case |
|---------|----------|----------|
| Form 471 Applications | `srbr-2d59` | FRN search, status, amounts |
| Form 472 Disbursements | `jpiu-tj8h` | Invoice tracking, payment status |
| Form 470 Requests | TBD | Vendor leads, service requests |
| ECF Applications | `i5j4-3rvr` | Emergency Connectivity Fund |
| NCES Schools | `nces.ed.gov` | School enrichment data |

---

## 🐛 Known Issues

1. **Frontend auth store** - Uses Zustand, may need to sync with backend JWT
2. **CORS** - Verify frontend origin is in allowed list
3. **Rate limiting** - Need to add for USAC API calls
4. **Error handling** - Some endpoints need better error responses

---

## 📝 For Future AI Sessions

When starting a new chat, say:
> "Read PROJECT_STATUS.md in the opendata repo to understand the current state of SkyRate AI. We're building an E-Rate intelligence platform with AI-powered analysis."

The AI should then:
1. Read this file for context
2. Check git status for any pending changes
3. Review the immediate next steps section
4. Continue from where we left off

---

## 📞 Support

- **Repository:** erateapp.com/opendata
- **Domain:** skyrate.ai
- **Stack:** Next.js 14 + FastAPI + PostgreSQL + Stripe
