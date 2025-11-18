# Deployment Guide

This guide covers deploying Hygieia in various environments.

## Docker Deployment (Recommended)

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space

### Quick Deploy

1. **Clone and configure**
   ```bash
   git clone <repository-url>
   cd hygieia
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Build and start**
   ```bash
   docker-compose up -d
   ```

3. **Verify deployment**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

4. **Access services**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Production Configuration

#### Environment Variables

Key production settings in `.env`:

```bash
# Application
APP_ENV=production
DEBUG=false
SECRET_KEY=<generate-strong-key>

# Database
DATABASE_URL=postgresql://user:pass@db:5432/hygieia

# Security
JWT_SECRET_KEY=<generate-strong-key>
ENCRYPTION_KEY=<generate-base64-key>

# API Credentials
GARMIN_CLIENT_ID=<your-id>
GARMIN_CLIENT_SECRET=<your-secret>
# ... other API credentials
```

#### Generate Secrets

```bash
# Secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Encryption key (32 bytes, base64)
python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
```

### Docker Compose Profiles

#### Development
```bash
docker-compose up
```

#### Production (with Nginx)
```bash
docker-compose --profile production up -d
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3+ (optional)

### Configuration

1. **Create namespace**
   ```bash
   kubectl create namespace hygieia
   ```

2. **Create secrets**
   ```bash
   kubectl create secret generic hygieia-secrets \
     --from-literal=SECRET_KEY=<key> \
     --from-literal=DATABASE_URL=<url> \
     -n hygieia
   ```

3. **Apply manifests**
   ```bash
   kubectl apply -f k8s/ -n hygieia
   ```

### Scaling

**Scale API pods**
```bash
kubectl scale deployment hygieia-backend --replicas=3 -n hygieia
```

**Scale workers**
```bash
kubectl scale deployment hygieia-celery-worker --replicas=5 -n hygieia
```

## Cloud Deployment

### AWS Deployment

#### Using ECS

1. **Build and push Docker images**
   ```bash
   docker build -t hygieia-backend ./backend
   docker build -t hygieia-frontend ./frontend

   docker tag hygieia-backend:latest <ecr-url>/hygieia-backend:latest
   docker tag hygieia-frontend:latest <ecr-url>/hygieia-frontend:latest

   docker push <ecr-url>/hygieia-backend:latest
   docker push <ecr-url>/hygieia-frontend:latest
   ```

2. **Create RDS instance**
   - PostgreSQL 15+ with TimescaleDB
   - Multi-AZ for production
   - Automated backups

3. **Create ElastiCache (Redis)**
   - Redis 7+
   - Multi-AZ if needed

4. **Deploy to ECS**
   - Use Fargate for serverless
   - Or EC2 for more control
   - Configure task definitions
   - Set up load balancer

#### Using EKS

1. **Create EKS cluster**
   ```bash
   eksctl create cluster --name hygieia-cluster --region us-east-1
   ```

2. **Deploy using kubectl**
   ```bash
   kubectl apply -f k8s/ -n hygieia
   ```

### Google Cloud Platform

#### Using Cloud Run

1. **Build and push**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/hygieia-backend ./backend
   gcloud builds submit --tag gcr.io/PROJECT_ID/hygieia-frontend ./frontend
   ```

2. **Deploy services**
   ```bash
   gcloud run deploy hygieia-backend \
     --image gcr.io/PROJECT_ID/hygieia-backend \
     --platform managed \
     --region us-central1

   gcloud run deploy hygieia-frontend \
     --image gcr.io/PROJECT_ID/hygieia-frontend \
     --platform managed \
     --region us-central1
   ```

3. **Set up Cloud SQL**
   - PostgreSQL instance with TimescaleDB
   - Cloud SQL Proxy for connections

### Azure Deployment

#### Using Azure Container Instances

1. **Create resource group**
   ```bash
   az group create --name hygieia-rg --location eastus
   ```

2. **Create container registry**
   ```bash
   az acr create --resource-group hygieia-rg --name hygieiaacr --sku Basic
   ```

3. **Build and push**
   ```bash
   az acr build --registry hygieiaacr --image hygieia-backend ./backend
   az acr build --registry hygieiaacr --image hygieia-frontend ./frontend
   ```

4. **Deploy**
   ```bash
   az container create \
     --resource-group hygieia-rg \
     --name hygieia-backend \
     --image hygieiaacr.azurecr.io/hygieia-backend \
     --dns-name-label hygieia-api \
     --ports 8000
   ```

## Database Setup

### TimescaleDB Configuration

1. **Enable extension**
   ```sql
   CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
   ```

2. **Create hypertable**
   ```sql
   SELECT create_hypertable('metrics', 'timestamp');
   ```

3. **Set retention policy**
   ```sql
   SELECT add_retention_policy('metrics', INTERVAL '1 year');
   ```

4. **Create continuous aggregates**
   ```sql
   CREATE MATERIALIZED VIEW metrics_hourly
   WITH (timescaledb.continuous) AS
   SELECT
     time_bucket('1 hour', timestamp) AS hour,
     metric_type,
     AVG(value) as avg_value
   FROM metrics
   GROUP BY hour, metric_type;
   ```

### Database Migrations

```bash
# Upgrade to latest
cd backend
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Create new migration
alembic revision --autogenerate -m "description"
```

## Monitoring & Logging

### Application Monitoring

**Prometheus + Grafana**

1. Add metrics endpoint:
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator

   Instrumentator().instrument(app).expose(app)
   ```

