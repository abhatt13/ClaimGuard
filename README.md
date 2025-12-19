# 🛡️ ClaimGuard

**AI-Powered Insurance Claims Processing & Fraud Detection System**

*Student Budget Edition - Built to run on <$50/month*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![Gradio](https://img.shields.io/badge/Gradio-4.16-orange.svg)](https://gradio.app/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Budget Breakdown](#budget-breakdown)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Datasets](#datasets)
- [Deployment](#deployment)
- [Cost Optimization](#cost-optimization)

---

## 🎯 Overview

ClaimGuard is a production-grade insurance claims processing system powered by AI, designed specifically for **students** and **budget-conscious developers**. It demonstrates enterprise-level architecture while keeping costs under **$30/month**.

### Key Capabilities

1. **Multi-Modal Damage Assessment** - Analyze photos, videos, and repair estimates using AI vision
2. **Policy Coverage Analyzer** - RAG system with semantic search through policy documents
3. **LangGraph Workflow** - Automated claim routing (instant approval → detailed review → fraud investigation)
4. **Fraud Detection Engine** - ML + Neo4j graph analysis to identify suspicious patterns
5. **Automated Settlement** - Generate settlement offers and explanation letters

---

## ✨ Features

### 🔍 Intelligent Claim Processing
- **Automated damage assessment** using OpenAI Vision (gpt-4o-mini)
- **Policy coverage analysis** with RAG (Retrieval-Augmented Generation)
- **Smart routing** based on claim amount, fraud score, and coverage

### 🚨 Fraud Detection
- **ML-based detection** using XGBoost on historical claims data
- **Graph network analysis** using Neo4j to identify fraud rings
- **Composite scoring** combining multiple detection methods
- **Real-time pattern matching** across claimant history

### ⚡ Workflow Automation
- **LangGraph orchestration** for complex decision trees
- **Instant approval** for low-risk claims (<$5,000)
- **Escalation logic** for high-risk or complex cases
- **Human-in-the-loop** for edge cases

### 📊 Analytics & Visualization
- **Interactive dashboards** built with Gradio
- **Fraud network graphs** visualized with Pyvis
- **Real-time metrics** and performance tracking

---

## 💰 Budget Breakdown

### Monthly Costs (~$20-30)

| Service | Cost | Notes |
|---------|------|-------|
| **Local PostgreSQL** | **FREE** | Docker container |
| **Local Redis** | **FREE** | Docker container |
| **Neo4j Community** | **FREE** | Docker container |
| **Qdrant Local** | **FREE** | Docker container |
| **MinIO Storage** | **FREE** | Local S3-compatible |
| **OpenAI API** | **$20-30** | GPT-3.5-turbo + gpt-4o-mini |
| **Hosting (Optional)** | **FREE** | Railway/Render free tier |

### Cost Optimization Strategies

✅ **Use GPT-3.5-turbo** instead of GPT-4 (30x cheaper!)
✅ **Aggressive caching** (90% cache hit rate = 90% cost reduction)
✅ **Local models** (Ollama) for non-critical tasks
✅ **Batch processing** to reduce API calls
✅ **Sample datasets** instead of full datasets

**Total: ~$25/month** 🎉 (Well under your $50 budget!)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Async API framework
- **LangChain & LangGraph** - Workflow orchestration
- **SQLAlchemy** - ORM for PostgreSQL
- **Redis** - Caching & session management

### AI/ML
- **OpenAI** - GPT-3.5-turbo, gpt-4o-mini, embeddings
- **Scikit-learn & XGBoost** - Fraud detection models
- **OpenCV** - Image processing

### Databases
- **PostgreSQL** - Relational data (claims, policies, users)
- **Neo4j** - Graph database for fraud networks
- **Qdrant** - Vector database for RAG
- **Redis** - High-speed cache

### Frontend
- **Gradio** - Interactive ML/AI interfaces

### Infrastructure
- **Docker & Docker Compose** - Local development
- **MinIO** - S3-compatible object storage

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Git**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone the Repository

```bash
git clone https://github.com/abhatt13/ClaimGuard.git
cd ClaimGuard
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your favorite editor
```

**Required:** Add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start Docker Services

```bash
# Start all services (PostgreSQL, Redis, Neo4j, Qdrant, MinIO)
docker-compose up -d

# Check that all services are running
docker-compose ps
```

You should see all services healthy:
- ✅ claimguard-postgres
- ✅ claimguard-redis
- ✅ claimguard-neo4j
- ✅ claimguard-qdrant
- ✅ claimguard-minio

### 4. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py
```

### 6. Download Datasets (Sample)

```bash
# Download Kaggle fraud dataset (requires Kaggle API)
kaggle datasets download -d arpan129/insurance-fraud-detection
unzip insurance-fraud-detection.zip -d data/raw/kaggle_fraud/

# Download sample vehicle damage images
# (Instructions in docs/datasets.md)
```

### 7. Run the Application

```bash
# Terminal 1: Start FastAPI backend
uvicorn app.api.main:app --reload --port 8000

# Terminal 2: Start Gradio UI
python app/ui/app.py
```

### 8. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Gradio UI**: http://localhost:7860
- **Neo4j Browser**: http://localhost:7474 (user: neo4j, pass: claimguard123)
- **MinIO Console**: http://localhost:9001 (user: claimguard, pass: claimguard123)

---

## 📁 Project Structure

```
ClaimGuard/
├── app/
│   ├── api/                    # FastAPI routes
│   │   ├── main.py
│   │   └── routes/
│   │       ├── claims.py
│   │       ├── damage.py
│   │       ├── fraud.py
│   │       └── workflow.py
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Settings management
│   │   ├── database.py         # DB connections
│   │   └── security.py         # Auth & encryption
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   │   ├── damage/             # Damage assessment
│   │   ├── fraud/              # Fraud detection
│   │   ├── policy/             # Policy RAG
│   │   └── workflow/           # LangGraph workflows
│   ├── ml/                     # ML models & training
│   └── ui/                     # Gradio interface
├── data/                       # Datasets (gitignored)
├── scripts/                    # Utility scripts
├── tests/                      # Test suite
├── docker-compose.yml          # Local services
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## ⚙️ Configuration

All configuration is managed through environment variables in `.env`:

### Required Settings

```bash
# OpenAI API (REQUIRED)
OPENAI_API_KEY=sk-...

# Database (Auto-configured for Docker)
DATABASE_URL=postgresql://claimguard_user:claimguard_pass@localhost:5432/claimguard

# Security (Change in production!)
JWT_SECRET_KEY=your-secret-key-here
```

### Optional Settings

```bash
# Use local LLM instead of OpenAI (FREE)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Cost control
MAX_CLAIMS_PER_DAY=1000
RATE_LIMIT_PER_MINUTE=60
```

See `.env.example` for all available options.

---

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_fraud_detector.py
```

### Code Formatting

```bash
# Format code
black app/
isort app/

# Lint
flake8 app/
mypy app/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📊 Datasets

### Fraud Detection
- **Kaggle Insurance Fraud**: 15,420 records ([Download](https://www.kaggle.com/datasets/arpan129/insurance-fraud-detection))

### Vehicle Damage Images
- **VehiDE Dataset**: 13,945 images ([Paper](https://www.tandfonline.com/doi/full/10.1080/24751839.2024.2367387))
- **Roboflow Car Damage**: 300+ annotated images ([Download](https://universe.roboflow.com/car-damage-kadad/car-damage-images))

*Note: For budget reasons, use sample subsets during development*

---

## 🚢 Deployment

### Free Tier Options

#### Option 1: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

#### Option 2: Render
1. Connect GitHub repo
2. Create Web Service
3. Set environment variables
4. Deploy!

---

## 💡 Cost Optimization Tips

### 1. Maximize Cache Hits
```python
# All LLM responses are cached in Redis
# Aim for 90%+ cache hit rate
```

### 2. Use Cheaper Models
```python
# GPT-3.5-turbo for text: $0.001/1K tokens
# gpt-4o-mini for vision: $0.15/1M tokens
# vs GPT-4: $0.03/1K tokens (30x more expensive!)
```

### 3. Batch Processing
```python
# Process multiple images in one API call
# Use embeddings batch API
```

### 4. Local Models (FREE)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Run local Llama
ollama run llama2

# Update .env
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 👨‍💻 Author

**Aakash Bhatt** ([@abhatt13](https://github.com/abhatt13))

---

## 📚 Resources

- [Project Plan](/.claude/plans/logical-puzzling-cray.md)
- [API Documentation](http://localhost:8000/docs)
