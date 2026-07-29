# OpenSnap

An open-source, privacy-first alternative to Snapchat.

## Features
- **Open Architecture**: Complete visibility into code, data flows, and moderation
- **Privacy-First**: Data minimization, user-owned data, opt-out personalization
- **Community-Governed**: Not controlled by a single corporate entity
- **Cross-Platform**: iOS/Android via Valdi framework

## Tech Stack
- **Frontend**: Valdi (TypeScript, native views)
- **Backend**: FastAPI (Python), PostgreSQL, KeyDB
- **Recommendations**: Apache Flink, Hopsworks, PyTorch
- **Moderation**: HuggingFace Transformers + HITL dashboard
- **Storage**: MinIO (S3-compatible)
- **Infrastructure**: Kubernetes, Terraform

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- KeyDB (or Redis)

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourorg/opensnap.git
cd opensnap

# Set up environment
cp .env.example .env
# Edit .env with your configurations

# Run infrastructure locally
docker-compose up -d postgres redis minio

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload

# Install frontend dependencies
cd ../frontend/valdi
npm install
npm run dev

# Run recommendation engine (requires Kafka setup)
cd ../recommendation
python -m flink_jobs.feature_update