2. Configure Prometheus:
   ```yaml
   scrape_configs:
     - job_name: 'hygieia'
       static_configs:
         - targets: ['backend:8000']
   ```

### Log Aggregation

**ELK Stack**

1. Configure logging:
   ```python
   import logging
   from pythonjsonlogger import jsonlogger

   handler = logging.StreamHandler()
   handler.setFormatter(jsonlogger.JsonFormatter())
   ```

2. Ship logs to Elasticsearch

**Cloud Logging**

- AWS CloudWatch
- Google Cloud Logging
- Azure Monitor

### Error Tracking

**Sentry**

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="<your-sentry-dsn>",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

## Backup & Recovery

### Database Backups

**Automated backups**
```bash
# Backup
pg_dump -h localhost -U hygieia hygieia > backup.sql

# Restore
psql -h localhost -U hygieia hygieia < backup.sql
```

**Continuous archiving (WAL)**
```bash
# Configure in postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /path/to/archive/%f'
```

### Application State

- Configuration in version control
- Secrets in vault/secret manager
- User data in database (backed up)

## Security Best Practices

1. **Use HTTPS in production**
   - SSL/TLS certificates (Let's Encrypt)
   - Redirect HTTP to HTTPS

2. **Secure secrets**
   - Use environment variables
   - Never commit secrets
   - Use secret managers (AWS Secrets Manager, etc.)

3. **Database security**
   - Strong passwords
   - Network isolation
   - Encrypted connections

4. **API security**
   - Rate limiting
   - CORS configuration
   - Input validation

5. **Regular updates**
   - Keep dependencies updated
   - Security patches
   - Vulnerability scanning

## Performance Optimization

### Database Optimization

1. **Indexes**
   - Add indexes for common queries
   - Monitor slow queries

2. **Connection pooling**
   - Configure pool size
   - Use connection pooling

3. **Query optimization**
   - Use EXPLAIN ANALYZE
   - Optimize slow queries
   - Use materialized views

### Application Optimization

1. **Caching**
   - Redis for frequent queries
   - HTTP caching headers
   - CDN for static assets

2. **Async operations**
   - Background tasks for slow operations
   - Async database queries

3. **Resource limits**
   - Container resource limits
   - Worker concurrency settings

## Troubleshooting

### Common Issues

**Database connection errors**
```bash
# Check connection
docker-compose exec backend python -c "from api.database import engine; print(engine.connect())"
```

**Celery workers not processing**
```bash
# Check worker status
docker-compose exec celery-worker celery -A ingestion.tasks inspect active
```

**Memory issues**
```bash
# Check container resources
docker stats
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database
docker-compose exec timescaledb pg_isready

# Redis
docker-compose exec redis redis-cli ping
```

## Scaling Guidelines

### Vertical Scaling

- Increase container resources
- Upgrade database instance
- Increase Redis memory

### Horizontal Scaling

- Multiple API instances (stateless)
- Multiple Celery workers
- Database read replicas
- Redis cluster

### Load Balancing

- Nginx for API load balancing
- Cloud load balancers (ALB, GCP LB)
- Health checks for routing

## Maintenance

### Routine Tasks

1. **Database maintenance**
   ```bash
   # Vacuum
   docker-compose exec timescaledb psql -U hygieia -c "VACUUM ANALYZE;"
   ```

2. **Log rotation**
   - Configure log rotation
   - Clean old logs

3. **Dependency updates**
   ```bash
   # Backend
   pip list --outdated

   # Frontend
   npm outdated
   ```

4. **Monitor metrics**
   - Response times
   - Error rates
   - Resource usage

## Support

For deployment issues:
- Check logs: `docker-compose logs`
- Review documentation
- Open GitHub issue
