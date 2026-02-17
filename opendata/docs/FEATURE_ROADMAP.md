# SkyRate AI v2 - Feature Roadmap

**Last Updated:** January 15, 2025  
**Target Launch:** Q1 2025  
**Domain:** skyrate.ai

---

## 🎯 Vision

Build the most intelligent E-Rate platform that helps:
- **Vendors** find and win more E-Rate business through AI-powered lead scoring
- **Consultants** serve more schools with AI-powered appeal generation and monitoring

---

## 📅 Release Schedule

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Working authentication and basic portal functionality

### Phase 2: Core Features (Weeks 3-4)  
**Goal:** Feature parity with competitors + AI query engine

### Phase 3: AI Differentiation (Weeks 5-6)
**Goal:** Launch AI-powered features that competitors lack

### Phase 4: Production Launch (Week 7)
**Goal:** Public beta on skyrate.ai

---

## 🔧 Phase 1: Foundation

### 1.1 Authentication System
- [x] Backend JWT authentication (`/api/v1/auth/*`)
- [x] User model with roles (consultant, vendor, admin)
- [ ] Frontend sign-in page wired to API
- [ ] Frontend sign-up page with role selection
- [ ] Password reset flow
- [ ] Email verification

### 1.2 Subscription System  
- [x] Stripe checkout session creation
- [x] Webhook handler for payment events
- [x] Subscription model with status tracking
- [ ] Frontend pricing page
- [ ] Frontend subscription management page
- [ ] Trial period handling (14 days)

### 1.3 User Dashboard
- [ ] Role-based dashboard routing
- [ ] Subscription status display
- [ ] Quick actions sidebar
- [ ] Recent activity feed

---

## 🏢 Phase 2: Core Features

### 2.1 Vendor Portal Features

#### 2.1.1 Form 470 Lead Search
**Parity with QueryBob**
- [x] Backend search endpoint (`POST /api/v1/vendor/search`)
- [ ] Frontend search form with filters:
  - State/region
  - Service category (C1/C2)
  - Equipment type keyword
  - Date range
  - Budget range
- [ ] Search results table with:
  - School name and BEN
  - Request details
  - Estimated budget
  - Posted date
  - Quick actions (save, export, contact)

#### 2.1.2 Lead Management
- [x] Save search functionality
- [x] Search history
- [ ] Saved leads list
- [ ] Lead status tracking (contacted, proposal sent, won, lost)
- [ ] Export leads to CSV

#### 2.1.3 Entity Analysis
- [ ] School profile view
  - BEN details
  - Funding history
  - Category 2 budget remaining
  - Past vendors/contracts
- [ ] District-level aggregation

#### 2.1.4 Email Alerts
- [ ] Daily lead digest email
- [ ] Configurable alert preferences
- [ ] Instant alerts for high-value leads

### 2.2 Consultant Portal Features

#### 2.2.1 School Portfolio Management
- [x] Add schools to portfolio
- [x] CSV bulk import
- [x] School list view
- [ ] School detail view with:
  - Current applications
  - Historical funding
  - Denial history
  - Contact information

#### 2.2.2 FRN Monitoring
**Parity with QueryBob FRN Monitor ($150/mo value - included)**
- [ ] Automatic status tracking for portfolio schools
- [ ] Status change detection
- [ ] PIA question alerts
- [ ] Commitment decision alerts
- [ ] Funding status alerts

#### 2.2.3 Application Dashboard
- [ ] Visual pipeline of all applications
- [ ] Status breakdown charts
- [ ] Filterable/sortable application table
- [ ] Bulk actions

#### 2.2.4 Reporting
- [ ] Portfolio summary PDF
- [ ] School-specific reports
- [ ] Funding year comparison
- [ ] Custom branding option

---

## 🤖 Phase 3: AI Differentiation

### 3.1 Natural Language Query Engine
**No competitor offers this**

#### Features
- [ ] Chat-style interface
- [ ] Natural language to USAC query translation
- [ ] Context-aware follow-up questions
- [ ] Query suggestions

#### Example Queries
```
"Show me denied applications in Texas over $50,000"
"Find schools that applied for Cisco routers last year"  
"Which of my portfolio schools have PIA questions pending?"
"Compare funding for district XYZ across the last 3 years"
```

### 3.2 AI Lead Scoring (Vendors)
**No competitor offers this**

