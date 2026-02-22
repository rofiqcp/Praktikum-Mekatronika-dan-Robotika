'use strict';

const path    = require('path');
const express = require('express');
const cors    = require('cors');
const Database = require('better-sqlite3');

// ─── Database setup ───────────────────────────────────────────────────────────
const DB_PATH = path.join(__dirname, '..', 'database', 'praktikum1.db');
const db = new Database(DB_PATH);

// Ensure the table exists (idempotent)
db.exec(`
  CREATE TABLE IF NOT EXISTS mqtt_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    device      TEXT    NOT NULL,
    uptime      INTEGER,
    counter     INTEGER,
    message     TEXT,
    received_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

const insertStmt = db.prepare(`
  INSERT INTO mqtt_messages (device, uptime, counter, message)
  VALUES (@device, @uptime, @counter, @message)
`);

const selectStmt = db.prepare(`
  SELECT id, device, uptime, counter, message, received_at
  FROM   mqtt_messages
  ORDER  BY received_at DESC
  LIMIT  50
`);

const countStmt = db.prepare(`SELECT COUNT(*) AS total FROM mqtt_messages`);

// ─── Express app ──────────────────────────────────────────────────────────────
const app = express();

app.use(cors());
app.use(express.json());

// Serve static frontend files
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// POST /api/data  – accept data from edge Python subscriber
app.post('/api/data', (req, res) => {
  const { device, uptime, counter, message } = req.body;

  if (!device) {
    return res.status(400).json({ error: "'device' field is required" });
  }

  try {
    const info = insertStmt.run({
      device:  device,
      uptime:  uptime  ?? null,
      counter: counter ?? null,
      message: message ?? null,
    });
    return res.json({ ok: true, id: info.lastInsertRowid });
  } catch (err) {
    console.error('[DB] Insert error:', err.message);
    return res.status(500).json({ error: 'Database error' });
  }
});

// GET /api/data  – return last 50 records
app.get('/api/data', (req, res) => {
  try {
    const rows  = selectStmt.all();
    const total = countStmt.get().total;
    return res.json({ total, data: rows });
  } catch (err) {
    console.error('[DB] Select error:', err.message);
    return res.status(500).json({ error: 'Database error' });
  }
});

// Fallback – serve index.html for any unmatched GET (SPA support)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
});

// ─── Start server ─────────────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[Server] Percobaan 1 backend running on http://localhost:${PORT}`);
  console.log(`[DB]     SQLite database at ${DB_PATH}`);
});
