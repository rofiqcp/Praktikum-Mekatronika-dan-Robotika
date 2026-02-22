<template>
  <!-- Percobaan 6 – Daftar Alert Real-Time -->
  <div class="alert-list">
    <div v-if="alerts.length === 0" class="empty">
      Tidak ada alert saat ini.
    </div>
    <transition-group name="fade" tag="ul" class="list">
      <li
        v-for="(alert, i) in alerts"
        :key="alert.timestamp + i"
        class="alert-item"
        :class="severityClass(alert)"
      >
        <span class="alert-icon">{{ alertIcon(alert) }}</span>
        <div class="alert-body">
          <div class="alert-title">{{ alertTitle(alert) }}</div>
          <div class="alert-meta">
            {{ alert.device }} ·
            {{ formatTime(alert.timestamp) }}
          </div>
          <div v-if="alert.anomalies" class="alert-detail">
            <span
              v-for="a in alert.anomalies"
              :key="a.field"
              class="anomaly-tag"
            >
              {{ a.field }}: {{ a.value }} (z={{ a.z_score }})
            </span>
          </div>
        </div>
      </li>
    </transition-group>
  </div>
</template>

<script setup>
defineProps({
  alerts: { type: Array, default: () => [] },
});

function severityClass(alert) {
  if (alert.alert === 'anomaly_detected') return 'severity-warning';
  if (alert.alert === 'motion_detected')  return 'severity-info';
  return 'severity-default';
}

function alertIcon(alert) {
  if (alert.alert === 'anomaly_detected') return '⚠️';
  if (alert.alert === 'motion_detected')  return '🚶';
  return '🔔';
}

function alertTitle(alert) {
  const map = {
    anomaly_detected: 'Anomali Terdeteksi',
    motion_detected:  'Gerakan Terdeteksi',
  };
  return map[alert.alert] ?? alert.alert ?? 'Alert';
}

function formatTime(ts) {
  if (!ts) return '';
  return new Date(ts).toLocaleTimeString('id-ID');
}
</script>

<style scoped>
.alert-list { max-height: 320px; overflow-y: auto; }
.empty      { color: #64748b; text-align: center; padding: 20px; font-size: 13px; }
.list       { list-style: none; margin: 0; padding: 0; }

.alert-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 6px;
  font-size: 13px;
}

.severity-warning { background: #422006; border-left: 3px solid #f59e0b; }
.severity-info    { background: #0c1a2e; border-left: 3px solid #3b82f6; }
.severity-default { background: #1e293b; border-left: 3px solid #475569; }

.alert-icon  { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
.alert-title { font-weight: 600; color: #e2e8f0; }
.alert-meta  { color: #64748b; font-size: 11px; margin-top: 2px; }
.alert-detail{ margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px; }
.anomaly-tag {
  background: #1e293b;
  border: 1px solid #475569;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 11px;
  color: #94a3b8;
}

.fade-enter-active { transition: all 0.3s ease; }
.fade-enter-from   { opacity: 0; transform: translateY(-8px); }
</style>
