-- PostgreSQL initialisation script for Percobaan 2
-- Run as a superuser, or as the target user after creating the database manually.

-- Create the database (run this part connected to the 'postgres' database)
-- Uncomment if running from psql as superuser:
-- CREATE DATABASE iot_db;
-- \c iot_db;

-- ── Sensor readings table ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sensor_readings (
    id          SERIAL PRIMARY KEY,
    device      VARCHAR(50),
    temperature FLOAT,
    humidity    FLOAT,
    heat_index  FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast time-range queries
CREATE INDEX IF NOT EXISTS idx_recorded_at ON sensor_readings(recorded_at);
