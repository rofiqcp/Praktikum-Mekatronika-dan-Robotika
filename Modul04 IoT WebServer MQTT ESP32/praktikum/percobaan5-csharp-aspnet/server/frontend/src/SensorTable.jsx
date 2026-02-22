// Percobaan 5 – Frontend: SensorTable.jsx
// Menampilkan tabel pembacaan sensor terbaru.

export default function SensorTable({ readings }) {
  if (!readings || readings.length === 0) {
    return (
      <div style={{ color: '#64748b', textAlign: 'center', padding: '24px' }}>
        Belum ada data sensor.
      </div>
    );
  }

  const cols = [
    { key: 'receivedAt', label: 'Waktu',        fmt: v => new Date(v).toLocaleTimeString('id-ID') },
    { key: 'device',     label: 'Device',        fmt: v => v },
    { key: 'lightRaw',   label: 'Light Raw',     fmt: v => v },
    { key: 'lightPct',   label: 'Cahaya (%)',    fmt: v => `${v}%` },
    { key: 'potRaw',     label: 'Pot Raw',       fmt: v => v },
    { key: 'potPct',     label: 'Pot (%)',       fmt: v => `${v}%` },
    { key: 'uptime',     label: 'Uptime (s)',    fmt: v => v },
  ];

  return (
    <div style={{ overflowX: 'auto', marginTop: '8px' }}>
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: '13px',
        color: '#e2e8f0',
      }}>
        <thead>
          <tr style={{ background: '#1e293b' }}>
            {cols.map(c => (
              <th key={c.key} style={{
                padding: '10px 14px',
                textAlign: 'left',
                color: '#94a3b8',
                borderBottom: '1px solid #334155',
                whiteSpace: 'nowrap',
              }}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {readings.map((row, i) => (
            <tr key={row.id ?? i} style={{
              background: i % 2 === 0 ? '#0f172a' : '#1e293b',
            }}>
              {cols.map(c => (
                <td key={c.key} style={{ padding: '8px 14px', borderBottom: '1px solid #1e293b' }}>
                  {c.fmt(row[c.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
