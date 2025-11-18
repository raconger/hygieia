"""
Garmin Connect API integration
"""
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectAuthenticationError
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GarminClient:
    """Client for interacting with Garmin Connect API"""

    def __init__(self, email: str = None, password: str = None):
        """
        Initialize Garmin client

        Note: This uses email/password authentication. For production,
        should use OAuth 2.0 with the official Garmin Health API.
        """
        self.email = email
        self.password = password
        self.client = None

    def authenticate(self) -> bool:
        """Authenticate with Garmin Connect"""
        try:
            self.client = Garmin(self.email, self.password)
            self.client.login()
            logger.info("Successfully authenticated with Garmin Connect")
            return True
        except GarminConnectAuthenticationError as e:
            logger.error(f"Garmin authentication failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Garmin connection error: {e}")
            return False

    def get_heart_rate_data(self, date: datetime) -> List[Dict[str, Any]]:
        """Get heart rate data for a specific date"""
        if not self.client:
            raise Exception("Not authenticated with Garmin")

        try:
            date_str = date.strftime("%Y-%m-%d")
            hr_data = self.client.get_heart_rates(date_str)
            return hr_data
        except Exception as e:
            logger.error(f"Failed to fetch heart rate data: {e}")
            return []

    def get_sleep_data(self, date: datetime) -> Dict[str, Any]:
        """Get sleep data for a specific date"""
        if not self.client:
            raise Exception("Not authenticated with Garmin")

        try:
            date_str = date.strftime("%Y-%m-%d")
            sleep_data = self.client.get_sleep_data(date_str)
            return sleep_data
        except Exception as e:
            logger.error(f"Failed to fetch sleep data: {e}")
            return {}

    def get_daily_stats(self, date: datetime) -> Dict[str, Any]:
        """Get daily stats (steps, calories, etc.)"""
        if not self.client:
            raise Exception("Not authenticated with Garmin")

        try:
            date_str = date.strftime("%Y-%m-%d")
            stats = self.client.get_stats(date_str)
            return stats
        except Exception as e:
            logger.error(f"Failed to fetch daily stats: {e}")
            return {}

    def get_activities(self, start_date: datetime, end_date: datetime = None) -> List[Dict[str, Any]]:
        """Get activities in a date range"""
        if not self.client:
            raise Exception("Not authenticated with Garmin")

        try:
            if end_date is None:
                end_date = datetime.now()

            activities = self.client.get_activities_by_date(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            return activities
        except Exception as e:
            logger.error(f"Failed to fetch activities: {e}")
            return []

    def get_body_composition(self, date: datetime) -> Dict[str, Any]:
        """Get body composition data"""
        if not self.client:
            raise Exception("Not authenticated with Garmin")

        try:
            date_str = date.strftime("%Y-%m-%d")
            body_comp = self.client.get_body_composition(date_str)
            return body_comp
        except Exception as e:
            logger.error(f"Failed to fetch body composition: {e}")
            return {}

    def get_stress_data(self, date: datetime) -> List[Dict[str, Any]]:
        """Get stress data for a specific date"""
        if not self.client:
            raise Exception("Not authenticated with Garmin")

        try:
            date_str = date.strftime("%Y-%m-%d")
            stress_data = self.client.get_stress_data(date_str)
            return stress_data
        except Exception as e:
            logger.error(f"Failed to fetch stress data: {e}")
            return []

    def sync_all_data(self, start_date: datetime, end_date: datetime = None) -> Dict[str, Any]:
        """
        Sync all available data for a date range

        Returns a dictionary with all collected data
        """
        if end_date is None:
            end_date = datetime.now()

        results = {
            "heart_rate": [],
            "sleep": [],
            "stats": [],
            "activities": [],
            "body_composition": [],
            "stress": []
        }

        # Fetch data for each day in the range
        current_date = start_date
        while current_date <= end_date:
            try:
                # Heart rate
                hr_data = self.get_heart_rate_data(current_date)
                if hr_data:
                    results["heart_rate"].extend(hr_data)

                # Sleep
                sleep_data = self.get_sleep_data(current_date)
                if sleep_data:
                    results["sleep"].append(sleep_data)

                # Daily stats
                stats = self.get_daily_stats(current_date)
                if stats:
                    results["stats"].append(stats)

                # Body composition
                body_comp = self.get_body_composition(current_date)
                if body_comp:
                    results["body_composition"].append(body_comp)

                # Stress
                stress_data = self.get_stress_data(current_date)
                if stress_data:
                    results["stress"].extend(stress_data)

            except Exception as e:
                logger.error(f"Error syncing data for {current_date}: {e}")

            current_date += timedelta(days=1)

        # Fetch activities for the entire range
        activities = self.get_activities(start_date, end_date)
        results["activities"] = activities

        return results


def normalize_garmin_data(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize Garmin data into standard metric format

    Args:
        raw_data: Raw data from Garmin API

    Returns:
        List of normalized metrics ready for database insertion
    """
    normalized_metrics = []

    # TODO: Implement data normalization
    # Convert Garmin-specific data format to our standard metric format
    # Extract timestamps, values, units, etc.

    return normalized_metrics
