<template>
  <!-- Percobaan 6 – App.vue: Dashboard Utama Real-Time -->
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div>
        <h1>⚡ Real-Time IoT Dashboard</h1>
        <p class="sub">Percobaan 6 – FastAPI + WebSocket + Vue.js 3 + MongoDB</p>
      </div>
      <div class="ws-status" :class="{ connected: store.isConnected }">
        <span class="dot" />
        {{ store.isConnected ? 'WebSocket Terhubung' : 'Menghubungkan...' }}
      </div>
    </header>

    <!-- Gauge metrik -->
    <section class="section">
      <h2 class="section-title">📊 Sensor Saat Ini</h2>
      <div class="gauges">
        <MetricGauge
          label="Suhu"
          :value="store.latestTemperature"
          unit="°C"
          icon="🌡️"
          :min="0" :max="60"
          :warnAt="35" :dangerAt="45"
          :decimals="1"
        />
        <MetricGauge
          label="Kelembaban"
          :value="store.latestHumidity"
          unit="%"
          icon="💧"
          :min="0" :max="100"
          :warnAt="80" :dangerAt="90"
          :decimals="1"
        />
        <MetricGauge
          label="Gas (ppm)"
          :value="store.latestGasPpm"
          unit="ppm"
          icon="💨"
          :min="0" :max="1000"
          :warnAt="300" :dangerAt="400"
          :decimals="0"
        />
        <div class="motion-card" :class="{ active: store.latestMotion }">
          <div class="motion-icon">{{ store.latestMotion ? '🚨' : '🔵' }}</div>
          <div class="motion-label">PIR Motion</div>
          <div class="motion-value" :class="{ danger: store.latestMotion }">
            {{ store.latestMotion ? 'TERDETEKSI' : 'Aman' }}
          </div>
        </div>
      </div>
    </section>

    <!-- Grafik suhu -->
    <section class="section">
      <h2 class="section-title">📈 Riwayat Suhu (20 data terakhir)</h2>
      <RealtimeChart
        :data="store.tempHistory"
        title="Suhu (°C)"
        unit="°C"
        color="#f87171"
        :minVal="15" :maxVal="60"
      />
    </section>

    <!-- Alert -->
    <section class="section">
      <h2 class="section-title">🔔 Alert Terbaru</h2>
      <AlertList :alerts="store.alerts" />
    </section>

    <!-- Tabel data mentah -->
    <section class="section">
      <h2 class="section-title">📋 Data Terbaru ({{ store.readings.length }} entri)</h2>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Waktu</th><th>Device</th><th>Suhu</th>
              <th>Hum</th><th>Gas ppm</th><th>Motion</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(r, i) in store.readings.filter(x => x._type === 'sensor').slice(0, 20)"
              :key="r.timestamp + i"
            >
              <td>{{ formatTime(r.timestamp) }}</td>
              <td>{{ r.device }}</td>
              <td>{{ r.temperature?.toFixed(1) }}°C</td>
              <td>{{ r.humidity?.toFixed(1) }}%</td>
              <td>{{ r.gas_ppm?.toFixed(0) }}</td>
              <td>{{ r.motion ? '🚶 Ya' : '–' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import { useSensorStore } from './stores/sensor.js';
import MetricGauge  from './components/MetricGauge.vue';
import AlertList    from './components/AlertList.vue';
import RealtimeChart from './components/RealtimeChart.vue';

const store = useSensorStore();

onMounted(() => store.connect());
onUnmounted(() => store.disconnect());

function formatTime(ts) {
  if (!ts) return '';
  return new Date(ts).toLocaleTimeString('id-ID');
}
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a;
  color: #e2e8f0;
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
}
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1e293b; }
::-webkit-scrollbar-thumb { background: #475569; border-radius: 3px; }
</style>

<style scoped>
.app     { max-width: 1100px; margin: 0 auto; padding: 24px 16px; }

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 12px;
}
h1      { font-size: 22px; color: #38bdf8; }
.sub    { color: #64748b; font-size: 13px; margin-top: 4px; }

.ws-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #ef4444;
  padding: 6px 12px;
  background: #1e293b;
  border-radius: 20px;
  border: 1px solid #ef444444;
}
.ws-status.connected { color: #22c55e; border-color: #22c55e44; }
.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:0.4 } }

.section       { margin-bottom: 28px; }
.section-title { font-size: 15px; color: #94a3b8; margin-bottom: 12px; }

.gauges {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.motion-card {
  background: #1e293b;
  border: 2px solid #22c55e;
  border-radius: 12px;
  padding: 16px 20px;
  min-width: 150px;
  text-align: center;
  transition: border-color 0.3s;
}
.motion-card.active { border-color: #ef4444; }
.motion-icon  { font-size: 28px; margin-bottom: 6px; }
.motion-label { color: #94a3b8; font-size: 12px; margin-bottom: 8px; }
.motion-value { font-size: 20px; font-weight: 700; color: #22c55e; }
.motion-value.danger { color: #ef4444; animation: blink 0.8s infinite; }
@keyframes blink { 0%,100% { opacity:1 } 50% { opacity:0.3 } }

.table-wrap  { overflow-x: auto; }
.data-table  { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th {
  padding: 8px 12px;
  color: #64748b;
  border-bottom: 1px solid #334155;
  text-align: left;
  background: #1e293b;
}
.data-table td {
  padding: 7px 12px;
  border-bottom: 1px solid #1e293b;
}
.data-table tr:nth-child(even) td { background: #1e293b; }
</style>
