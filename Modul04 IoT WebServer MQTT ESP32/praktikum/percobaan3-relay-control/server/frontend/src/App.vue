<template>
  <div class="container">
    <header>
      <h1>🔌 Percobaan 3 – Remote Relay &amp; LED Control</h1>
      <p class="subtitle">Real-time control via MQTT · Socket.IO</p>
    </header>

    <!-- ── Status Cards ────────────────────────────────────── -->
    <section class="cards">
      <div
        v-for="device in devices"
        :key="device.key"
        :class="['card', status[device.key] === 'ON' ? 'on' : 'off']"
      >
        <div class="card-icon">{{ device.icon }}</div>
        <div class="card-name">{{ device.label }}</div>
        <div class="card-state">{{ status[device.key] || '…' }}</div>
        <button
          class="toggle-btn"
          @click="toggleDevice(device.key)"
          :disabled="sending"
        >
          {{ status[device.key] === 'ON' ? 'Turn OFF' : 'Turn ON' }}
        </button>
      </div>
    </section>

    <!-- ── Emergency Button ────────────────────────────────── -->
    <section class="emergency">
      <button class="all-off-btn" @click="sendAllOff" :disabled="sending">
        ⚠️ ALL OFF (Emergency)
      </button>
    </section>

    <!-- ── Uptime ──────────────────────────────────────────── -->
    <section class="meta" v-if="status.uptime !== undefined">
      <span>Device uptime: <strong>{{ status.uptime }}s</strong></span>
      <span>Last update: <strong>{{ lastUpdated }}</strong></span>
      <span :class="['conn-dot', connected ? 'live' : 'dead']">
        {{ connected ? '● Live' : '○ Disconnected' }}
      </span>
    </section>

    <!-- ── Log ────────────────────────────────────────────── -->
    <section class="log-section">
      <h2>Status Log (last 20 events)</h2>
      <div class="log-box" ref="logBox">
        <div v-if="logs.length === 0" class="log-empty">Menunggu data dari ESP32…</div>
        <div v-for="(entry, i) in logs" :key="i" class="log-entry">
          <span class="log-ts">{{ entry.ts }}</span>
          <span class="log-msg">
            R1:<b :class="entry.relay1">{{ entry.relay1 }}</b>
            R2:<b :class="entry.relay2">{{ entry.relay2 }}</b>
            L1:<b :class="entry.led1">{{ entry.led1 }}</b>
            L2:<b :class="entry.led2">{{ entry.led2 }}</b>
            uptime:{{ entry.uptime }}s
          </span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { io } from 'socket.io-client';

// ─── State ─────────────────────────────────────────────────
const status      = ref({ relay1: 'OFF', relay2: 'OFF', led1: 'OFF', led2: 'OFF', uptime: 0 });
const logs        = ref([]);
const connected   = ref(false);
const sending     = ref(false);
const lastUpdated = ref('—');
const logBox      = ref(null);

const devices = [
  { key: 'relay1', label: 'Relay 1', icon: '⚡' },
  { key: 'relay2', label: 'Relay 2', icon: '⚡' },
  { key: 'led1',   label: 'LED 1',   icon: '💡' },
  { key: 'led2',   label: 'LED 2',   icon: '💡' },
];

const DEVICE_NUM = { relay1: 1, relay2: 2, led1: 3, led2: 4 };

// ─── Socket.IO ────────────────────────────────────────────
let socket;

function handleStatus(data) {
  status.value = { ...status.value, ...data };
  lastUpdated.value = new Date().toLocaleTimeString('id-ID');
  addLog(data);
}

function addLog(data) {
  logs.value.unshift({
    ts:     new Date().toLocaleTimeString('id-ID'),
    relay1: data.relay1 || '?',
    relay2: data.relay2 || '?',
    led1:   data.led1   || '?',
    led2:   data.led2   || '?',
    uptime: data.uptime ?? '?',
  });
  if (logs.value.length > 20) logs.value.pop();
  nextTick(() => {
    if (logBox.value) logBox.value.scrollTop = 0;
  });
}

