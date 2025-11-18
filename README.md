# Hygieia - Personal Health Data Aggregation Platform

A comprehensive health tracking application that aggregates data from multiple wearable devices, fitness platforms, and environmental sensors to provide holistic health insights.

## 🎯 Overview

Hygieia solves the health data fragmentation problem by consolidating data from:
- **Wearables**: Garmin, Oura Ring, Apple Health
- **Fitness Platforms**: Strava
- **Smart Devices**: Wyze Scale
- **Environmental Data**: Weather, Air Quality Index

## ✨ Features

### Phase 1 (MVP) - Current
- ✅ Garmin Connect integration
- ✅ Time-series data storage (TimescaleDB)
- ✅ Basic visualizations (line charts, trends)
- ✅ Threshold-based alerts
- ✅ RESTful API

### Phase 2 - Planned
- 🔄 Multi-device integration (Oura, Wyze, Strava, Apple Health)
- 🔄 Weather and AQI data collection
- 🔄 Advanced visualizations (heatmaps, distributions)
- 🔄 Correlation analysis

### Phase 3 - Future
- 📋 Anomaly detection with ML
- 📋 Predictive analytics
- 📋 Mobile applications

## 🏗️ Architecture

```
Frontend (React + TypeScript)
    ↓
API Gateway (FastAPI)
    ↓
┌─────────────┬──────────────┬─────────────┐
│  Ingestion  │  Analytics   │   Alerts    │
└─────────────┴──────────────┴─────────────┘
    ↓
TimescaleDB + PostgreSQL + Redis
    ↓
External APIs (Garmin, Oura, Weather, etc.)
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hygieia
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

3. Start the services:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
hygieia/
├── backend/
│   ├── api/              # FastAPI application
│   ├── ingestion/        # Data collection services
│   ├── analytics/        # Analysis and correlation engine
│   ├── alerts/           # Alert system
│   └── models/           # Database models
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   └── utils/        # Utilities
│   └── public/
├── database/
│   └── migrations/       # Database migrations
├── docker/               # Docker configurations
└── docs/                 # Documentation
```

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

## 📊 Key Metrics Tracked

- **Cardiovascular**: Heart rate, HRV, resting HR, VO2 max
- **Sleep**: Sleep stages, duration, quality, temperature
- **Activity**: Steps, distance, calories, training load
- **Recovery**: Body Battery, readiness score, stress
- **Body Composition**: Weight, body fat %, muscle mass
- **Environmental**: Temperature, humidity, AQI, UV index

## 🔐 Security & Privacy

- OAuth 2.0 for external API authentication
- Encrypted credential storage
- HIPAA-compliant data handling
- User-controlled data retention and deletion

## 📖 API Documentation

Full API documentation is available at `/docs` when running the backend service.

Key endpoints:
- `GET /api/v1/metrics` - Query health metrics
- `POST /api/v1/sync` - Trigger data synchronization
- `GET /api/v1/trends` - Get trend analysis
- `POST /api/v1/alerts` - Configure alerts

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 Configuration

### Data Sources

Configure your data sources in `.env`:

```env
# Garmin
GARMIN_CLIENT_ID=your_client_id
GARMIN_CLIENT_SECRET=your_client_secret

# Oura
OURA_ACCESS_TOKEN=your_token

# Weather
OPENWEATHER_API_KEY=your_api_key
```

### Alert Configuration

Alerts can be configured via the UI or API:
- Threshold alerts (e.g., HR > 65 bpm)
- Trend alerts (e.g., HRV declining for 7 days)
- Environmental alerts (e.g., poor AQI)

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with data from:
- Garmin Connect API
- Oura Ring API
- Strava API
- OpenWeatherMap API
- And more...

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Version**: 1.0.0
**Last Updated**: November 18, 2025
