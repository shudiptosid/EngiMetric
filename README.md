# EngiMetric

**AI-Powered Engineering Project Cost Estimation Platform**

EngiMetric is a full-stack SaaS application built for freelance engineers and agencies to accurately estimate, analyze, and quote engineering project costs. It combines a calibrated ML analytics engine with a professional dashboard to deliver data-driven pricing intelligence.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Screenshots](#screenshots)
- [License](#license)

---

## Features

### Intelligence Engine
- **5-Dimension Complexity Scoring** -- Hardware, Software, AI/ML, Deployment, and Risk/Safety dimensions (0-5 each, 25-point scale)
- **Monte Carlo Risk Simulation** -- 10,000-iteration probabilistic cost distribution with 90% confidence intervals
- **Acceptance Probability Model** -- Logistic regression-based client acceptance prediction with price sensitivity curves
- **Profit Margin Optimization** -- Revenue-maximizing margin calculation using acceptance-weighted expected value
- **Market-Calibrated Pricing** -- India-market benchmarks with auto-detected hourly rates and hardware cost estimation

### Multi-Model Cost Calculator
- **Hourly Model** -- Rate x Hours with risk buffer and profit margin
- **Fixed Price Model** -- Inclusive of hardware, software, and license costs
- **Complexity Multiplier Model** -- Base cost scaled by complexity factor (1x-4x)
- **Value-Based Model** -- Percentage of estimated client revenue impact
- **Modular Model** -- Per-module hour allocation (frontend, backend, testing, etc.)

### Professional Dashboard
- **Pro Dashboard** -- 7-panel analytics view with Acceptance Gauge, Optimal Price Card, Risk Card, Acceptance Curve, Profit Optimization, Monte Carlo Distribution, and Complexity Radar
- **Overview** -- Stats grid, quick actions, and recent project table
- **AI Analyzer** -- GPT-powered project description analysis with automatic complexity scoring
- **Proposal Generator** -- Export-ready PDF and DOCX quotations with branded templates
- **Document Workspace** -- Rich text editor and spreadsheet grid for notes and data
- **Project Management** -- Client project CRUD with complexity tracking

### Theme System
- **Dual Theme** -- Off-white (default) and dark mode with persistent toggle
- **CSS Variable Architecture** -- All colors driven by theme-aware custom properties
- **LocalStorage Persistence** -- Theme preference saved across sessions

---

## Architecture

```
EngiMetric
|
|-- backend/              FastAPI + Python
|   |-- main.py           Application entry point
|   |-- models.py         SQLAlchemy ORM models
|   |-- schemas.py        Pydantic request/response schemas
|   |-- auth.py           JWT authentication
|   |-- database.py       Async SQLite/PostgreSQL setup
|   |-- routes/           API route handlers
|   |   |-- analytics.py        Full analysis pipeline
|   |   |-- pricing_routes.py   Cost calculation endpoints
|   |   |-- project_routes.py   Project CRUD
|   |   |-- quotation_routes.py Proposal generation + PDF/DOCX export
|   |   |-- document_routes.py  Document workspace API
|   |   |-- ai_routes.py        GPT integration
|   |   |-- auth_routes.py      Login, signup, JWT refresh
|   |-- services/         Business logic layer
|       |-- analytics_engine.py  ML models, Monte Carlo, acceptance curves
|       |-- pricing_engine.py    Multi-model pricing calculations
|       |-- ai_service.py        OpenAI GPT integration
|       |-- export_service.py    PDF and DOCX generation (ReportLab, python-docx)
|
|-- frontend/             Next.js 16 + React
    |-- src/app/          App Router pages
    |   |-- dashboard/    All dashboard routes
    |   |   |-- pro-dashboard/   7-panel analytics dashboard
    |   |   |-- analytics/       AI Intelligence Engine
    |   |   |-- calculator/      Multi-model cost calculator
    |   |   |-- proposals/       Quotation manager
    |   |   |-- projects/        Project management
    |   |   |-- documents/       Rich text + spreadsheet workspace
    |   |   |-- analyzer/        GPT-powered project analyzer
    |   |   |-- settings/        User preferences
    |   |-- login/        Authentication pages
    |   |-- signup/
    |-- src/components/   Reusable UI components
    |   |-- AcceptanceGauge.tsx         ECharts gauge
    |   |-- AcceptanceCurve.tsx         Price vs probability curve
    |   |-- MonteCarloHistogram.tsx     Cost distribution histogram
    |   |-- ProfitOptimizationChart.tsx Revenue optimization curve
    |   |-- ComplexityRadar.tsx         5-axis radar chart
    |   |-- Sidebar.tsx                 Navigation sidebar
    |   |-- ThemeToggle.tsx             Light/dark mode toggle
    |   |-- StatsCard.tsx               Dashboard stat cards
    |-- src/lib/          Shared utilities
        |-- api.ts        Axios API client
        |-- auth.tsx      AuthProvider context
        |-- theme.tsx     ThemeProvider context
```

---

## Tech Stack

| Layer        | Technology                                                  |
|-------------|-------------------------------------------------------------|
| Frontend     | Next.js 16, React 19, TypeScript                           |
| Charts       | ECharts (echarts-for-react), Recharts                       |
| Icons        | Lucide React                                                |
| Styling      | CSS Variables, dual-theme architecture                      |
| Backend      | FastAPI, Python 3.11+                                       |
| Database     | SQLAlchemy 2.0 (SQLite dev / PostgreSQL prod)               |
| Auth         | JWT (python-jose), bcrypt password hashing                  |
| AI           | OpenAI GPT API                                              |
| Export       | ReportLab (PDF), python-docx (DOCX), openpyxl (XLSX)       |
| ML/Stats     | NumPy-free pure Python Monte Carlo and regression models    |

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm 9 or higher

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your settings

# Start the server
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`.

---

## Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template):

| Variable            | Description                          | Default              |
|--------------------|--------------------------------------|----------------------|
| `SECRET_KEY`        | JWT signing secret                   | (required)           |
| `DATABASE_URL`      | SQLAlchemy connection string         | `sqlite+aiosqlite:///./engineercost.db` |
| `OPENAI_API_KEY`    | OpenAI API key for GPT features      | (optional)           |
| `ALGORITHM`         | JWT algorithm                        | `HS256`              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry duration      | `1440`               |

---

## API Reference

### Authentication
| Method | Endpoint           | Description          |
|--------|--------------------|----------------------|
| POST   | `/api/auth/signup`  | Create new account   |
| POST   | `/api/auth/login`   | Login, returns JWT   |
| GET    | `/api/auth/me`      | Get current user     |

### Projects
| Method | Endpoint                | Description           |
|--------|-------------------------|-----------------------|
| GET    | `/api/projects`          | List user projects    |
| POST   | `/api/projects`          | Create project        |
| PUT    | `/api/projects/{id}`     | Update project        |
| DELETE | `/api/projects/{id}`     | Delete project        |

### Analytics
| Method | Endpoint                    | Description                      |
|--------|------------------------------|----------------------------------|
| POST   | `/api/analytics/full`        | Run full analysis pipeline       |
| POST   | `/api/analytics/complexity`  | Complexity scoring only          |
| POST   | `/api/analytics/price`       | Price prediction only            |

### Quotations
| Method | Endpoint                          | Description                  |
|--------|-----------------------------------|------------------------------|
| GET    | `/api/quotations`                  | List quotations              |
| POST   | `/api/quotations`                  | Create quotation             |
| GET    | `/api/quotations/{id}/pdf`         | Export as PDF                |
| GET    | `/api/quotations/{id}/docx`        | Export as DOCX               |

### Documents
| Method | Endpoint                   | Description              |
|--------|----------------------------|--------------------------|
| GET    | `/api/documents`            | List documents           |
| POST   | `/api/documents`            | Create document          |
| PUT    | `/api/documents/{id}`       | Update document          |
| DELETE | `/api/documents/{id}`       | Delete document          |

### AI
| Method | Endpoint            | Description                              |
|--------|---------------------|------------------------------------------|
| POST   | `/api/ai/analyze`    | GPT-powered project complexity analysis  |

---

## Screenshots

> Screenshots can be added here after deployment or by capturing local development views.

---

## License

All rights reserved. This is a private repository. No part of this codebase may be reproduced, distributed, or used without explicit written permission from the author.

---

Built by [shudiptosid](https://github.com/shudiptosid)
