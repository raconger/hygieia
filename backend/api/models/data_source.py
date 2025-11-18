"""
Data source models for external API integrations
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from api.database import Base


class DataSource(Base):
    """Available data sources"""
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # garmin, oura, strava, etc.
    display_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    requires_oauth = Column(Boolean, default=True)

    # API configuration
    api_endpoint = Column(String, nullable=True)
    api_version = Column(String, nullable=True)
    rate_limit = Column(Integer, nullable=True)  # requests per hour

    # Supported metrics
    supported_metrics = Column(JSONB, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<DataSource(name={self.name})>"


class DataSourceAuth(Base):
    """User authentication tokens for data sources"""
    __tablename__ = "data_source_auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)

    # OAuth tokens (encrypted)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)

    # Additional credentials
    credentials = Column(JSONB, nullable=True)  # Encrypted JSON

    # Status
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    last_sync_status = Column(String, nullable=True)  # success, failed, partial

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="data_sources")

    def __repr__(self):
        return f"<DataSourceAuth(user_id={self.user_id}, data_source_id={self.data_source_id})>"
