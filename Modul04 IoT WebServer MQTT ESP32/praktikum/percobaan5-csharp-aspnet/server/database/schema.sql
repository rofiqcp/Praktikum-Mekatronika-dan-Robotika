-- Percobaan 5: Skema SQLite (Referensi)
-- EF Core membuat tabel ini secara otomatis via migration.
-- File ini hanya untuk referensi dokumentasi.

CREATE TABLE IF NOT EXISTS SensorReadings (
    Id         INTEGER PRIMARY KEY AUTOINCREMENT,
    Device     TEXT    NOT NULL DEFAULT 'UNKNOWN',
    LightRaw   INTEGER NOT NULL DEFAULT 0,
    LightPct   INTEGER NOT NULL DEFAULT 0,
    PotRaw     INTEGER NOT NULL DEFAULT 0,
    PotPct     INTEGER NOT NULL DEFAULT 0,
    Uptime     INTEGER NOT NULL DEFAULT 0,
    ReceivedAt TEXT    NOT NULL  -- ISO 8601 UTC, disimpan oleh EF Core
);

-- Index untuk query ORDER BY ReceivedAt DESC
CREATE INDEX IF NOT EXISTS IX_SensorReadings_ReceivedAt
    ON SensorReadings (ReceivedAt DESC);
