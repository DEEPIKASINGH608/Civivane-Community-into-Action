<div align="center">

# 🌍 Civivane
### Real-Time Disaster Relief & Community Request Intelligence Command Center

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=flat&logo=react)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38Bdf8?style=flat&logo=tailwind-css)](https://tailwindcss.com/)
[![Leaflet GIS](https://img.shields.io/badge/Mapping-Leaflet%20%2F%20OpenStreetMap-199900?style=flat&logo=leaflet)](https://leafletjs.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![WebSockets](https://img.shields.io/badge/RealTime-WebSockets-000000?style=flat&logo=socketdotio)](https://fastapi.tiangolo.com/advanced/websockets/)

*Empowering emergency response teams, district administration, and local citizens with real-time geospatial intelligence, AI-assisted verification, instant request matching, and transparent disaster relief allocation.*

</div>

---

## 📌 Table of Contents

- [Executive Summary](#-executive-summary)
- [The Problem & Our Solution](#-the-problem--our-solution)
- [Key Architectural Capabilities](#-key-architectural-capabilities)
- [System Architecture & Workflow](#-system-architecture--workflow)
- [Comprehensive Directory Structure](#-comprehensive-directory-structure)
- [Detailed API Reference](#-detailed-api-reference)
- [Local Setup & Installation Guide](#-local-setup--installation-guide)
- [Database Migrations & Environment Configuration](#-database-migrations--environment-configuration)
- [Impact & Feasibility](#-impact--feasibility)
- [License](#-license)

---

## 📌 Executive Summary

During natural calamities, critical infrastructure breakdowns, or district-wide emergencies, relief agencies and local administration struggle with fragmented channels, delayed response times, unverified reports, and precise geographic tracking.

**Civivane** is an end-to-end civic intelligence and emergency response platform functioning as a unified Command Center. It enables citizens to log critical emergency needs—such as medical aid, clean water, food supplies, or emergency shelter—tagged with precise GPS coordinates. Simultaneously, it equips response teams with real-time WebSocket feeds, automated resource-matching algorithms, AI vision verification, and interactive GIS mapping.

---

## 💡 The Problem & Our Solution

| The Problem (Asli Samasya) | The Civivane Solution |
| :--- | :--- |
| **Fragmented Communication:** Chaos across scattered instant messaging groups makes tracking active incidents almost impossible. | **Centralized Request Intake:** A structured platform logging, categorizing, and routing all civic and emergency needs. |
| **Geographic Confusion:** Rescue teams waste critical time searching for vague or inaccurate address descriptions. | **Live GIS Mapping:** Real-time spatial tracking with Leaflet and OpenStreetMap rendering pinpoint locations. |
| **Fake or Duplicate Reports:** Crisis situations suffer from spam, inaccurate claims, or duplicated request entries. | **AI-Driven Vision & Verification:** Automated vision verification and data cleaning algorithms filtering incoming feeds. |
| **Manual Resource Matching:** Matching volunteer supplies with affected areas manually leads to critical delays. | **Automated Matching Engine:** Smart proximity and category matching engine pairing requirements directly with support pools. |

---

## 🚀 Key Architectural Capabilities

### 🧠 1. AI Intelligence Suite
- **Vision Verifier (`ai/vision_verifier.py`):** Inspects media uploads attached to incoming requests to verify crisis authenticity and prevent duplicate/spam logs.
- **Data Cleaner (`ai/data_cleaner.py`):** Normalizes user input, strips noise, and structures raw text into prioritized data models.
- **Multilingual Assistant (`ai/multilingual_assistant.py`):** Translates regional dialect submissions into actionable administrative reports.

### 🌐 2. Spatial & Real-Time Engine
- **Geospatial Processing (`services/geo_service.py`):** Calculates spatial bounds, proximity radii, and coordinate validation for incident mapping.
- **Resource Matching Engine (`services/matching_engine.py`):** Pairs incoming requests (`requests.py`) with available support infrastructure and volunteers (`support.py`) based on distance and severity.
- **WebSocket Broadcast Manager (`websockets/manager.py`):** Pushes instant event updates to the live command dashboard without requiring client polling.

### 🛡️ 3. Security & Access Control
- **JWT Authentication (`core/security.py`):** End-to-end token generation, password hashing (Bcrypt), and session protection.
- **Role-Based Endpoint Control:** Dedicated routes securing administrative write actions and public reporting triggers.

---

## 📂 Comprehensive Directory Structure

```text
civivane/
├── backend/
│   ├── alembic/                    # Database migration environment
│   │   ├── env.py                  # Alembic migration configuration
│   │   └── versions/              # Migration revision files
│   ├── app/
│   │   ├── ai/                     # AI & Verification Intelligence
│   │   │   ├── data_cleaner.py     # Input sanitization & normalization
│   │   │   ├── multilingual_assistant.py # Regional language processing
│   │   │   └── vision_verifier.py # Image verification engine
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/      # API Controllers
│   │   │           ├── analytics.py # District metrics & status feeds
│   │   │           ├── auth.py      # Registration & JWT token routes
│   │   │           ├── requests.py  # Incident creation & lifecycle
│   │   │           └── support.py   # Relief supply & volunteer allocation
│   │   ├── core/                   # System Configuration & Security
│   │   │   ├── config.py           # App settings & env loading
│   │   │   └── security.py         # Password hashing & JWT handlers
│   │   ├── db/                     # Persistence Layer
│   │   │   └── session.py          # SQLAlchemy session maker
│   │   ├── models/                 # ORM Database Schemas
│   │   │   └── domain.py           # Domain entities (Users, Requests, Relief)
│   │   ├── schemas/                # Pydantic Data Validation Models
│   │   │   └── schemas.py          # Request/Response payloads
│   │   ├── services/               # Core Business Logic
│   │   │   ├── geo_service.py      # GIS spatial operations
│   │   │   └── matching_engine.py # Resource matching algorithms
│   │   └── websockets/             # Real-time Broadcast System
│   │       └── manager.py          # Active WebSocket connection pool
│   ├── main.py                     # FastAPI application entry point
│   ├── .env                        # Local environment credentials
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable UI Components
│   │   │   └── CivicMap.jsx        # Leaflet interactive map controller
│   │   ├── pages/                  # Route Pages
│   │   │   └── Dashboard.jsx       # Command Center main view
│   │   ├── services/               # HTTP & WebSocket Client Setup
│   │   │   └── api.js              # Axios instance with interceptors
│   │   ├── App.jsx                 # Application layout & routes
│   │   ├── main.jsx                # React root mount
│   │   └── index.css               # Tailwind CSS directives
│   ├── package.json                # Frontend dependencies
│   └── vite.config.js              # Vite build configuration
├── docker-compose.yml              # Container orchestration setup
└── README.md                       # Documentation



🛠️ Detailed API Reference

    FastAPI automatically generates interactive OpenAPI documentation accessible at /docs when the backend is running. The API endpoints are structured as follows:

        For authentication, the Auth module provides a POST /api/v1/auth/register endpoint to register a new citizen or operator account with no authentication required, along with a POST /api/v1/auth/login endpoint to authenticate users and return a JWT Bearer token without requiring prior authorization.

        For managing incident logs, the Requests module offers a GET /api/v1/requests/ endpoint to fetch all active emergency requests publicly without authentication, and a POST /api/v1/requests/ endpoint to submit a new emergency request with precise coordinates which requires valid authorization (🔒 Yes).

        For resource management and metrics, the Support module provides a POST /api/v1/support/ endpoint to register available relief resources or aid requiring authorization, while the Analytics module provides a GET /api/v1/analytics/overview endpoint to fetch high-level summary metrics and heatmaps under authorized access.


⚙️ Local Setup & Installation Guide

    Prerequisites
        Python: v3.10 or higher
        Node.js: v18 or higher
        PostgreSQL: v14+ (or local SQLite for quick testing)
    Step 1: Clone the Repository

    git clone [https://github.com/DEEPIKASINGH608/civivane.git](https://github.com/DEEPIKASINGH608/civivane.git)

    cd civivane
    Step 2: Backend Setup

        1.Navigate to backend and create virtual environment
            cd backend
            python -m venv venv
        2.Activate Virtual Environment:
        Windows (PowerShell):
            .\venv\Scripts\Activate
        Linux/macOS:
            source venv/bin/activate
        3.Install Dependencies:
            pip install -r requirements.txt
        4.Configure Environment Variables:
            Create or verify the .env file in the backend/ directory:
                PROJECT_NAME="Civivane Command Center"
                SECRET_KEY="your_super_secret_jwt_key_here"
                ALGORITHM="HS256"
                ACCESS_TOKEN_EXPIRE_MINUTES=60
                DATABASE_URL="postgresql+psycopg://postgres:YourPassword@localhost:5432/civivane_db"

        5.Run Database Migrations
            alembic upgrade head
        6.Launch FastAPI Development Server:
            uvicorn main:app --reload --port 8000
        The Swagger API documentation will be live at http://127.0.0.1:8000/docs.

    Step 3: Frontend Setup

    1.Open a new terminal window and navigate to frontend/:

        cd frontend

    2.Install Node dependencies:
        npm install
    3.Start Development Server:
        npm run dev
    The Civivane Dashboard will be accessible at http://localhost:5173.



🧪 Workflow Verification Steps

    Open http://127.0.0.1:8000/docs.

    Register a user via POST /api/v1/auth/register.

    Obtain your token via POST /api/v1/auth/login.

    Store the JWT token in your browser local storage using DevTools (F12 -> Console):JavaScriptlocalStorage.setItem('token', 'YOUR_ACTUAL_JWT_TOKEN');

    Navigate to http://localhost:5173. Use the "+ Report Need" modal to submit an emergency request.

    Observe the incident render dynamically on the CivicMap interface.



🏆 Impact & Feasibility

    Immediate Humanitarian Impact: Accelerates dispatch times by cutting down geographic confusion through direct coordinate mapping.

    Robust Technical Architecture: Combines asynchronous Python handling (FastAPI) with client-side reactive rendering (React + Vite + Leaflet) for low-latency operations under heavy workloads.

    Scalable Deployment: Docker-ready infrastructure designed to deploy cleanly on cloud services (Render, Vercel, AWS, or local municipal servers).