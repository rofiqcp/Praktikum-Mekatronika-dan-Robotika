// Percobaan 5 – Frontend: SensorCard.jsx
// Menampilkan satu metrik sensor dalam bentuk kartu.

export default function SensorCard({ label, value, unit, color = '#3b82f6', icon = '📊' }) {
  const pct = typeof value === 'number' ? Math.min(100, Math.max(0, value)) : 0;

  return (
    <div style={{
      background: '#1e293b',
      border: `2px solid ${color}`,
      borderRadius: '12px',
      padding: '20px',
      minWidth: '160px',
      textAlign: 'center',
      boxShadow: `0 0 12px ${color}44`,
    }}>
      <div style={{ fontSize: '32px', marginBottom: '8px' }}>{icon}</div>
      <div style={{ color: '#94a3b8', fontSize: '13px', marginBottom: '4px' }}>{label}</div>
      <div style={{ color, fontSize: '36px', fontWeight: 700, lineHeight: 1 }}>
        {value !== null && value !== undefined ? value : '–'}
      </div>
      <div style={{ color: '#64748b', fontSize: '12px', marginTop: '4px' }}>{unit}</div>

      {/* Progress bar */}
      <div style={{ marginTop: '12px', background: '#334155', borderRadius: '4px', height: '6px' }}>
        <div style={{
          width: `${pct}%`,
          height: '100%',
          background: color,
          borderRadius: '4px',
          transition: 'width 0.5s ease',
        }} />
      </div>
    </div>
  );
}
