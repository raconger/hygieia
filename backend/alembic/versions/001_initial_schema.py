"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-11-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create data_sources table
    op.create_table('data_sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('requires_oauth', sa.Boolean(), nullable=True),
    sa.Column('api_endpoint', sa.String(), nullable=True),
    sa.Column('api_version', sa.String(), nullable=True),
    sa.Column('rate_limit', sa.Integer(), nullable=True),
    sa.Column('supported_metrics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    # Create data_source_auth table
    op.create_table('data_source_auth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('data_source_id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.Text(), nullable=True),
    sa.Column('refresh_token', sa.Text(), nullable=True),
    sa.Column('token_expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('credentials', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_sync', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_sync_status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create metrics table
    op.create_table('metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('metric_type', sa.String(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('quality_score', sa.Float(), nullable=True),
    sa.Column('is_manual', sa.Integer(), nullable=True),
    sa.Column('synced_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_metric_source_time', 'metrics', ['metric_type', 'source', 'timestamp'], unique=False)
    op.create_index('idx_user_metric_time', 'metrics', ['user_id', 'metric_type', 'timestamp'], unique=False)
    op.create_index('idx_user_time', 'metrics', ['user_id', 'timestamp'], unique=False)
    op.create_index(op.f('ix_metrics_id'), 'metrics', ['id'], unique=False)
    op.create_index(op.f('ix_metrics_metric_type'), 'metrics', ['metric_type'], unique=False)
    op.create_index(op.f('ix_metrics_source'), 'metrics', ['source'], unique=False)
    op.create_index(op.f('ix_metrics_timestamp'), 'metrics', ['timestamp'], unique=False)

    # Convert metrics to hypertable (TimescaleDB)
    op.execute("SELECT create_hypertable('metrics', 'timestamp', if_not_exists => TRUE);")

    # Create activities table
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('activity_type', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('duration_seconds', sa.Integer(), nullable=True),
    sa.Column('distance_meters', sa.Float(), nullable=True),
    sa.Column('elevation_gain_meters', sa.Float(), nullable=True),
    sa.Column('elevation_loss_meters', sa.Float(), nullable=True),
    sa.Column('avg_pace', sa.Float(), nullable=True),
    sa.Column('avg_speed', sa.Float(), nullable=True),
    sa.Column('max_speed', sa.Float(), nullable=True),
    sa.Column('avg_power', sa.Float(), nullable=True),
    sa.Column('max_power', sa.Float(), nullable=True),
    sa.Column('avg_heart_rate', sa.Float(), nullable=True),
    sa.Column('max_heart_rate', sa.Float(), nullable=True),
    sa.Column('calories', sa.Integer(), nullable=True),
    sa.Column('training_load', sa.Float(), nullable=True),
    sa.Column('perceived_effort', sa.Integer(), nullable=True),
    sa.Column('location_name', sa.String(), nullable=True),
    sa.Column('start_latitude', sa.Float(), nullable=True),
    sa.Column('start_longitude', sa.Float(), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('synced_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_activity_type_time', 'activities', ['activity_type', 'start_time'], unique=False)
    op.create_index('idx_user_activity_time', 'activities', ['user_id', 'start_time'], unique=False)
    op.create_index(op.f('ix_activities_external_id'), 'activities', ['external_id'], unique=False)
    op.create_index(op.f('ix_activities_start_time'), 'activities', ['start_time'], unique=False)

    # Create alert_rules table
    op.create_table('alert_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('alert_type', sa.String(), nullable=False),
    sa.Column('priority', sa.String(), nullable=True),
    sa.Column('conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('delivery_methods', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('quiet_hours_start', sa.Integer(), nullable=True),
    sa.Column('quiet_hours_end', sa.Integer(), nullable=True),
    sa.Column('weekdays_only', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_triggered', sa.DateTime(timezone=True), nullable=True),
    sa.Column('trigger_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create alerts table
    op.create_table('alerts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('alert_rule_id', sa.Integer(), nullable=True),
    sa.Column('priority', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['alert_rule_id'], ['alert_rules.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create alert_history table
    op.create_table('alert_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alert_rule_id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('metric_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('delivery_status', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=True),
    sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('snoozed_until', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['alert_rule_id'], ['alert_rules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('alert_history')
    op.drop_table('alerts')
    op.drop_table('alert_rules')
    op.drop_index('idx_user_activity_time', table_name='activities')
    op.drop_index('idx_activity_type_time', table_name='activities')
    op.drop_index(op.f('ix_activities_start_time'), table_name='activities')
    op.drop_index(op.f('ix_activities_external_id'), table_name='activities')
    op.drop_table('activities')
    op.drop_index('idx_user_time', table_name='metrics')
    op.drop_index('idx_user_metric_time', table_name='metrics')
    op.drop_index('idx_metric_source_time', table_name='metrics')
    op.drop_index(op.f('ix_metrics_timestamp'), table_name='metrics')
    op.drop_index(op.f('ix_metrics_source'), table_name='metrics')
    op.drop_index(op.f('ix_metrics_metric_type'), table_name='metrics')
    op.drop_index(op.f('ix_metrics_id'), table_name='metrics')
    op.drop_table('metrics')
    op.drop_table('data_source_auth')
    op.drop_table('data_sources')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
