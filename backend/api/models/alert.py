"""
Alert models for notifications and monitoring
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from api.database import Base
import enum


class AlertPriority(str, enum.Enum):
    """Alert priority levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, enum.Enum):
    """Types of alerts"""
    THRESHOLD = "threshold"
    ANOMALY = "anomaly"
    TREND = "trend"
    CORRELATION = "correlation"
    MISSING_DATA = "missing_data"
    ENVIRONMENTAL = "environmental"


class AlertDeliveryMethod(str, enum.Enum):
    """Alert delivery methods"""
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class AlertRule(Base):
    """User-defined alert rules"""
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Rule details
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    alert_type = Column(SQLEnum(AlertType), nullable=False)
    priority = Column(SQLEnum(AlertPriority), default=AlertPriority.INFO)

    # Conditions (stored as JSON)
    conditions = Column(JSONB, nullable=False)
    # Example: {"metric": "heart_rate", "operator": ">", "threshold": 100, "duration_minutes": 5}

    # Delivery settings
    delivery_methods = Column(JSONB, nullable=False)  # List of delivery methods
    quiet_hours_start = Column(Integer, nullable=True)  # Hour (0-23)
    quiet_hours_end = Column(Integer, nullable=True)    # Hour (0-23)
    weekdays_only = Column(Boolean, default=False)

    # Status
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime(timezone=True), nullable=True)
    trigger_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="alert_rules")
    history = relationship("AlertHistory", back_populates="alert_rule")

    def __repr__(self):
        return f"<AlertRule(name={self.name}, type={self.alert_type})>"


class AlertHistory(Base):
    """History of triggered alerts"""
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)
    alert_rule_id = Column(Integer, ForeignKey("alert_rules.id"), nullable=False)

    # Alert details
    priority = Column(SQLEnum(AlertPriority), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)

    # Triggering data
    metric_values = Column(JSONB, nullable=True)  # Snapshot of metric values

    # Delivery
    delivery_status = Column(JSONB, nullable=True)  # Status per delivery method
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # User interaction
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    snoozed_until = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    alert_rule = relationship("AlertRule", back_populates="history")

    def __repr__(self):
        return f"<AlertHistory(title={self.title}, priority={self.priority})>"


class Alert(Base):
    """Active alerts (view)"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alert_rule_id = Column(Integer, ForeignKey("alert_rules.id"), nullable=True)

    # Alert details
    priority = Column(SQLEnum(AlertPriority), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)

    # Status
    is_active = Column(Boolean, default=True)
    acknowledged = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Alert(title={self.title}, priority={self.priority})>"
