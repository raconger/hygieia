"""
Metrics service for database operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd

from api.models.metric import Metric, MetricType
from api.models.user import User


class MetricsService:
    """Service for metric operations"""

    @staticmethod
    async def get_metrics(
        db: AsyncSession,
        user: User,
        metric_type: Optional[str] = None,
        source: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[Metric]:
        """Query metrics with filters"""
        query = select(Metric).where(Metric.user_id == user.id)

        if metric_type:
            query = query.where(Metric.metric_type == metric_type)

        if source:
            query = query.where(Metric.source == source)

        if start_date:
            query = query.where(Metric.timestamp >= start_date)

        if end_date:
            query = query.where(Metric.timestamp <= end_date)

        query = query.order_by(Metric.timestamp.desc()).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_metric_summary(
        db: AsyncSession,
        user: User,
        metric_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """Calculate statistical summary for a metric"""
        query = select(Metric).where(
            and_(
                Metric.user_id == user.id,
                Metric.metric_type == metric_type
            )
        )

        if start_date:
            query = query.where(Metric.timestamp >= start_date)

        if end_date:
            query = query.where(Metric.timestamp <= end_date)

        result = await db.execute(query)
        metrics = result.scalars().all()

        if not metrics:
            return {
                "metric_type": metric_type,
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "min": 0.0,
                "max": 0.0,
                "std": 0.0,
                "unit": ""
            }

        values = [m.value for m in metrics]
        df = pd.Series(values)

        return {
            "metric_type": metric_type,
            "count": len(values),
            "mean": float(df.mean()),
            "median": float(df.median()),
            "min": float(df.min()),
            "max": float(df.max()),
            "std": float(df.std()),
            "unit": metrics[0].unit if metrics else ""
        }

    @staticmethod
    async def get_latest_metrics(
        db: AsyncSession,
        user: User
    ) -> dict:
        """Get latest value for each metric type"""
        # Query for latest metric of each type
        from sqlalchemy.sql import distinct

        result = {}

        # Get all metric types for user
        metric_types_query = select(distinct(Metric.metric_type)).where(
            Metric.user_id == user.id
        )
        metric_types_result = await db.execute(metric_types_query)
        metric_types = metric_types_result.scalars().all()

        for metric_type in metric_types:
            query = select(Metric).where(
                and_(
                    Metric.user_id == user.id,
                    Metric.metric_type == metric_type
                )
            ).order_by(Metric.timestamp.desc()).limit(1)

            latest_result = await db.execute(query)
            latest_metric = latest_result.scalar_one_or_none()

            if latest_metric:
                result[metric_type] = {
                    "value": latest_metric.value,
                    "unit": latest_metric.unit,
                    "timestamp": latest_metric.timestamp.isoformat(),
                    "source": latest_metric.source
                }

        return result

    @staticmethod
    async def create_metric(
        db: AsyncSession,
        user: User,
        metric_type: str,
        value: float,
        unit: str,
        source: str = "manual",
        timestamp: Optional[datetime] = None,
        metadata: Optional[dict] = None
    ) -> Metric:
        """Create a new metric"""
        metric = Metric(
            user_id=user.id,
            metric_type=metric_type,
            value=value,
            unit=unit,
            source=source,
            timestamp=timestamp or datetime.utcnow(),
            metadata=metadata,
            is_manual=1 if source == "manual" else 0,
            synced_at=datetime.utcnow()
        )

        db.add(metric)
        await db.commit()
        await db.refresh(metric)

        return metric

    @staticmethod
    async def bulk_create_metrics(
        db: AsyncSession,
        user: User,
        metrics_data: List[dict]
    ) -> int:
        """Bulk create metrics"""
        metrics = [
            Metric(
                user_id=user.id,
                **metric_data
            )
            for metric_data in metrics_data
        ]

        db.add_all(metrics)
        await db.commit()

        return len(metrics)
