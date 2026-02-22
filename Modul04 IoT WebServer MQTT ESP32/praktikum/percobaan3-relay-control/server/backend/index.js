'use strict';

const express   = require('express');
const http      = require('http');
const { Server } = require('socket.io');
const cors      = require('cors');
const mongoose  = require('mongoose');
const mqtt      = require('mqtt');

// ─── App Setup ───────────────────────────────────────────────────────────────
const app    = express();
const server = http.createServer(app);
const io     = new Server(server, {
    cors: { origin: '*', methods: ['GET', 'POST'] }
});

const PORT       = process.env.PORT       || 3001;
// Untuk produksi gunakan: MONGO_URI=mongodb://user:pass@host:27017/percobaan3 node index.js
const MONGO_URI  = process.env.MONGO_URI  || 'mongodb://localhost:27017/percobaan3';
const MQTT_BROKER = process.env.MQTT_BROKER || 'mqtt://localhost:1883';

// ─── Middleware ───────────────────────────────────────────────────────────────
app.use(cors());
app.use(express.json());

// ─── MongoDB Schema ───────────────────────────────────────────────────────────
const statusSchema = new mongoose.Schema({
    relay1:    { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    relay2:    { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    led1:      { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    led2:      { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    uptime:    { type: Number, default: 0 },
    createdAt: { type: Date,   default: Date.now }
});
const Status = mongoose.model('Status', statusSchema);

// ─── MongoDB Connection ───────────────────────────────────────────────────────
mongoose.connect(MONGO_URI)
    .then(() => console.log(`[MongoDB] Connected: ${MONGO_URI}`))
    .catch(err => console.error('[MongoDB] Connection error:', err.message));

// ─── MQTT Client ──────────────────────────────────────────────────────────────
const mqttClient = mqtt.connect(MQTT_BROKER);

mqttClient.on('connect', () => {
    console.log(`[MQTT] Connected to broker: ${MQTT_BROKER}`);
});

mqttClient.on('error', err => {
    console.error('[MQTT] Error:', err.message);
});

// ─── Routes ───────────────────────────────────────────────────────────────────

// POST /api/status  – receive device status from Python edge
app.post('/api/status', async (req, res) => {
    try {
        const { relay1, relay2, led1, led2, uptime } = req.body;

        const doc = new Status({ relay1, relay2, led1, led2, uptime });
        await doc.save();

        const payload = { relay1, relay2, led1, led2, uptime, createdAt: doc.createdAt };
        io.emit('status', payload);

        res.status(201).json({ success: true, data: payload });
    } catch (err) {
        console.error('[POST /api/status]', err.message);
        res.status(500).json({ success: false, error: err.message });
    }
});

// GET /api/status/latest  – return latest device status
app.get('/api/status/latest', async (req, res) => {
    try {
        const doc = await Status.findOne().sort({ createdAt: -1 });
        if (!doc) return res.status(404).json({ success: false, error: 'No status yet' });
        res.json({ success: true, data: doc });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// GET /api/status/history?limit=50  – return status history
app.get('/api/status/history', async (req, res) => {
    try {
        const limit = Math.min(parseInt(req.query.limit) || 50, 200);
        const docs  = await Status.find().sort({ createdAt: -1 }).limit(limit);
        res.json({ success: true, count: docs.length, data: docs });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/command  – receive command from frontend, publish to MQTT
app.post('/api/command', (req, res) => {
    try {
        const { device, state } = req.body;

        if (!device || !state) {
            return res.status(400).json({ success: false, error: 'Missing device or state' });
        }

        const DEVICE_NUM = { relay1: 1, relay2: 2, led1: 3, led2: 4 };
        const relayNum   = DEVICE_NUM[device.toLowerCase()];

        if (state.toUpperCase() === 'ALL_OFF') {
            mqttClient.publish('control/all/off', JSON.stringify({ command: 'all_off' }));
            console.log('[MQTT] Published ALL OFF');
            return res.json({ success: true, message: 'ALL OFF sent' });
        }

        if (!relayNum) {
            return res.status(400).json({ success: false, error: `Unknown device: ${device}` });
        }

        const payload = JSON.stringify({ relay: relayNum, state: state.toUpperCase() });
        mqttClient.publish('control/relay/set', payload);
        console.log(`[MQTT] Published command: ${payload}`);

        res.json({ success: true, message: `Command sent: ${payload}` });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// ─── Socket.IO ────────────────────────────────────────────────────────────────
io.on('connection', (socket) => {
    console.log(`[Socket.IO] Client connected: ${socket.id}`);

    // Send latest status on connect
    Status.findOne().sort({ createdAt: -1 })
        .then(doc => { if (doc) socket.emit('status', doc); })
        .catch(() => {});

    socket.on('disconnect', () => {
        console.log(`[Socket.IO] Client disconnected: ${socket.id}`);
    });
});

// ─── Start Server ─────────────────────────────────────────────────────────────
server.listen(PORT, () => {
    console.log(`[Server] Percobaan 3 Backend running on http://localhost:${PORT}`);
});
