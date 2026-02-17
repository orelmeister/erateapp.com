# SkyRate AI v2 - Project Status & Continuation Guide

**Last Updated:** January 15, 2025  
**Domain:** skyrate.ai  
**Deployment Target:** DigitalOcean  
**Status:** Active Development

---

## 🎯 Executive Summary

SkyRate AI is an AI-powered E-Rate intelligence platform serving two customer segments:
1. **E-Rate Consultants** - Help schools apply for and manage E-Rate funding
2. **Service Providers/Vendors** - Sell products/services to E-Rate funded schools

### Key Decision: STREAMLIT IS DEPRECATED
> ⚠️ **IMPORTANT:** The `skyrate-ai/` Streamlit application is NO LONGER the target platform.  
> All development focuses on `skyrate-ai-v2/` (Next.js frontend + FastAPI backend).

---

## 💰 Pricing Model

| User Type | Monthly | Annual | Target Value |
|-----------|---------|--------|--------------|
| **Vendors** | $200/month | $2,000/year | Form 470 leads, school discovery |
| **Consultants** | $300/month | $3,000/year | Portfolio management, appeal generation |

---

## 🏗️ Architecture

```
opendata/
├── skyrate-ai-v2/           # ← PRODUCTION TARGET
│   ├── frontend/            # Next.js 14 + React + Tailwind
│   │   ├── app/             # App Router pages
│   │   │   ├── admin/       # Admin dashboard
│   │   │   ├── consultant/  # Consultant portal
│   │   │   ├── vendor/      # Vendor portal  
│   │   │   ├── dashboard/   # Main dashboard
│   │   │   ├── sign-in/     # Authentication
│   │   │   └── sign-up/     # Registration
│   │   └── lib/             # Utilities
│   │
│   └── backend/             # FastAPI Python
│       ├── app/
│       │   ├── api/v1/      # API endpoints
│       │   │   ├── auth.py       # Authentication
│       │   │   ├── consultant.py # Consultant features
│       │   │   ├── vendor.py     # Vendor features
│       │   │   ├── query.py      # NL queries
│       │   │   ├── subscriptions.py # Stripe payments
│       │   │   └── admin.py      # Admin features
│       │   ├── core/        # Config, security, DB
│       │   └── models/      # SQLAlchemy models
│       └── requirements.txt
│
├── skyrate-ai/              # ⛔ DEPRECATED - Streamlit (reference only)
│   └── utils/               # ✅ REUSABLE - Business logic imported by v2
│       ├── ai_models.py     # AI model manager (Gemini, DeepSeek, Claude)
│       ├── usac_client.py   # USAC/Socrata data fetching
│       ├── denial_analyzer.py    # Denial reason analysis
│       ├── appeals_strategy.py   # Appeal generation
│       ├── evidence_pack.py      # Evidence document creation
│       ├── email_sender.py       # Email automation
│       └── enrichment.py         # BEN/school enrichment
│
└── usac-mcp-server/         # MCP server for Claude Desktop
```

---

## 🔧 Tech Stack

### Frontend (skyrate-ai-v2/frontend)
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** Zustand + React Query
- **UI Components:** Radix UI primitives
- **Auth:** NextAuth.js (planned)
- **Tables:** TanStack Table

### Backend (skyrate-ai-v2/backend)
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** PostgreSQL (production) / SQLite (development)
- **ORM:** SQLAlchemy
- **Auth:** JWT (python-jose)
- **Payments:** Stripe

### AI Models (via skyrate-ai/utils/ai_models.py)
- Google Gemini 2.0 Flash (primary)
- DeepSeek Chat (backup)
- Anthropic Claude 3.5 Sonnet (premium)

### Data Sources
- USAC Open Data via Socrata API
- FCC Form 470/471 databases

---

## 📊 Current Implementation Status

### Services Layer (NEW - January 15, 2025)

The services layer wraps legacy `skyrate-ai/utils/` business logic for FastAPI.

