# Architecture Overview

This document provides a comprehensive overview of Hygieia's architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│  Dashboard | Visualizations | Alerts | Data Explorer       │
└─────────────────────┬───────────────────────────────────────┘
                      │
              ┌───────▼────────┐
              │   API Gateway   │
              │  (FastAPI)      │
              └───────┬────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
    ┌────▼────┐  ┌───▼────┐  ┌───▼────┐
    │  Data   │  │Analytics│  │ Alert  │
    │Ingestion│  │ Engine  │  │ Engine │
    └────┬────┘  └───┬────┘  └───┬────┘
         │           │            │
    ┌────▼───────────▼────────────▼─────┐
    │  TimescaleDB (time-series data)   │
    │  PostgreSQL (metadata, configs)   │
    │  Redis (cache, queue)             │
    └───────────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │  External APIs                    │
    │  Garmin | Oura | Wyze | Strava   │
    │  Weather | AQI                    │
    └───────────────────────────────────┘
```

## Components

### Frontend Layer

**Technology**: React 18 + TypeScript + Material-UI

**Responsibilities**:
- User interface and visualization
- State management (Zustand)
- API client (React Query)
- Authentication flow
- Real-time updates

**Key Features**:
- Responsive design (mobile, tablet, desktop)
- Dark mode support
- Interactive charts (Recharts)
- Progressive Web App capabilities

### API Gateway

**Technology**: FastAPI (Python 3.11+)

**Responsibilities**:
- RESTful API endpoints
- Request validation (Pydantic)
- Authentication & authorization (JWT)
- Rate limiting
- API documentation (OpenAPI/Swagger)

**Middleware**:
- CORS handling
- Request logging
- Error handling
- Rate limiting

### Data Ingestion Layer

**Technology**: Celery + Redis

**Responsibilities**:
- Scheduled data synchronization
- API client implementations
- Data normalization
- Quality checks
- Error handling and retry logic

**Data Sources**:
1. **Garmin Connect**
   - Heart rate, HRV, sleep, activities
   - OAuth 2.0 authentication
   - Hourly sync

2. **Oura Ring**
   - Sleep stages, readiness, temperature
   - OAuth 2.0 authentication
   - Daily sync

3. **Strava**
   - Activities, performance metrics
   - OAuth 2.0 authentication
   - Real-time webhooks

4. **Wyze Scale**
   - Body composition metrics
   - Email/password authentication
   - On-demand sync

5. **Weather & AQI**
   - OpenWeatherMap API
   - AirNow API
   - 15-minute sync

### Analytics Engine

**Technology**: Python (pandas, scipy, scikit-learn)

**Capabilities**:
- Statistical analysis
- Correlation detection
- Trend analysis
- Anomaly detection
- Pattern recognition
- Predictive modeling (future)

**Algorithms**:
- Pearson/Spearman correlation
- Moving averages
- Standard deviation
- Z-score anomaly detection
- Time series decomposition

### Alert Engine

**Technology**: Python + Redis

**Responsibilities**:
- Rule evaluation
- Condition checking
- Notification dispatch
- Alert history
- Snooze management

**Alert Types**:
- Threshold (value exceeds limit)
- Anomaly (statistical outlier)
- Trend (sustained increase/decrease)
- Correlation (condition combinations)
- Missing data
- Environmental (weather/AQI)

### Data Storage Layer

#### TimescaleDB (Time-Series Data)

**Schema**:
- Metrics table (hypertable)
- Automated data retention policies
- Continuous aggregates for common queries
- Efficient compression

**Optimizations**:
- Partitioning by time
- Indexes on user_id, metric_type, timestamp
- Materialized views for dashboards

#### PostgreSQL (Relational Data)

**Tables**:
- Users
- Data source connections
- Alert rules
- Alert history
- Activities
- Settings

#### Redis (Cache & Queue)

**Usage**:
- Celery message broker
- Result backend
- API response cache
- Rate limiting
- Session storage

## Data Flow

### Ingestion Flow

```
External API → Celery Task → Data Normalization →
Quality Check → Database Insert → Cache Update →
Alert Check → Notification (if triggered)
```

### Query Flow

```
User Request → API Endpoint → Cache Check →
Database Query → Transform/Aggregate →
Cache Store → JSON Response
```

### Alert Flow

```
Celery Beat Schedule → Fetch Alert Rules →
Evaluate Conditions → Trigger Alert →
Store History → Send Notifications → Update Status
```

## Security

### Authentication

- JWT tokens for API authentication
- OAuth 2.0 for external services
- Secure credential storage (encryption)
- Token refresh mechanism

### Data Protection

- Encrypted database connections
- API credential encryption
- HTTPS only in production
- HIPAA-compliant practices

### Access Control

- User-based data isolation
- API rate limiting
- CORS restrictions
- Input validation

## Scalability

### Horizontal Scaling

- **API**: Multiple FastAPI instances behind load balancer
- **Workers**: Multiple Celery workers for parallel processing
- **Database**: Read replicas for query distribution

### Vertical Scaling

- **Database**: Increase resources for TimescaleDB
- **Redis**: Increase memory for larger cache
- **Workers**: More CPU/memory for data processing

### Optimization Strategies

- Database query optimization
- Caching frequently accessed data
- Background job prioritization
- Data compression and archival
- CDN for static assets

## Monitoring & Observability

### Logging

- Structured logging (JSON format)
- Log aggregation (ELK stack compatible)
- Error tracking and alerting

### Metrics

- API response times
- Database query performance
- Celery task metrics
- Cache hit rates
- Error rates

### Health Checks

- `/health` endpoint for each service
- Database connectivity
- External API status
- Worker queue depth

## Deployment

### Development

```bash
docker-compose up
```

### Production

- Docker containers
- Kubernetes orchestration
- Environment-based configuration
- Automated backups
- Blue-green deployment

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 + TypeScript | User interface |
| API | FastAPI (Python) | REST API |
| Database | TimescaleDB + PostgreSQL | Data storage |
| Cache/Queue | Redis | Caching & job queue |
| Worker | Celery | Background tasks |
| Charts | Recharts | Data visualization |
| State | Zustand | Client state management |
| Query | React Query | Server state & caching |
| Containerization | Docker | Deployment |

## Future Enhancements

1. **GraphQL API** for flexible data querying
2. **WebSocket** support for real-time updates
3. **Machine Learning** for predictive insights
4. **Mobile Apps** (React Native)
5. **Multi-tenancy** for coaches/teams
6. **Advanced Analytics** with ML models
7. **Data Export** to standard formats (Apple Health, FHIR)
