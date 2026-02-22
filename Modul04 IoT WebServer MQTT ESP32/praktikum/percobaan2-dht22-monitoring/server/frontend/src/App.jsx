import React, { useState, useEffect, useCallback } from 'react'

// ─── Styles (inline to keep component self-contained) ─────────────────────────
const S = {
  page: {
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    background: '#0f172a',
    color: '#e2e8f0',
    minHeight: '100vh',
    padding: '24px',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '28px',
  },
  h1: { fontSize: '1.5rem', color: '#38bdf8', margin: 0 },
  badge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    background: '#1e293b',
    border: '1px solid #334155',
    borderRadius: '9999px',
    padding: '4px 14px',
    fontSize: '0.8rem',
    color: '#94a3b8',
  },
  dot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#22c55e',
  },
  // Big current-value cards
  bigCards: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
    marginBottom: '24px',
  },
  bigCard: (accent) => ({
    background: '#1e293b',
    border: `1px solid ${accent}44`,
    borderRadius: '16px',
    padding: '28px 24px',
    textAlign: 'center',
  }),
  bigValue: (accent) => ({
    fontSize: '3rem',
    fontWeight: '800',
    color: accent,
    lineHeight: 1.1,
  }),
  bigLabel: {
    fontSize: '0.85rem',
    color: '#94a3b8',
    marginTop: '8px',
    textTransform: 'uppercase',
    letterSpacing: '.06em',
  },
  bigUnit: { fontSize: '1.4rem', fontWeight: '400', marginLeft: '4px' },

  // Stats row
  statsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
    gap: '12px',
    marginBottom: '24px',
  },
  statCard: {
    background: '#1e293b',
    border: '1px solid #334155',
    borderRadius: '10px',
    padding: '14px 18px',
  },
  statLabel: { fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '.05em' },
  statValue: { fontSize: '1.4rem', fontWeight: '700', color: '#e2e8f0', marginTop: '4px' },

  // Table
  tableWrap: {
    background: '#1e293b',
    border: '1px solid #334155',
    borderRadius: '12px',
    overflow: 'hidden',
  },
  tableHead: {
    padding: '14px 20px',
    borderBottom: '1px solid #334155',
    color: '#cbd5e1',
    fontWeight: '600',
    fontSize: '0.95rem',
  },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' },
  th: {
    textAlign: 'left',
    padding: '10px 16px',
    background: '#0f172a',
    color: '#64748b',
    fontWeight: '600',
    textTransform: 'uppercase',
    fontSize: '0.72rem',
    letterSpacing: '.05em',
  },
  td: { padding: '9px 16px', color: '#cbd5e1', borderTop: '1px solid #1e3a5f22' },

  error: {
    background: '#7f1d1d',
    border: '1px solid #ef4444',
    borderRadius: '8px',
    padding: '12px 16px',
    marginBottom: '20px',
    color: '#fca5a5',
    fontSize: '0.875rem',
  },
  center: { textAlign: 'center', padding: '32px', color: '#64748b' },
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function fmt(v, decimals = 1) {
  if (v === null || v === undefined) return '–'
  return Number(v).toFixed(decimals)
}

function fmtDate(iso) {
  if (!iso) return '–'
  const d = new Date(iso)
  return isNaN(d) ? iso : d.toLocaleString('id-ID', { hour12: false })
}

