# EngiMetric

### Engineering Financial Intelligence Platform

> Stop guessing project prices. Start knowing them.

Engineers lose money or clients because they price projects by gut feel. EngiMetric uses ML-calibrated analytics, India-market benchmarks, and acceptance probability modeling to give you data-driven pricing intelligence — so every quote is competitive, profitable, and backed by math.

---

## The Problem

- Freelance engineers **underquote** and lose profit, or **overquote** and lose clients
- No structured way to score project complexity across hardware, software, AI, deployment, and risk
- No visibility into whether a quoted price will actually be accepted
- Pricing is done on spreadsheets with no market calibration

## The Solution

EngiMetric gives you a 4-step pricing pipeline:

1. **Score** — Rate your project across 5 complexity dimensions (0-5 each, 25-point scale)
2. **Analyze** — AI estimates hours, cost, risk, and acceptance probability using India-market benchmarks
3. **Price** — Get ML-predicted pricing with confidence intervals, or calculate manually
4. **Propose** — Generate branded PDF/DOCX quotations ready to send

## Target Users

- **Freelance engineers** — IoT, embedded, automation, full-stack
- **Small agencies** (2-10 people) — need consistent quoting across team members
- **Technical consultants** — hardware + software project costing

---

## How It Works

### Intelligence Engine

The core of EngiMetric. Calibrated against 10 real India-market benchmark projects and 15 complexity reference points.

- **5-Dimension Complexity Scoring** — Hardware, Software, AI/ML, Deployment, Risk/Safety (0-5 each)
- **Monte Carlo Risk Simulation** — 5,000-iteration probabilistic cost distribution with 90% confidence intervals
- **Acceptance Probability** — Logistic regression model predicting client acceptance at any price point
- **Profit Margin Optimization** — Finds the margin that maximizes expected revenue (price × acceptance probability)
- **User Hours Override** — System estimates hours, but you can override with your own completion time. Pricing recalculates automatically.

#### Rate Detection

Auto-detects hourly rates from the `MARKET_RATES` table based on your project's complexity tier:
| Tier | Rate Range (₹/hr) |
|------|-------------------|
| Normal (0-6) | ₹500 – ₹800 |
| Moderate (7-12) | ₹800 – ₹1,200 |
| High (13-18) | ₹1,200 – ₹2,000 |
| Industrial (19-25) | ₹2,000 – ₹2,500 |

Set your hourly rate to **0** for auto-detection, or enter your own value.

#### Hardware Estimation

Interpolates hardware costs from 10 India-market benchmark projects spanning ₹900 (basic sensor kit) to ₹10,00,000 (smart factory). Set hardware cost to **0** for auto-estimation, or enter your own.

### Cost Calculator

Two modes for different workflows:

- **Smart AI Pricing** (recommended) — Score complexity, get AI-recommended price with acceptance analysis
- **Manual Override** — Direct rate × hours + materials + risk + profit calculation

All 5 backend pricing models (hourly, fixed, value-based, complexity multiplier, modular) remain available via API.

### Dashboard

Business-level metrics at a glance:

- Win Rate, Conversion Rate, Monthly Revenue Forecast, Avg Project Value
- Revenue trend chart
- Recent projects table with complexity and status tracking

### AI Analyzer

GPT-powered project description analysis — paste your project brief and get automatic complexity scoring suggestions.

### Proposals

Export-ready PDF and DOCX quotations with branded templates. Attached to projects for tracking.

---

## Why EngiMetric Is Different

| Feature                | Spreadsheet | Generic SaaS | EngiMetric                                       |
| ---------------------- | ----------- | ------------ | ------------------------------------------------ |
| Complexity scoring     | Manual      | Generic      | 5-dimension, calibrated                          |
| Price prediction       | Formula     | Template     | ML-blended (60% formula + 40% benchmark)         |
| Acceptance probability | None        | None         | Logistic regression with client-type adjustments |
| Risk simulation        | None        | Basic        | 5,000-iteration Monte Carlo                      |
| Market calibration     | None        | US-centric   | India-market 2026 benchmarks                     |
| User hours override    | N/A         | N/A          | AI estimate + your override, side-by-side        |