// ─── Commands ─────────────────────────────────────────────
async function toggleDevice(key) {
  const newState = status.value[key] === 'ON' ? 'OFF' : 'ON';
  await sendCommand(key, newState);
}

async function sendCommand(device, state) {
  sending.value = true;
  try {
    const res = await fetch('/api/command', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ device, state }),
    });
    if (!res.ok) {
      const err = await res.json();
      console.error('[API] Command error:', err);
    }
  } catch (e) {
    console.error('[fetch] Error:', e);
  } finally {
    sending.value = false;
  }
}

async function sendAllOff() {
  sending.value = true;
  try {
    await fetch('/api/command', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ device: 'all', state: 'ALL_OFF' }),
    });
  } catch (e) {
    console.error('[fetch] Error:', e);
  } finally {
    sending.value = false;
  }
}

// ─── Lifecycle ────────────────────────────────────────────
onMounted(async () => {
  // Fetch latest status via REST
  try {
    const res  = await fetch('/api/status/latest');
    const json = await res.json();
    if (json.success) handleStatus(json.data);
  } catch (_) {}

  // Connect Socket.IO
  socket = io('http://localhost:3001', { transports: ['websocket', 'polling'] });
  socket.on('connect',    () => { connected.value = true; });
  socket.on('disconnect', () => { connected.value = false; });
  socket.on('status',     handleStatus);
});

onBeforeUnmount(() => {
  if (socket) socket.disconnect();
});
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

.container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 16px;
  background: #f0f4f8;
  min-height: 100vh;
}

header { text-align: center; margin-bottom: 28px; }
header h1 { font-size: 1.8rem; color: #1a202c; }
.subtitle { color: #718096; margin-top: 4px; }

/* ── Cards ─────────────────────────────────────────────── */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.card {
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,.12);
  transition: transform .15s;
}
.card:hover { transform: translateY(-2px); }

.card.on  { background: #c6f6d5; border: 2px solid #38a169; }
.card.off { background: #fed7d7; border: 2px solid #e53e3e; }

.card-icon  { font-size: 2rem; margin-bottom: 8px; }
.card-name  { font-weight: 600; color: #2d3748; margin-bottom: 4px; }
.card-state { font-size: 1.4rem; font-weight: 700; margin-bottom: 12px; }
.card.on  .card-state { color: #276749; }
.card.off .card-state { color: #c53030; }

.toggle-btn {
  padding: 6px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  background: #2b6cb0;
  color: #fff;
  transition: background .15s;
}
.toggle-btn:hover:not(:disabled) { background: #2c5282; }
.toggle-btn:disabled { opacity: .5; cursor: not-allowed; }

/* ── Emergency ─────────────────────────────────────────── */
.emergency { text-align: center; margin-bottom: 20px; }
.all-off-btn {
  padding: 12px 36px;
  font-size: 1.1rem;
  font-weight: 700;
  background: #e53e3e;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background .15s;
}
.all-off-btn:hover:not(:disabled) { background: #c53030; }
.all-off-btn:disabled { opacity: .5; cursor: not-allowed; }

/* ── Meta ──────────────────────────────────────────────── */
.meta {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
  font-size: .9rem;
  color: #4a5568;
  flex-wrap: wrap;
}
.conn-dot { font-weight: 700; }
.conn-dot.live  { color: #38a169; }
.conn-dot.dead  { color: #e53e3e; }

/* ── Log ───────────────────────────────────────────────── */
.log-section h2 {
  font-size: 1.1rem;
  color: #2d3748;
  margin-bottom: 10px;
}

.log-box {
  background: #1a202c;
  border-radius: 8px;
  padding: 12px;
  max-height: 320px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: .82rem;
}

.log-empty { color: #718096; text-align: center; padding: 16px; }

.log-entry {
  display: flex;
  gap: 12px;
  padding: 4px 0;
  border-bottom: 1px solid #2d3748;
  color: #e2e8f0;
}

.log-ts  { color: #68d391; min-width: 80px; }
.log-msg b.ON  { color: #68d391; }
.log-msg b.OFF { color: #fc8181; }
</style>
