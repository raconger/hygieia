"""
Application configuration using Pydantic settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Hygieia"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-to-a-random-secret-key"
    API_VERSION: str = "v1"

    # API Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    DATABASE_URL: str = "postgresql://hygieia:hygieia@localhost:5432/hygieia"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Garmin Connect API
    GARMIN_CLIENT_ID: str = ""
    GARMIN_CLIENT_SECRET: str = ""
    GARMIN_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/garmin/callback"

    # Oura Ring API
    OURA_CLIENT_ID: str = ""
    OURA_CLIENT_SECRET: str = ""
    OURA_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oura/callback"

    # Strava API
    STRAVA_CLIENT_ID: str = ""
    STRAVA_CLIENT_SECRET: str = ""
    STRAVA_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/strava/callback"

    # Weather API
    OPENWEATHER_API_KEY: str = ""

    # Air Quality API
    AIRNOW_API_KEY: str = ""

    # Default location
    DEFAULT_LATITUDE: float = 37.7749
    DEFAULT_LONGITUDE: float = -122.4194

    # Sync Configuration
    SYNC_INTERVAL_MINUTES: int = 60
    HISTORICAL_BACKFILL_DAYS: int = 90

    # Alert Configuration
    ENABLE_ALERTS: bool = True
    ALERT_EMAIL_FROM: str = "alerts@hygieia.app"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Security
    JWT_SECRET_KEY: str = "change-this-to-a-random-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str = "change-this-to-a-32-byte-base64-key"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Data Retention
    RAW_DATA_RETENTION_DAYS: int = 365
    AGGREGATED_DATA_RETENTION_DAYS: int = 1825
    ALERT_HISTORY_RETENTION_DAYS: int = 90

    # Feature Flags
    ENABLE_CORRELATION_ANALYSIS: bool = True
    ENABLE_ANOMALY_DETECTION: bool = False
    ENABLE_ML_FEATURES: bool = False
    ENABLE_EXPORT: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
