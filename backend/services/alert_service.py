"""
Alert service for rule evaluation
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd

from api.models.alert import AlertRule, Alert, AlertHistory, AlertPriority
from api.models.metric import Metric
from api.models.user import User


class AlertService:
    """Service for alert operations"""

    @staticmethod
    async def evaluate_alert_rules(
        db: AsyncSession
    ) -> dict:
        """Evaluate all active alert rules"""
        # Get all active alert rules
        query = select(AlertRule).where(AlertRule.is_active == True)
        result = await db.execute(query)
        alert_rules = result.scalars().all()

        alerts_triggered = 0

        for rule in alert_rules:
            # Check quiet hours
            if AlertService._is_in_quiet_hours(rule):
                continue

            # Evaluate rule
            should_trigger = await AlertService._evaluate_rule(db, rule)

            if should_trigger:
                await AlertService._trigger_alert(db, rule)
                alerts_triggered += 1

        return {
            "status": "success",
            "rules_evaluated": len(alert_rules),
            "alerts_triggered": alerts_triggered
        }

    @staticmethod
    def _is_in_quiet_hours(rule: AlertRule) -> bool:
        """Check if current time is in quiet hours"""
        if rule.quiet_hours_start is None or rule.quiet_hours_end is None:
            return False

        now = datetime.utcnow()
        current_hour = now.hour

        if rule.quiet_hours_start < rule.quiet_hours_end:
            return rule.quiet_hours_start <= current_hour < rule.quiet_hours_end
        else:  # Quiet hours cross midnight
            return current_hour >= rule.quiet_hours_start or current_hour < rule.quiet_hours_end

    @staticmethod
    async def _evaluate_rule(
        db: AsyncSession,
        rule: AlertRule
    ) -> bool:
        """Evaluate if alert rule conditions are met"""
        conditions = rule.conditions

        if rule.alert_type == "threshold":
            return await AlertService._evaluate_threshold(db, rule.user_id, conditions)
        elif rule.alert_type == "trend":
            return await AlertService._evaluate_trend(db, rule.user_id, conditions)
        elif rule.alert_type == "anomaly":
            return await AlertService._evaluate_anomaly(db, rule.user_id, conditions)

        return False

    @staticmethod
    async def _evaluate_threshold(
        db: AsyncSession,
        user_id: int,
        conditions: dict
    ) -> bool:
        """Evaluate threshold condition"""
        metric_type = conditions.get('metric')
        operator = conditions.get('operator')
        threshold = conditions.get('threshold')
        duration_minutes = conditions.get('duration_minutes', 0)

        # Get recent metrics
        start_time = datetime.utcnow() - timedelta(minutes=max(duration_minutes, 60))

        query = select(Metric).where(
            and_(
                Metric.user_id == user_id,
                Metric.metric_type == metric_type,
                Metric.timestamp >= start_time
            )
        ).order_by(Metric.timestamp.desc())

        result = await db.execute(query)
        metrics = result.scalars().all()

        if not metrics:
            return False

        # Check if condition met
        latest_value = metrics[0].value

        if operator == '>':
            condition_met = latest_value > threshold
        elif operator == '<':
            condition_met = latest_value < threshold
        elif operator == '>=':
            condition_met = latest_value >= threshold
        elif operator == '<=':
            condition_met = latest_value <= threshold
        elif operator == '==':
            condition_met = latest_value == threshold
        else:
            return False

        # If duration specified, check if condition sustained
        if duration_minutes > 0 and condition_met:
            # Check if all metrics in duration meet condition
            for metric in metrics:
                if metric.timestamp < start_time:
                    break

                value = metric.value
                if operator == '>' and value <= threshold:
                    return False
                elif operator == '<' and value >= threshold:
                    return False

        return condition_met

    @staticmethod
    async def _evaluate_trend(
        db: AsyncSession,
        user_id: int,
        conditions: dict
    ) -> bool:
        """Evaluate trend condition"""
        metric_type = conditions.get('metric')
        direction = conditions.get('direction')  # 'increasing' or 'decreasing'
        days = conditions.get('days', 7)

        # Get metrics for the period
        start_date = datetime.utcnow() - timedelta(days=days)

        query = select(Metric).where(
            and_(
                Metric.user_id == user_id,
                Metric.metric_type == metric_type,
                Metric.timestamp >= start_date
            )
        ).order_by(Metric.timestamp)

        result = await db.execute(query)
        metrics = result.scalars().all()

        if len(metrics) < 2:
            return False

        # Calculate trend
        df = pd.DataFrame([
            {"timestamp": m.timestamp, "value": m.value}
            for m in metrics
        ])

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        # Calculate linear regression
        x = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
        y = df['value']

        from scipy import stats
        slope, _, _, _, _ = stats.linregress(x, y)

        # Check direction
        if direction == 'increasing':
            return slope > 0
        elif direction == 'decreasing':
            return slope < 0

        return False

    @staticmethod
    async def _evaluate_anomaly(
        db: AsyncSession,
        user_id: int,
        conditions: dict
    ) -> bool:
        """Evaluate anomaly condition"""
        metric_type = conditions.get('metric')
        sensitivity = conditions.get('sensitivity', 2.0)
        lookback_days = conditions.get('lookback_days', 30)

        # Get baseline data
        end_date = datetime.utcnow() - timedelta(days=1)  # Exclude today
        start_date = end_date - timedelta(days=lookback_days)

        query = select(Metric).where(
            and_(
                Metric.user_id == user_id,
                Metric.metric_type == metric_type,
                Metric.timestamp >= start_date,
                Metric.timestamp <= end_date
            )
        )

        result = await db.execute(query)
        baseline_metrics = result.scalars().all()

        if not baseline_metrics:
            return False

        # Get today's value
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_query = select(Metric).where(
            and_(
                Metric.user_id == user_id,
                Metric.metric_type == metric_type,
                Metric.timestamp >= today_start
            )
        ).order_by(Metric.timestamp.desc()).limit(1)

        today_result = await db.execute(today_query)
        today_metric = today_result.scalar_one_or_none()

        if not today_metric:
            return False

        # Calculate z-score
        baseline_values = [m.value for m in baseline_metrics]
        mean = pd.Series(baseline_values).mean()
        std = pd.Series(baseline_values).std()

        if std == 0:
            return False

        z_score = abs((today_metric.value - mean) / std)

        return z_score > sensitivity

    @staticmethod
    async def _trigger_alert(
        db: AsyncSession,
        rule: AlertRule
    ):
        """Trigger an alert"""
        # Create alert
        alert = Alert(
            user_id=rule.user_id,
            alert_rule_id=rule.id,
            priority=rule.priority,
            title=rule.name,
            message=f"Alert condition met: {rule.description}",
            is_active=True,
            acknowledged=False
        )

        db.add(alert)

        # Create history entry
        history = AlertHistory(
            alert_rule_id=rule.id,
            priority=rule.priority,
            title=rule.name,
            message=f"Alert triggered: {rule.description}",
            acknowledged=False
        )

        db.add(history)

        # Update rule
        rule.last_triggered = datetime.utcnow()
        rule.trigger_count = (rule.trigger_count or 0) + 1

        await db.commit()

        # TODO: Send notifications based on delivery_methods

    @staticmethod
    async def acknowledge_alert(
        db: AsyncSession,
        alert_id: int,
        user: User
    ) -> Alert:
        """Acknowledge an alert"""
        query = select(Alert).where(
            and_(
                Alert.id == alert_id,
                Alert.user_id == user.id
            )
        )

        result = await db.execute(query)
        alert = result.scalar_one_or_none()

        if not alert:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Alert not found")

        alert.acknowledged = True
        alert.is_active = False

        await db.commit()
        await db.refresh(alert)

        return alert
