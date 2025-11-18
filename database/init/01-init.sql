-- Initialize Hygieia database
-- This script runs when the database container is first created

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create hypertable for metrics (time-series optimized)
-- Note: This will be executed after tables are created by SQLAlchemy
-- You may need to run this manually or through alembic migration

-- CREATE HYPERTABLE IF NOT EXISTS metrics (timestamp);

-- Create indexes for better query performance
-- These will be created by SQLAlchemy models, but can be added here if needed

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE hygieia TO hygieia;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hygieia;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hygieia;

-- Create data retention policies (example)
-- SELECT add_retention_policy('metrics', INTERVAL '1 year');

-- Create continuous aggregates for common queries (example)
-- CREATE MATERIALIZED VIEW metrics_hourly
-- WITH (timescaledb.continuous) AS
-- SELECT
--   time_bucket('1 hour', timestamp) AS hour,
--   metric_type,
--   AVG(value) as avg_value,
--   MAX(value) as max_value,
--   MIN(value) as min_value
-- FROM metrics
-- GROUP BY hour, metric_type;

-- Create refresh policy for continuous aggregate
-- SELECT add_continuous_aggregate_policy('metrics_hourly',
--   start_offset => INTERVAL '3 hours',
--   end_offset => INTERVAL '1 hour',
--   schedule_interval => INTERVAL '1 hour');
