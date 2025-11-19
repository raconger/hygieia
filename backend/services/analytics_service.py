"""
Analytics service for correlations and insights
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Tuple, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats

from api.models.metric import Metric
from api.models.user import User


class AnalyticsService:
    """Service for analytics operations"""

    @staticmethod
    async def calculate_correlation(
        db: AsyncSession,
        user: User,
        metric_x: str,
        metric_y: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        method: str = "pearson"
    ) -> dict:
        """Calculate correlation between two metrics"""
        # Fetch metrics for X
        query_x = select(Metric).where(
            and_(
                Metric.user_id == user.id,
                Metric.metric_type == metric_x
            )
        )
        if start_date:
            query_x = query_x.where(Metric.timestamp >= start_date)
        if end_date:
            query_x = query_x.where(Metric.timestamp <= end_date)

        result_x = await db.execute(query_x.order_by(Metric.timestamp))
        metrics_x = result_x.scalars().all()

        # Fetch metrics for Y
        query_y = select(Metric).where(
            and_(
                Metric.user_id == user.id,
                Metric.metric_type == metric_y
            )
        )
        if start_date:
            query_y = query_y.where(Metric.timestamp >= start_date)
        if end_date:
            query_y = query_y.where(Metric.timestamp <= end_date)

        result_y = await db.execute(query_y.order_by(Metric.timestamp))
        metrics_y = result_y.scalars().all()

        if not metrics_x or not metrics_y:
            return {
                "metric_x": metric_x,
                "metric_y": metric_y,
                "correlation": 0.0,
                "p_value": 1.0,
                "sample_size": 0,
                "correlation_type": method
            }

        # Convert to dataframes and align timestamps
        df_x = pd.DataFrame([
            {"timestamp": m.timestamp, "value": m.value}
            for m in metrics_x
        ])
        df_y = pd.DataFrame([
            {"timestamp": m.timestamp, "value": m.value}
            for m in metrics_y
        ])

        # Merge on nearest timestamps
        df_x['timestamp'] = pd.to_datetime(df_x['timestamp'])
        df_y['timestamp'] = pd.to_datetime(df_y['timestamp'])

        # For simplicity, merge on date only
        df_x['date'] = df_x['timestamp'].dt.date
        df_y['date'] = df_y['timestamp'].dt.date

        # Average values by date
        df_x_daily = df_x.groupby('date')['value'].mean().reset_index()
        df_y_daily = df_y.groupby('date')['value'].mean().reset_index()

        # Merge
        df_merged = pd.merge(df_x_daily, df_y_daily, on='date', suffixes=('_x', '_y'))

        if len(df_merged) < 2:
            return {
                "metric_x": metric_x,
                "metric_y": metric_y,
                "correlation": 0.0,
                "p_value": 1.0,
                "sample_size": len(df_merged),
                "correlation_type": method
            }

        # Calculate correlation
        if method == "pearson":
            correlation, p_value = stats.pearsonr(df_merged['value_x'], df_merged['value_y'])
        else:  # spearman
            correlation, p_value = stats.spearmanr(df_merged['value_x'], df_merged['value_y'])

        return {
            "metric_x": metric_x,
            "metric_y": metric_y,
            "correlation": float(correlation),
            "p_value": float(p_value),
            "sample_size": len(df_merged),
            "correlation_type": method
        }

    @staticmethod
    async def find_correlations(
        db: AsyncSession,
        user: User,
        metric: Optional[str] = None,
        min_correlation: float = 0.3,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[dict]:
        """Find significant correlations"""
        from sqlalchemy.sql import distinct

        # Get all metric types
        metric_types_query = select(distinct(Metric.metric_type)).where(
            Metric.user_id == user.id
        )
        result = await db.execute(metric_types_query)
        all_metrics = list(result.scalars().all())

        correlations = []

        if metric:
            # Find correlations with specific metric
            for other_metric in all_metrics:
                if other_metric != metric:
                    corr_result = await AnalyticsService.calculate_correlation(
                        db, user, metric, other_metric, start_date, end_date
                    )
                    if abs(corr_result['correlation']) >= min_correlation:
                        correlations.append(corr_result)
        else:
            # Find all pairwise correlations
            for i, metric_x in enumerate(all_metrics):
                for metric_y in all_metrics[i+1:]:
                    corr_result = await AnalyticsService.calculate_correlation(
                        db, user, metric_x, metric_y, start_date, end_date
                    )
                    if abs(corr_result['correlation']) >= min_correlation:
                        correlations.append(corr_result)

        # Sort by absolute correlation
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)

        return correlations

    @staticmethod
    async def detect_anomalies(
        db: AsyncSession,
        user: User,
        metric_type: str,
        sensitivity: float = 2.0,
        lookback_days: int = 30
    ) -> dict:
        """Detect anomalies using z-score"""
        end_date = datetime.utcnow()
        start_date = end_date - pd.Timedelta(days=lookback_days)

        query = select(Metric).where(
            and_(
                Metric.user_id == user.id,
                Metric.metric_type == metric_type,
                Metric.timestamp >= start_date,
                Metric.timestamp <= end_date
            )
        ).order_by(Metric.timestamp)

        result = await db.execute(query)
        metrics = result.scalars().all()

        if not metrics:
            return {
                "metric_type": metric_type,
                "anomalies": [],
                "baseline_mean": 0.0,
                "baseline_std": 0.0
            }

        # Convert to pandas
        df = pd.DataFrame([
            {"timestamp": m.timestamp, "value": m.value}
            for m in metrics
        ])

        # Calculate statistics
        mean_val = df['value'].mean()
        std_val = df['value'].std()

        # Find anomalies (values beyond sensitivity * std from mean)
        df['z_score'] = (df['value'] - mean_val) / std_val
        anomalies = df[abs(df['z_score']) > sensitivity]

        return {
            "metric_type": metric_type,
            "anomalies": [
                {
                    "timestamp": row['timestamp'].isoformat(),
                    "value": float(row['value']),
                    "z_score": float(row['z_score'])
                }
                for _, row in anomalies.iterrows()
            ],
            "baseline_mean": float(mean_val),
            "baseline_std": float(std_val)
        }

    @staticmethod
    async def segment_analysis(
        db: AsyncSession,
        user: User,
        metric_type: str,
        segment_by: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[dict]:
        """Analyze metrics by segments (e.g., day of week)"""
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
            return []

        # Convert to dataframe
        df = pd.DataFrame([
            {"timestamp": m.timestamp, "value": m.value}
            for m in metrics
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Add segment column
        if segment_by == "day_of_week":
            df['segment'] = df['timestamp'].dt.day_name()
        elif segment_by == "hour_of_day":
            df['segment'] = df['timestamp'].dt.hour
        elif segment_by == "month":
            df['segment'] = df['timestamp'].dt.month_name()
        else:
            df['segment'] = "all"

        # Group by segment
        grouped = df.groupby('segment')['value']

        results = []
        for segment, values in grouped:
            results.append({
                "segment": str(segment),
                "count": int(len(values)),
                "mean": float(values.mean()),
                "median": float(values.median()),
                "std": float(values.std())
            })

        return results
