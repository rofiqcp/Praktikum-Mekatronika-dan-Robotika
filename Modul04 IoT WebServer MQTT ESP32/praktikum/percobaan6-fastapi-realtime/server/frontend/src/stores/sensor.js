// Percobaan 6 – Frontend: Pinia store untuk data sensor real-time via WebSocket

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const MAX_READINGS = 100;
const MAX_ALERTS   = 20;
const WS_URL       = 'ws://localhost:8000/ws';
const PING_INTERVAL_MS = 25000;

export const useSensorStore = defineStore('sensor', () => {
  const readings       = ref([]);
  const alerts         = ref([]);
  const currentReading = ref(null);
  const isConnected    = ref(false);

  let ws          = null;
  let pingTimer   = null;
  let reconnTimer = null;

  // ── Computed ───────────────────────────────────────────────────────────────
  const latestTemperature = computed(() => currentReading.value?.temperature ?? null);
  const latestHumidity    = computed(() => currentReading.value?.humidity    ?? null);
  const latestGasPpm      = computed(() => currentReading.value?.gas_ppm     ?? null);
  const latestMotion      = computed(() => currentReading.value?.motion      ?? false);

  const tempHistory = computed(() =>
    readings.value
      .filter(r => r._type === 'sensor' && r.temperature != null)
      .slice(0, 20)
      .map(r => ({ t: r.timestamp, v: r.temperature }))
      .reverse()
  );

  // ── Actions ────────────────────────────────────────────────────────────────
  function addReading(data) {
    readings.value.unshift(data);
    if (readings.value.length > MAX_READINGS) {
      readings.value.splice(MAX_READINGS);
    }
    currentReading.value = data;
  }

  function addAlert(data) {
    alerts.value.unshift(data);
    if (alerts.value.length > MAX_ALERTS) {
      alerts.value.splice(MAX_ALERTS);
    }
  }

  function connect() {
    if (ws && ws.readyState === WebSocket.OPEN) return;

    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      isConnected.value = true;
      console.log('[WS] Terhubung ke', WS_URL);
      pingTimer = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) ws.send('ping');
      }, PING_INTERVAL_MS);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'pong') return;

        if (data._type === 'sensor') {
          addReading(data);
        } else if (data._type === 'alert' || data.alert) {
          addAlert(data);
        } else {
          // Tipe tidak diketahui – coba simpan sebagai sensor
          addReading(data);
        }
      } catch (e) {
        console.warn('[WS] Parse error:', e);
      }
    };

    ws.onclose = () => {
      isConnected.value = false;
      clearInterval(pingTimer);
      console.warn('[WS] Terputus. Reconnect dalam 5 detik...');
      reconnTimer = setTimeout(connect, 5000);
    };

    ws.onerror = (err) => {
      console.error('[WS] Error:', err);
      ws.close();
    };
  }

  function disconnect() {
    clearInterval(pingTimer);
    clearTimeout(reconnTimer);
    if (ws) {
      ws.onclose = null; // cegah auto-reconnect
      ws.close();
      ws = null;
    }
    isConnected.value = false;
  }

  return {
    readings,
    alerts,
    currentReading,
    isConnected,
    latestTemperature,
    latestHumidity,
    latestGasPpm,
    latestMotion,
    tempHistory,
    connect,
    disconnect,
    addReading,
    addAlert,
  };
});
