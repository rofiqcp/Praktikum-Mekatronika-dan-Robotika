<template>
  <!-- Percobaan 6 – Komponen Gauge Metrik -->
  <div class="gauge-card" :style="{ borderColor: thresholdColor }">
    <div class="gauge-icon">{{ icon }}</div>
    <div class="gauge-label">{{ label }}</div>

    <!-- Bar gauge -->
    <div class="gauge-bar-track">
      <div
        class="gauge-bar-fill"
        :style="{ width: barPct + '%', background: thresholdColor }"
      />
    </div>

    <div class="gauge-value" :style="{ color: thresholdColor }">
      {{ displayValue }}<span class="gauge-unit">{{ unit }}</span>
    </div>

    <div class="gauge-range">{{ min }} – {{ max }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  label:     { type: String,  required: true },
  value:     { type: Number,  default: null  },
  unit:      { type: String,  default: ''    },
  min:       { type: Number,  default: 0     },
  max:       { type: Number,  default: 100   },
  icon:      { type: String,  default: '📊'  },
  warnAt:    { type: Number,  default: null  },  // kuning jika >= warnAt
  dangerAt:  { type: Number,  default: null  },  // merah jika >= dangerAt
  decimals:  { type: Number,  default: 1     },
});

const barPct = computed(() => {
  if (props.value === null || props.value === undefined) return 0;
  const clamped = Math.min(props.max, Math.max(props.min, props.value));
  return ((clamped - props.min) / (props.max - props.min)) * 100;
});

const thresholdColor = computed(() => {
  const v = props.value;
  if (v === null || v === undefined) return '#475569';
  if (props.dangerAt !== null && v >= props.dangerAt) return '#ef4444';
  if (props.warnAt   !== null && v >= props.warnAt)   return '#f59e0b';
  return '#22d3ee';
});

const displayValue = computed(() => {
  if (props.value === null || props.value === undefined) return '–';
  return Number(props.value).toFixed(props.decimals);
});
</script>

<style scoped>
.gauge-card {
  background: #1e293b;
  border: 2px solid #475569;
  border-radius: 12px;
  padding: 16px 20px;
  min-width: 150px;
  text-align: center;
  transition: border-color 0.3s;
}
.gauge-icon  { font-size: 28px; margin-bottom: 6px; }
.gauge-label { color: #94a3b8; font-size: 12px; margin-bottom: 8px; }
.gauge-bar-track {
  background: #334155;
  border-radius: 4px;
  height: 6px;
  margin-bottom: 10px;
  overflow: hidden;
}
.gauge-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease, background 0.3s;
}
.gauge-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  transition: color 0.3s;
}
.gauge-unit  { font-size: 14px; margin-left: 4px; font-weight: 400; }
.gauge-range { color: #475569; font-size: 11px; margin-top: 6px; }
</style>
