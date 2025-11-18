"""
Metric models for time-series health data
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from api.database import Base
import enum


class MetricType(str, enum.Enum):
    """Types of health metrics"""
    # Cardiovascular
    HEART_RATE = "heart_rate"
    HEART_RATE_VARIABILITY = "hrv"
    RESTING_HEART_RATE = "resting_hr"
    VO2_MAX = "vo2_max"
    BLOOD_PRESSURE_SYSTOLIC = "bp_systolic"
    BLOOD_PRESSURE_DIASTOLIC = "bp_diastolic"

    # Sleep
    SLEEP_DURATION = "sleep_duration"
    SLEEP_DEEP = "sleep_deep"
    SLEEP_REM = "sleep_rem"
    SLEEP_LIGHT = "sleep_light"
    SLEEP_AWAKE = "sleep_awake"
    SLEEP_SCORE = "sleep_score"
    SLEEP_TEMPERATURE = "sleep_temperature"

    # Activity
    STEPS = "steps"
    DISTANCE = "distance"
    CALORIES = "calories"
    ACTIVE_MINUTES = "active_minutes"
    FLOORS_CLIMBED = "floors_climbed"

    # Body Composition
    WEIGHT = "weight"
    BODY_FAT_PERCENTAGE = "body_fat_pct"
    MUSCLE_MASS = "muscle_mass"
    BMI = "bmi"
    METABOLIC_AGE = "metabolic_age"

    # Stress & Recovery
    STRESS_LEVEL = "stress_level"
    BODY_BATTERY = "body_battery"
    READINESS_SCORE = "readiness_score"
    RECOVERY_TIME = "recovery_time"

    # Training
    TRAINING_LOAD = "training_load"
    INTENSITY_MINUTES = "intensity_minutes"

    # Environmental
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    AIR_QUALITY_INDEX = "aqi"
    UV_INDEX = "uv_index"
    BAROMETRIC_PRESSURE = "barometric_pressure"


class Metric(Base):
    """Time-series metric data"""
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Metric identification
    metric_type = Column(SQLEnum(MetricType), nullable=False, index=True)
    source = Column(String, nullable=False, index=True)  # garmin, oura, wyze, etc.

    # Value and units
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # bpm, kg, %, etc.

    # Timestamp
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    # Metadata
    metadata = Column(JSONB, nullable=True)  # Additional context
    quality_score = Column(Float, nullable=True)  # Data quality indicator
    is_manual = Column(Integer, default=0)  # 0=automatic, 1=manual entry

    # Sync tracking
    synced_at = Column(DateTime(timezone=True), nullable=True)

    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_user_metric_time', 'user_id', 'metric_type', 'timestamp'),
        Index('idx_user_time', 'user_id', 'timestamp'),
        Index('idx_metric_source_time', 'metric_type', 'source', 'timestamp'),
    )

    def __repr__(self):
        return f"<Metric(type={self.metric_type}, value={self.value}, timestamp={self.timestamp})>"
