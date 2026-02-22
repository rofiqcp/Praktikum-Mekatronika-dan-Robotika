-- PostgreSQL DDL for Percobaan 4: Multi-Sensor Dashboard
-- Jalankan sebagai user postgres: psql -U postgres -f init.sql

-- ── Database ─────────────────────────────────────────────────────────────────
CREATE DATABASE iot_praktikum
    WITH ENCODING = 'UTF8'
         LC_COLLATE = 'en_US.utf8'
         LC_CTYPE   = 'en_US.utf8';

\connect iot_praktikum;

-- ── Table ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sensor_readings (
    id             BIGSERIAL    PRIMARY KEY,
    device         VARCHAR(64)  NOT NULL,
    temperature    NUMERIC(6,2),
    humidity       NUMERIC(6,2),
    light          INTEGER      CHECK (light       BETWEEN 0 AND 100),
    soil_moisture  INTEGER      CHECK (soil_moisture BETWEEN 0 AND 100),
    battery        NUMERIC(4,2),
    recorded_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    location       VARCHAR(128)
);

-- ── Indexes ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_recorded_at  ON sensor_readings (recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_device       ON sensor_readings (device);
CREATE INDEX IF NOT EXISTS idx_device_time  ON sensor_readings (device, recorded_at DESC);

-- ── Seed Data (sample readings) ───────────────────────────────────────────────
INSERT INTO sensor_readings (device, temperature, humidity, light, soil_moisture, battery, recorded_at, location)
VALUES
    ('ESP32-MULTI', 25.4, 62.1, 78, 45, 3.7, NOW() - INTERVAL '5 minutes',  'Lab Mekatronika - Ruang B204'),
    ('ESP32-MULTI', 25.6, 61.8, 80, 44, 3.7, NOW() - INTERVAL '10 minutes', 'Lab Mekatronika - Ruang B204'),
    ('ESP32-MULTI', 25.1, 63.0, 75, 46, 3.7, NOW() - INTERVAL '15 minutes', 'Lab Mekatronika - Ruang B204'),
    ('ESP32-MULTI', 24.9, 63.5, 72, 47, 3.7, NOW() - INTERVAL '20 minutes', 'Lab Mekatronika - Ruang B204'),
    ('ESP32-MULTI', 24.7, 64.0, 70, 48, 3.7, NOW() - INTERVAL '25 minutes', 'Lab Mekatronika - Ruang B204');

-- ── Verify ────────────────────────────────────────────────────────────────────
SELECT COUNT(*) AS total_rows FROM sensor_readings;
