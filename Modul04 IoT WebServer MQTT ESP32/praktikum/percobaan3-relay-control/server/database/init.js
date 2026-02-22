'use strict';
/**
 * database/init.js
 * Inisialisasi MongoDB untuk Percobaan 3.
 * Jalankan sekali: node database/init.js
 */

const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/percobaan3';

const statusSchema = new mongoose.Schema({
    relay1:    { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    relay2:    { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    led1:      { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    led2:      { type: String, enum: ['ON', 'OFF'], default: 'OFF' },
    uptime:    { type: Number, default: 0 },
    createdAt: { type: Date,   default: Date.now }
});

const Status = mongoose.model('Status', statusSchema);

async function init() {
    try {
        await mongoose.connect(MONGO_URI);
        console.log(`[MongoDB] Connected: ${MONGO_URI}`);

        // Create indexes
        await Status.collection.createIndex({ createdAt: -1 });
        console.log('[MongoDB] Index on createdAt created');

        // Seed initial status record
        const existing = await Status.countDocuments();
        if (existing === 0) {
            await Status.create({
                relay1:    'OFF',
                relay2:    'OFF',
                led1:      'OFF',
                led2:      'OFF',
                uptime:    0,
                createdAt: new Date()
            });
            console.log('[MongoDB] Seeded initial status document');
        } else {
            console.log(`[MongoDB] Collection already has ${existing} documents; skipping seed`);
        }

        console.log('[MongoDB] Initialization complete');
    } catch (err) {
        console.error('[MongoDB] Error:', err.message);
        process.exit(1);
    } finally {
        await mongoose.disconnect();
    }
}

init();
