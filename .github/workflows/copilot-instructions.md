# GitHub Copilot Agent Instructions for OpenSnap Development

## Project Context
OpenSnap is an open-source alternative to Snapchat. The goal is to create a transparent, privacy-first, community-governed platform.

## Architecture Summary
- **Frontend**: Valdi (Snap's open-source cross-platform framework), TypeScript/TSX
- **Backend**: FastAPI (Python), PostgreSQL, KeyDB (Redis-compatible)
- **Recommendations**: Apache Flink, Hopsworks feature store, PyTorch
- **Moderation**: HuggingFace Transformers, HITL React dashboard
- **Storage**: MinIO (S3-compatible)
- **Observability**: Prometheus, Grafana

## Copilot Behavior Guidelines
1. **Code Style**: Use Python type hints, PEP 8; TypeScript strict mode; clean, documented code.
2. **Testing**: Write pytest for backend; Jest for frontend.
3. **Documentation**: Docstrings for all functions; inline comments for non-obvious logic.
4. **Security**: Never hardcode secrets; use environment variables; validate inputs; use bcrypt for passwords.
5. **Privacy**: Data minimization by design; user consent for data collection; PII encryption.
6. **Performance**: Optimize SQL queries; use Redis/KeyDB for caching; async where appropriate.

## Next Development Priorities
1. ✅ Backend database models complete
2. ✅ Authentication routes complete
3. ✅ Recommendation engine pipeline (Flink job) started
4. ✅ Moderation service started
5. 🔜 Complete feed generation endpoints (recommendations + social graph)
6. 🔜 Frontend Valdi screens (Camera, Feed, Stories, Profile)
7. 🔜 Deploy to Kubernetes (minikube/kind for testing)
8. 🔜 HITL moderation dashboard (React)
9. 🔜 End-to-end integration tests

## Common Patterns to Follow
- Use `async/await` for FastAPI routes with DB calls
- Use `httpx` for external service calls
- Use `alembic` for database migrations
- Use `pytest-asyncio` for async tests

## Key Files to Focus On
- `backend/app/routers/feed.py` - Feed/recommendation endpoints (in progress)
- `frontend/valdi/src/screens/FeedScreen.tsx` - Feed UI
- `recommendation/model/inference.py` - Model serving service
- `moderation/moderation_queue.py` - HITL queue management

## Environment Variables
Refer to `.env.example` for required config.

## Deployment Target
Kubernetes cluster with:
- PostgreSQL (StatefulSet)
- KeyDB (Redis-compatible, StatefulSet)
- FastAPI backend (Deployment)
- Flink job (Job)
- PyTorch inference service (Deployment)
- Moderation service (Deployment)
- React dashboard (Deployment)
- MinIO (StatefulSet)

## Testing Standards
- Minimum 80% code coverage
- Mock external APIs
- Load test with locust