| Service | File | Status | Description |
|---------|------|--------|-------------|
| `USACService` | `services/usac_service.py` | ✅ Complete | Form 470/471 data, FRN line items, enrichment |
| `AIService` | `services/ai_service.py` | ✅ Complete | Multi-model AI routing (Gemini/DeepSeek/Claude) |
| `DenialService` | `services/denial_service.py` | ✅ Complete | FCDL parsing, violation analysis, deadlines |
| `AppealsService` | `services/appeals_service.py` | ✅ Complete | Strategy generation, timelines, checklists |

**Usage Example:**
```python
from app.services import get_usac_service, get_denial_service

usac = get_usac_service()
denied = usac.search_denied_applications(year=2025, state="TX", min_amount=50000)

denial = get_denial_service()
details = denial.get_denial_details(application_number="251000123")
```

### Backend API Endpoints

| Endpoint | Status | Notes |
|----------|--------|-------|
| `POST /api/v1/auth/register` | ✅ Complete | User registration |
| `POST /api/v1/auth/login` | ✅ Complete | JWT authentication |
| `GET /api/v1/auth/me` | ✅ Complete | Current user info |
| `GET /api/v1/subscriptions/status` | ✅ Complete | Subscription check |
| `POST /api/v1/subscriptions/create-checkout` | ✅ Complete | Stripe checkout |
| `POST /api/v1/subscriptions/webhook` | ✅ Complete | Stripe webhooks |
| **Consultant Portal** | | |
| `GET/PUT /api/v1/consultant/profile` | ✅ Complete | Profile CRUD |
| `GET/POST /api/v1/consultant/schools` | ✅ Complete | Portfolio management |
| `POST /api/v1/consultant/upload-csv` | ✅ Complete | Bulk school import |
| `POST /api/v1/consultant/appeal` | 🔄 Partial | Appeal generation - wire to AppealsService |
| **Vendor Portal** | | |
| `GET/PUT /api/v1/vendor/profile` | ✅ Complete | Profile CRUD |
| `POST /api/v1/vendor/search` | ✅ Complete | School/lead search |
| `GET /api/v1/vendor/search/history` | ✅ Complete | Search history |
| **Query Engine** | | |
| `POST /api/v1/query/natural` | 🔄 Partial | Wire to AIService + USACService |
| `POST /api/v1/query/direct` | 🔄 Partial | Wire to USACService |

### Frontend Pages

| Page | Status | Notes |
|------|--------|-------|
| `/` | ✅ Complete | Landing page |
| `/sign-in` | 🔄 Scaffolded | Needs API integration |
| `/sign-up` | 🔄 Scaffolded | Needs API integration |
| `/dashboard` | 🔄 Scaffolded | Basic layout |
| `/consultant/*` | 🔄 Scaffolded | Basic structure |
| `/vendor/*` | 🔄 Scaffolded | Basic structure |
| `/admin/*` | 🔄 Scaffolded | Basic structure |

### Database Models

| Model | Status | Fields |
|-------|--------|--------|
| `User` | ✅ Complete | id, email, password_hash, role, created_at |
| `Subscription` | ✅ Complete | plan, status, stripe_id, start_date, end_date |
| `ConsultantProfile` | ✅ Complete | company_name, contact_name, phone, website |
| `ConsultantSchool` | ✅ Complete | ben, frn, school_name, state, tags |
| `VendorProfile` | ✅ Complete | company_name, service_types, target_states |
| `VendorSearch` | ✅ Complete | search_params, results_count |

---

## 🏆 Competitor Analysis Summary

See [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) for detailed analysis.

### QueryBob (querybob.com)
- **Pricing:** $250 baseline + $300/month or $3,000/year
- **Key Features:** Form 470 leads, FRN monitoring ($150/mo add-on), PDF reports, CRM APIs

### FundsForLearning (fundsforlearning.com)  
- **Pricing:** Quote-based, free tier for applicants
- **Key Features:** E-rate Manager platform, deadline alerts, application tracking

### Our Differentiation (AI-Powered)
| Feature | Competitors | SkyRate AI |
|---------|-------------|------------|
| Lead discovery | Basic filters | AI-ranked predictions |
| Denial handling | Manual review | AI appeal generation |
| Funding timing | Not available | Predictive analytics |
| Monitoring | Email alerts | Proactive AI insights |

---

## 🚀 Deployment Plan

### Target: DigitalOcean

**Infrastructure:**
- 1x Droplet (Basic, $12/mo) - API + DB
- OR App Platform ($5/mo) for auto-scaling
- Managed PostgreSQL ($15/mo) for production

**Domain Setup:**
- Primary: skyrate.ai
- API: api.skyrate.ai
- App: app.skyrate.ai

**Environment Variables Required:**
```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/skyrate

# JWT
SECRET_KEY=<generate-secure-key>

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# AI Models
GEMINI_API_KEY=...
DEEPSEEK_API_KEY=...
ANTHROPIC_API_KEY=...

# Email
GMAIL_USER=...
GMAIL_APP_PASSWORD=...
```

---

## 📋 Next Steps Priority

### Phase 1: Core Platform (Week 1-2)
1. [ ] Complete frontend authentication flow
2. [ ] Wire up consultant portal to backend APIs  
3. [ ] Wire up vendor portal to backend APIs
4. [ ] Implement Stripe subscription flow end-to-end

### Phase 2: AI Features (Week 3-4)
1. [ ] Natural language query with AI responses
2. [ ] Appeal letter generation with AI
3. [ ] Funding prediction model for vendors
4. [ ] FRN monitoring with proactive alerts

### Phase 3: Production (Week 5-6)
1. [ ] Deploy to DigitalOcean
2. [ ] Configure domain (skyrate.ai)
3. [ ] Set up production database
4. [ ] Enable Stripe live mode
5. [ ] Launch beta to select users

---

## 🔗 Quick Start Commands

### Run Backend (FastAPI)
```powershell
cd skyrate-ai-v2/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Run Frontend (Next.js)
```powershell
cd skyrate-ai-v2/frontend
npm run dev
```

### Run Both (VS Code Tasks)
Use the VS Code tasks:
- "Run SkyRate V2 Backend" (port 8001)
- Frontend needs manual `npm run dev` (port 3000)

---

## 📁 Key Files Reference

| Purpose | File Path |
|---------|-----------|
| Backend entry | `skyrate-ai-v2/backend/app/main.py` |
| Config/env | `skyrate-ai-v2/backend/app/core/config.py` |
| Consultant API | `skyrate-ai-v2/backend/app/api/v1/consultant.py` |
| Vendor API | `skyrate-ai-v2/backend/app/api/v1/vendor.py` |
| Subscriptions | `skyrate-ai-v2/backend/app/api/v1/subscriptions.py` |
| AI Models | `skyrate-ai/utils/ai_models.py` |
| USAC Client | `skyrate-ai/utils/usac_client.py` |
| Appeal Logic | `skyrate-ai/utils/appeals_strategy.py` |
| **Services Layer** | |
| USAC Service | `skyrate-ai-v2/backend/app/services/usac_service.py` |
| AI Service | `skyrate-ai-v2/backend/app/services/ai_service.py` |
| Denial Service | `skyrate-ai-v2/backend/app/services/denial_service.py` |
| Appeals Service | `skyrate-ai-v2/backend/app/services/appeals_service.py` |
| Frontend layout | `skyrate-ai-v2/frontend/app/layout.tsx` |

---

## 🤖 For AI Assistants

When continuing this project:

1. **Do NOT** work on `skyrate-ai/` Streamlit app - it's deprecated
2. **DO** focus on `skyrate-ai-v2/` (backend + frontend)
3. **REUSE** business logic from `skyrate-ai/utils/` (imported by v2 backend)
4. **Reference** competitor features in COMPETITOR_ANALYSIS.md
5. **Follow** the pricing model: Vendors $200/$2k, Consultants $300/$3k
6. **Target** DigitalOcean for deployment, domain skyrate.ai

### Key AI Differentiators to Build
- Predictive analytics for funding timing (vendors)
- AI-generated appeal letters with high success rate (consultants)
- Natural language queries ("show me denied schools in Texas over $100k")
- Proactive monitoring with intelligent alerts

---

*Document maintained for project continuity across AI assistant sessions.*
