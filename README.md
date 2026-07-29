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

Deployment
See docs/deployment_guide.md for Kubernetes/Helm deployment instructions.

Contributing
We welcome contributions! Please read CONTRIBUTING.md for guidelines.

License
MIT License - See LICENSE file for details.

Transparency Report
All code is open and auditable. The platform is designed for community governance. See docs/governance.md.

Note: This project is in active development. APIs and architecture are subject to change.


---

### 9. Docker Compose: `docker-compose.yml`
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: opensnap
      POSTGRES_PASSWORD: opensnap
      POSTGRES_DB: opensnap
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  keydb:
    image: eqalpha/keydb:latest
    ports:
      - "6379:6379"
    volumes:
      - keydb_data:/data
    command: keydb-server /etc/keydb/keydb.conf --appendonly yes

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

  kafka:
    image: bitnami/kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_CFG_NODE_ID: 0
      KAFKA_CFG_PROCESS_ROLES: controller,broker
      KAFKA_CFG_CONTROLLER_QUORUM_VOTERS: 0@kafka:9093
      KAFKA_CFG_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_CFG_CONTROLLER_LISTENER_NAMES: CONTROLLER

  zookeeper:
    image: bitnami/zookeeper:latest
    ports:
      - "2181:2181"
    environment:
      ALLOW_ANONYMOUS_LOGIN: "yes"

volumes:
  postgres_data:
  keydb_data:
  minio_data:
