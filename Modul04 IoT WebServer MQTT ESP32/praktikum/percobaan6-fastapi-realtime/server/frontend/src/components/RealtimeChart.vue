<template>
  <!-- Percobaan 6 – Grafik Garis SVG Real-Time untuk suhu -->
  <div class="chart-wrapper">
    <div class="chart-title">{{ title }}</div>
    <svg
      :viewBox="`0 0 ${W} ${H}`"
      class="chart-svg"
      preserveAspectRatio="none"
    >
      <!-- Grid lines -->
      <line
        v-for="y in gridYPositions"
        :key="y"
        :x1="PAD" :y1="y" :x2="W - PAD" :y2="y"
        stroke="#1e293b" stroke-width="1"
      />

      <!-- Polyline -->
      <polyline
        v-if="points.length >= 2"
        :points="pointsStr"
        fill="none"
        :stroke="color"
        stroke-width="2"
        stroke-linejoin="round"
        stroke-linecap="round"
      />

      <!-- Area fill -->
      <polygon
        v-if="points.length >= 2"
        :points="areaPointsStr"
        :fill="color + '22'"
      />

      <!-- Dots -->
      <circle
        v-for="(p, i) in points"
        :key="i"
        :cx="p.x" :cy="p.y"
        r="3"
        :fill="color"
      />

      <!-- Y-axis labels -->
      <text
        v-for="(label, i) in yLabels"
        :key="'yl' + i"
        :x="PAD - 4"
        :y="gridYPositions[i] + 4"
        text-anchor="end"
        font-size="10"
        fill="#64748b"
      >{{ label }}</text>

      <!-- X-axis labels (first + last) -->
      <text
        v-if="data.length > 0"
        :x="PAD"
        :y="H - 2"
        font-size="9"
        fill="#475569"
      >{{ formatTime(data[0]?.t) }}</text>
      <text
        v-if="data.length > 1"
        :x="W - PAD"
        :y="H - 2"
        font-size="9"
        fill="#475569"
        text-anchor="end"
      >{{ formatTime(data[data.length - 1]?.t) }}</text>
    </svg>

    <div class="chart-legend">
      <span :style="{ color }">●</span> {{ unit }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  data:    { type: Array,  default: () => [] },  // [{ t: ISO string, v: number }]
  title:   { type: String, default: 'Grafik'  },
  unit:    { type: String, default: ''        },
  color:   { type: String, default: '#22d3ee' },
  minVal:  { type: Number, default: null      },
  maxVal:  { type: Number, default: null      },
});

const W   = 400;
const H   = 120;
const PAD = 36;

const chartMin = computed(() => {
  if (props.minVal !== null) return props.minVal;
  const vals = props.data.map(d => d.v).filter(v => v != null);
  return vals.length ? Math.min(...vals) - 2 : 0;
});

const chartMax = computed(() => {
  if (props.maxVal !== null) return props.maxVal;
  const vals = props.data.map(d => d.v).filter(v => v != null);
  return vals.length ? Math.max(...vals) + 2 : 100;
});

function toX(i) {
  const n = props.data.length;
  if (n <= 1) return PAD;
  return PAD + (i / (n - 1)) * (W - PAD * 2);
}

function toY(v) {
  const range = chartMax.value - chartMin.value || 1;
  return H - PAD / 2 - ((v - chartMin.value) / range) * (H - PAD);
}

const points = computed(() =>
  props.data
    .filter(d => d.v != null)
    .map((d, i) => ({ x: toX(i), y: toY(d.v) }))
);

const pointsStr = computed(() =>
  points.value.map(p => `${p.x},${p.y}`).join(' ')
);

const areaPointsStr = computed(() => {
  if (points.value.length < 2) return '';
  const bottom = H - PAD / 2;
  const first  = points.value[0];
  const last   = points.value[points.value.length - 1];
  return `${first.x},${bottom} ` + pointsStr.value + ` ${last.x},${bottom}`;
});

const GRID_LINES = 4;
const gridYPositions = computed(() => {
  const arr = [];
  for (let i = 0; i <= GRID_LINES; i++) {
    arr.push(PAD / 2 + (i / GRID_LINES) * (H - PAD));
  }
  return arr;
});

const yLabels = computed(() =>
  gridYPositions.value.map(y => {
    const range = chartMax.value - chartMin.value || 1;
    const v = chartMax.value - ((y - PAD / 2) / (H - PAD)) * range;
    return v.toFixed(1);
  })
);

function formatTime(ts) {
  if (!ts) return '';
  return new Date(ts).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}
</script>

<style scoped>
.chart-wrapper {
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 10px;
  padding: 12px;
}
.chart-title  { color: #94a3b8; font-size: 13px; margin-bottom: 8px; }
.chart-svg    { width: 100%; height: 120px; display: block; }
.chart-legend { color: #64748b; font-size: 11px; margin-top: 4px; text-align: right; }
</style>
