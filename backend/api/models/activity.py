"""
Activity models for workouts and exercises
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from api.database import Base


class Activity(Base):
    """Activity/workout sessions"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Activity identification
    external_id = Column(String, nullable=True, index=True)  # ID from source platform
    source = Column(String, nullable=False)  # garmin, strava, etc.

    # Activity details
    activity_type = Column(String, nullable=False)  # running, cycling, swimming, etc.
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)

    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Distance & movement
    distance_meters = Column(Float, nullable=True)
    elevation_gain_meters = Column(Float, nullable=True)
    elevation_loss_meters = Column(Float, nullable=True)

    # Performance
    avg_pace = Column(Float, nullable=True)  # minutes per km
    avg_speed = Column(Float, nullable=True)  # km/h
    max_speed = Column(Float, nullable=True)
    avg_power = Column(Float, nullable=True)  # watts
    max_power = Column(Float, nullable=True)

    # Heart rate
    avg_heart_rate = Column(Float, nullable=True)
    max_heart_rate = Column(Float, nullable=True)

    # Calories & training
    calories = Column(Integer, nullable=True)
    training_load = Column(Float, nullable=True)
    perceived_effort = Column(Integer, nullable=True)  # 1-10 scale

    # Location
    location_name = Column(String, nullable=True)
    start_latitude = Column(Float, nullable=True)
    start_longitude = Column(Float, nullable=True)

    # Additional data
    metadata = Column(JSONB, nullable=True)  # GPS track, lap data, etc.

    # Sync tracking
    synced_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="activities")

    # Indexes
    __table_args__ = (
        Index('idx_user_activity_time', 'user_id', 'start_time'),
        Index('idx_activity_type_time', 'activity_type', 'start_time'),
    )

    def __repr__(self):
        return f"<Activity(type={self.activity_type}, start_time={self.start_time})>"