#### Features
- [ ] Probability score for each 470 lead
- [ ] Factors considered:
  - School's historical vendor preferences
  - Timing in funding cycle
  - Budget availability
  - Competition level
  - Geographic proximity
- [ ] Ranked lead lists
- [ ] "Hot leads" alerts

### 3.3 AI Appeal Generation (Consultants)
**No competitor offers this**

#### Features
- [x] Backend endpoint (`POST /api/v1/consultant/appeal`)
- [ ] Denial reason analysis
- [ ] Appeal letter generation with:
  - Policy citations
  - Evidence recommendations
  - Success probability
- [ ] One-click evidence pack assembly
- [ ] Appeal tracking

#### Appeal Workflow
1. User selects denied FRN
2. AI analyzes denial reason
3. AI generates appeal letter draft
4. User reviews and edits
5. AI suggests supporting evidence
6. One-click export as PDF/DOCX

### 3.4 Funding Predictions (Vendors)
**No competitor offers this**

#### Features
- [ ] Timeline prediction: "When will this school receive funding?"
- [ ] Batch predictions for lead prioritization
- [ ] Historical accuracy tracking

### 3.5 Proactive Alerts (Consultants)
**Competitors only offer reactive alerts**

#### Features
- [ ] AI pattern recognition
- [ ] "This application has patterns similar to denied applications"
- [ ] Recommended preventive actions
- [ ] Risk scoring for pending applications

---

## 🚀 Phase 4: Production Launch

### 4.1 Infrastructure
- [ ] DigitalOcean Droplet setup
- [ ] PostgreSQL database provisioned
- [ ] Domain configured (skyrate.ai)
- [ ] SSL certificates
- [ ] CDN for static assets

### 4.2 Deployment
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Environment variables configured
- [ ] Database migrations
- [ ] Health checks and monitoring

### 4.3 Stripe Production
- [ ] Live mode enabled
- [ ] Price IDs created:
  - Vendor Monthly ($200)
  - Vendor Annual ($2,000)
  - Consultant Monthly ($300)
  - Consultant Annual ($3,000)
- [ ] Webhook endpoint verified
- [ ] Tax handling configured

### 4.4 Launch Checklist
- [ ] Security audit
- [ ] Performance testing
- [ ] Email deliverability verified
- [ ] Support email configured
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] Documentation/help center

---

## 📊 Success Metrics

### Phase 1 Completion Criteria
- [ ] User can sign up, sign in, and see dashboard
- [ ] Stripe checkout flow works end-to-end
- [ ] Role-based routing works correctly

### Phase 2 Completion Criteria
- [ ] Vendor can search and save leads
- [ ] Consultant can manage school portfolio
- [ ] FRN status monitoring works
- [ ] Basic email alerts functional

### Phase 3 Completion Criteria
- [ ] Natural language queries return relevant results
- [ ] Appeal generation produces quality letters
- [ ] Lead scoring improves vendor efficiency
- [ ] Users report AI features as valuable

### Phase 4 Completion Criteria
- [ ] Site is live at skyrate.ai
- [ ] Payment processing works
- [ ] < 500ms API response times
- [ ] 99.9% uptime target

---

## 🔮 Future Phases (Post-Launch)

### Phase 5: Enterprise Features
- White-label school portals
- Team/organization accounts
- API access for integrations
- Custom reporting

### Phase 6: Integrations
- Salesforce connector
- HubSpot connector
- Zapier integration
- Webhook notifications

### Phase 7: Advanced AI
- Contract analysis
- Competitive intelligence
- Market trend predictions
- Automated RFP responses

---

## 📝 Technical Debt Tracking

### Known Issues
- [ ] v2 backend imports from skyrate-ai/utils via sys.path hack
- [ ] SQLite used for dev (needs PostgreSQL migration scripts)
- [ ] Frontend auth not wired to backend
- [ ] No rate limiting on API

### Refactoring Needs
- [ ] Move utils to shared package
- [ ] Add comprehensive error handling
- [ ] Implement request validation
- [ ] Add API documentation (OpenAPI)
- [ ] Add unit tests

---

## 📋 Sprint Planning Template

### Sprint N (Week X)
**Goal:** [Single sentence goal]

**Tasks:**
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Demo:** [What to show at end of sprint]

---

*Roadmap maintained for project planning and AI assistant continuity.*
