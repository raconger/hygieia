# Getting Started with Hygieia

This guide will help you set up and run Hygieia on your local machine.

## Prerequisites

- Docker and Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+ with TimescaleDB extension
  - Redis 7+

## Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hygieia
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **Login**
   - Use any email and password (demo mode)
   - Or set up proper authentication in the backend

## Manual Setup (Local Development)

### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   # Make sure PostgreSQL is running
   # Create database: createdb hygieia
   # Run migrations
   alembic upgrade head
   ```

4. **Start backend server**
   ```bash
   uvicorn api.main:app --reload
   ```

5. **Start Celery worker (in another terminal)**
   ```bash
   celery -A ingestion.tasks worker --loglevel=info
   ```

6. **Start Celery beat (in another terminal)**
   ```bash
   celery -A ingestion.tasks beat --loglevel=info
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

3. **Access the application**
   - Open http://localhost:3000

## Connecting Data Sources

### Garmin Connect

1. Go to Settings → Data Sources
2. Click "Connect" next to Garmin Connect
3. Follow OAuth flow to authorize access
4. Data will sync automatically every hour

### Oura Ring

1. Go to Settings → Data Sources
2. Click "Connect" next to Oura Ring
3. Authorize access to your Oura account
4. Data will sync automatically

### Strava

1. Go to Settings → Data Sources
2. Click "Connect" next to Strava
3. Authorize Strava access
4. Activities will sync automatically

### Weather Data

Weather and air quality data is collected automatically based on your location settings.

1. Go to Settings → Preferences
2. Set your default location (latitude/longitude)
3. Or location will be detected from your activities

## Next Steps

1. **Explore the Dashboard** - View your health metrics overview
2. **Check Trends** - Analyze long-term patterns
3. **Set Up Alerts** - Create custom alert rules
4. **Explore Analytics** - Discover correlations in your data

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify TimescaleDB extension is installed

### API authentication errors
- Check API credentials in `.env`
- Verify OAuth callback URLs are correct
- Ensure tokens haven't expired

### Data not syncing
- Check Celery worker is running
- View Celery logs for errors
- Verify API credentials are valid

### Frontend not loading
- Clear browser cache
- Check console for errors
- Verify backend API is running

## Getting Help

- Check the [FAQ](FAQ.md)
- Review the [API Documentation](http://localhost:8000/docs)
- Report issues on GitHub