// ─── App component ────────────────────────────────────────────────────────────
export default function App() {
  const [readings, setReadings] = useState([])
  const [stats, setStats]       = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      const [rReadings, rStats] = await Promise.all([
        fetch('/api/sensor?limit=20'),
        fetch('/api/sensor/stats'),
      ])

      if (!rReadings.ok) throw new Error(`Readings: HTTP ${rReadings.status}`)
      if (!rStats.ok)    throw new Error(`Stats: HTTP ${rStats.status}`)

      const [dataReadings, dataStats] = await Promise.all([
        rReadings.json(),
        rStats.json(),
      ])

      setReadings(dataReadings)
      setStats(dataStats)
      setError(null)
      setLastUpdate(new Date().toLocaleTimeString('id-ID'))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
    const id = setInterval(fetchData, 5000)
    return () => clearInterval(id)
  }, [fetchData])

  const latest = readings[0] ?? null

  return (
    <div style={S.page}>
      {/* ── Header ── */}
      <div style={S.header}>
        <h1 style={S.h1}>🌡️ DHT22 Monitor – Percobaan 2</h1>
        <div style={S.badge}>
          <span style={S.dot} />
          {lastUpdate ? `Update: ${lastUpdate}` : 'Connecting…'}
        </div>
      </div>

      {/* ── Error banner ── */}
      {error && <div style={S.error}>⚠️ {error}</div>}

      {/* ── Loading ── */}
      {loading && <div style={S.center}>Memuat data sensor…</div>}

      {/* ── Big current-value cards ── */}
      {!loading && (
        <div style={S.bigCards}>
          <div style={S.bigCard('#38bdf8')}>
            <div style={S.bigValue('#38bdf8')}>
              {fmt(latest?.temperature)}
              <span style={S.bigUnit}>°C</span>
            </div>
            <div style={S.bigLabel}>Suhu</div>
          </div>
          <div style={S.bigCard('#a78bfa')}>
            <div style={S.bigValue('#a78bfa')}>
              {fmt(latest?.humidity)}
              <span style={S.bigUnit}>%</span>
            </div>
            <div style={S.bigLabel}>Kelembaban</div>
          </div>
          <div style={S.bigCard('#fb923c')}>
            <div style={S.bigValue('#fb923c')}>
              {fmt(latest?.heat_index)}
              <span style={S.bigUnit}>°C</span>
            </div>
            <div style={S.bigLabel}>Heat Index</div>
          </div>
          <div style={S.bigCard('#4ade80')}>
            <div style={{ ...S.bigValue('#4ade80'), fontSize: '1.4rem' }}>
              {latest?.device ?? '–'}
            </div>
            <div style={S.bigLabel}>Device</div>
          </div>
        </div>
      )}

      {/* ── Stats row ── */}
      {!loading && stats && (
        <div style={S.statsRow}>
          {[
            { label: 'Temp Min',  value: `${fmt(stats.temperature?.min)}°C` },
            { label: 'Temp Max',  value: `${fmt(stats.temperature?.max)}°C` },
            { label: 'Temp Avg',  value: `${fmt(stats.temperature?.avg)}°C` },
            { label: 'Hum Min',   value: `${fmt(stats.humidity?.min)}%` },
            { label: 'Hum Max',   value: `${fmt(stats.humidity?.max)}%` },
            { label: 'Hum Avg',   value: `${fmt(stats.humidity?.avg)}%` },
            { label: 'Readings',  value: stats.count ?? '–' },
          ].map(({ label, value }) => (
            <div key={label} style={S.statCard}>
              <div style={S.statLabel}>{label}</div>
              <div style={S.statValue}>{value}</div>
            </div>
          ))}
        </div>
      )}

      {/* ── Table ── */}
      {!loading && (
        <div style={S.tableWrap}>
          <div style={S.tableHead}>📋 20 Pembacaan Terbaru</div>
          {readings.length === 0 ? (
            <div style={S.center}>Belum ada data. Tunggu pembacaan dari ESP32…</div>
          ) : (
            <table style={S.table}>
              <thead>
                <tr>
                  {['#', 'Device', 'Suhu (°C)', 'Kelembaban (%)', 'Heat Index (°C)', 'Waktu'].map(h => (
                    <th key={h} style={S.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {readings.map((row, idx) => (
                  <tr key={row.id}>
                    <td style={{ ...S.td, color: '#64748b' }}>{idx + 1}</td>
                    <td style={S.td}>
                      <span style={{
                        background: '#0c4a6e', color: '#38bdf8',
                        borderRadius: '6px', padding: '2px 8px',
                        fontSize: '0.78rem', fontWeight: 600,
                      }}>
                        {row.device}
                      </span>
                    </td>
                    <td style={{ ...S.td, color: '#38bdf8', fontWeight: 600 }}>
                      {fmt(row.temperature)}
                    </td>
                    <td style={{ ...S.td, color: '#a78bfa', fontWeight: 600 }}>
                      {fmt(row.humidity)}
                    </td>
                    <td style={{ ...S.td, color: '#fb923c' }}>
                      {fmt(row.heat_index)}
                    </td>
                    <td style={{ ...S.td, color: '#64748b', fontSize: '0.8rem' }}>
                      {fmtDate(row.recorded_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}
