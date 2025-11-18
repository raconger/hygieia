# API Guide

Complete guide to the Hygieia API.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication using JWT tokens.

### Login

```bash
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Using the token

Include the token in the Authorization header:

```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Endpoints

### Metrics

#### Get Metrics

```bash
GET /api/v1/metrics
```

Query Parameters:
- `metric_type` (optional): Filter by metric type
- `source` (optional): Filter by data source
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `time_range` (optional): Predefined range (7d, 30d, 90d, 1y, all)
- `limit` (optional): Maximum results (default: 1000, max: 10000)

Example:
```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/metrics?metric_type=heart_rate&time_range=7d"
```

#### Get Metric Types

```bash
GET /api/v1/metrics/types
```

Returns available metric categories and types.

#### Get Metric Summary

```bash
GET /api/v1/metrics/summary?metric_type=heart_rate&time_range=30d
```

Returns statistical summary (mean, median, min, max, std).

#### Create Metric (Manual Entry)

```bash
POST /api/v1/metrics
Content-Type: application/json

{
  "metric_type": "weight",
  "value": 75.5,
  "unit": "kg",
  "source": "manual"
}
```

### Synchronization

#### Trigger Sync

```bash
POST /api/v1/sync/trigger
Content-Type: application/json

{
  "sources": ["garmin", "oura"],
  "backfill_days": 7
}
```

#### Get Sync Status

```bash
GET /api/v1/sync/status
```

Returns status of all data sources.

### Trends

#### Get Trend

```bash
GET /api/v1/trends/heart_rate?start_date=2024-01-01&interval=day&moving_average_window=7
```

Query Parameters:
- `start_date` (optional): Start date
- `end_date` (optional): End date
- `interval` (optional): hour, day, week, month
- `moving_average_window` (optional): Window size for MA (default: 7)

#### Compare Periods

```bash
GET /api/v1/trends/compare/heart_rate?period=week
```

Compares current period with previous period.

#### Calendar Heatmap

```bash
GET /api/v1/trends/calendar/steps?year=2024
```

Returns daily aggregated data for calendar visualization.

### Analytics

#### Get Correlations

```bash
GET /api/v1/analytics/correlations?metric=hrv&min_correlation=0.3
```

Returns correlations between metrics.

#### Specific Correlation

```bash
GET /api/v1/analytics/correlations/sleep_duration/hrv?method=pearson
```

#### Detect Anomalies

```bash
GET /api/v1/analytics/anomalies/heart_rate?sensitivity=2.0&lookback_days=30
```

#### Segment Comparison

```bash
GET /api/v1/analytics/segment-comparison/hrv?segment_by=day_of_week
```

Compare metrics across segments (day of week, activity type, etc).

### Alerts

#### Get Alerts

```bash
GET /api/v1/alerts?active_only=true
```

#### Get Alert Rules

```bash
GET /api/v1/alerts/rules
```

#### Create Alert Rule

```bash
POST /api/v1/alerts/rules
Content-Type: application/json

{
  "name": "High Resting HR",
  "description": "Alert when resting HR exceeds 65 bpm",
  "alert_type": "threshold",
  "priority": "warning",
  "conditions": {
    "metric": "resting_hr",
    "operator": ">",
    "threshold": 65
  },
  "delivery_methods": ["in_app", "email"],
  "is_active": true
}
```

#### Acknowledge Alert

```bash
POST /api/v1/alerts/{alert_id}/acknowledge
```

#### Snooze Alert

```bash
POST /api/v1/alerts/{alert_id}/snooze?hours=2
```

## Rate Limiting

API requests are rate-limited to 60 requests per minute per IP address.

Rate limit headers:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window

## Error Responses

The API uses standard HTTP status codes:

- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

## Interactive Documentation

Visit http://localhost:8000/docs for interactive API documentation with Swagger UI.

## Examples

### Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/v1/auth/token',
    data={'username': 'user@example.com', 'password': 'password'})
token = response.json()['access_token']

# Get metrics
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/v1/metrics',
    headers=headers,
    params={'metric_type': 'heart_rate', 'time_range': '7d'})
metrics = response.json()
```

### JavaScript

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=user@example.com&password=password'
});
const { access_token } = await loginResponse.json();

// Get metrics
const metricsResponse = await fetch(
  'http://localhost:8000/api/v1/metrics?metric_type=heart_rate&time_range=7d',
  { headers: { 'Authorization': `Bearer ${access_token}` } }
);
const metrics = await metricsResponse.json();
```