---

## Pricing Plans

|                     | Free  | Pro         | Agency    |
| ------------------- | ----- | ----------- | --------- |
| Projects/month      | 3     | Unlimited   | Unlimited |
| Intelligence Engine | Basic | Full        | Full      |
| PDF/DOCX Export     | —     | ✓           | ✓         |
| Team Members        | 1     | 1           | Up to 10  |
| Price               | Free  | ₹499–999/mo | ₹1,999/mo |

---

## Tech Stack

| Layer    | Technology                                                  |
| -------- | ----------------------------------------------------------- |
| Frontend | Next.js 16, React 19, TypeScript                            |
| Charts   | ECharts (echarts-for-react), Recharts                       |
| Icons    | Lucide React                                                |
| Styling  | CSS Variables, dual-theme (light + dark)                    |
| Backend  | FastAPI, Python 3.11+                                       |
| Database | SQLAlchemy 2.0 (SQLite dev / PostgreSQL prod)               |
| Auth     | JWT (python-jose), bcrypt                                   |
| AI       | OpenAI GPT API                                              |
| Export   | ReportLab (PDF), python-docx (DOCX)                         |
| ML/Stats | Pure Python Monte Carlo, logistic regression, interpolation |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:3000`

### Environment Variables

| Variable         | Description                  | Default                                 |
| ---------------- | ---------------------------- | --------------------------------------- |
| `SECRET_KEY`     | JWT signing secret           | (required)                              |
| `DATABASE_URL`   | SQLAlchemy connection string | `sqlite+aiosqlite:///./engineercost.db` |
| `OPENAI_API_KEY` | OpenAI API key (optional)    | —                                       |

---

## API Reference

### Auth

| Method | Endpoint           | Description    |
| ------ | ------------------ | -------------- |
| POST   | `/api/auth/signup` | Create account |
| POST   | `/api/auth/login`  | Login → JWT    |
| GET    | `/api/auth/me`     | Current user   |

### Analytics

| Method | Endpoint                             | Description                                                                                          |
| ------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| POST   | `/api/analytics/full`                | Full analysis pipeline (complexity + hours + price + acceptance + Monte Carlo + profit optimization) |
| POST   | `/api/analytics/complexity-score`    | Complexity scoring only                                                                              |
| POST   | `/api/analytics/predict-price`       | Price prediction only                                                                                |
| POST   | `/api/analytics/acceptance`          | Acceptance probability                                                                               |
| POST   | `/api/analytics/monte-carlo`         | Risk simulation                                                                                      |
| POST   | `/api/analytics/profit-optimization` | Margin optimization                                                                                  |

### Projects & Quotations

| Method     | Endpoint                                 | Description              |
| ---------- | ---------------------------------------- | ------------------------ |
| GET/POST   | `/api/projects/`                         | List / Create projects   |
| PUT/DELETE | `/api/projects/{id}`                     | Update / Delete          |
| GET/POST   | `/api/quotations/`                       | List / Create quotations |
| GET        | `/api/quotations/{id}/export?format=pdf` | Export PDF/DOCX          |

### AI

| Method | Endpoint                     | Description          |
| ------ | ---------------------------- | -------------------- |
| POST   | `/api/ai/analyze-complexity` | GPT project analysis |

---

## Roadmap

- [ ] Stripe/Razorpay billing integration
- [ ] Team workspaces with role-based access
- [ ] Historical intelligence — learn from past projects to improve predictions
- [ ] Client portal — share proposals with clients for online approval
- [ ] Multi-currency support

---

## License

All rights reserved. Private repository. No reproduction without written permission.

---

Built by [shudiptosid](https://github.com/shudiptosid)
