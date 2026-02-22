// Percobaan 5 – Frontend: App.jsx
// Dashboard utama: polling sensor data + kontrol brightness LED.

import { useState, useEffect, useCallback } from 'react';
import SensorCard from './SensorCard';
import SensorTable from './SensorTable';

const POLL_INTERVAL_MS = 4000;

export default function App() {
  const [readings, setReadings]         = useState([]);
  const [latest, setLatest]             = useState(null);
  const [brightness, setBrightness]     = useState(0);
  const [ledStatus, setLedStatus]       = useState('');
  const [lastUpdated, setLastUpdated]   = useState(null);
  const [error, setError]               = useState('');

  // ── Fetch data sensor terbaru ────────────────────────────────────────────
  const fetchData = useCallback(async () => {
    try {
      const res  = await fetch('/api/sensors?limit=20');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setReadings(data);
      if (data.length > 0) setLatest(data[0]);
      setLastUpdated(new Date());
      setError('');
    } catch (e) {
      setError(`Gagal mengambil data: ${e.message}`);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [fetchData]);

  // ── Kirim perintah brightness LED ────────────────────────────────────────
  const sendBrightness = async () => {
    try {
      const res = await fetch('/api/led/brightness', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ brightness }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setLedStatus(`✓ Brightness dikirim: ${brightness}`);
      setTimeout(() => setLedStatus(''), 3000);
    } catch (e) {
      setLedStatus(`✗ Gagal: ${e.message}`);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0f172a',
      color: '#e2e8f0',
      fontFamily: 'system-ui, sans-serif',
      padding: '24px',
    }}>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '24px', color: '#38bdf8' }}>
          🌐 MQTT-HTTP Bridge Dashboard
        </h1>
        <p style={{ margin: '4px 0 0', color: '#64748b', fontSize: '13px' }}>
          Percobaan 5 – C# ASP.NET Core + React
          {lastUpdated && ` · Diperbarui: ${lastUpdated.toLocaleTimeString('id-ID')}`}
        </p>
      </div>

      {/* Error banner */}
      {error && (
        <div style={{
          background: '#7f1d1d', border: '1px solid #dc2626',
          borderRadius: '8px', padding: '10px 16px', marginBottom: '20px', fontSize: '13px',
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* Kartu sensor */}
      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', marginBottom: '28px' }}>
        <SensorCard
          label="Intensitas Cahaya"
          value={latest?.lightPct ?? '–'}
          unit="%"
          color="#f59e0b"
          icon="☀️"
        />
        <SensorCard
          label="Potensiometer"
          value={latest?.potPct ?? '–'}
          unit="%"
          color="#8b5cf6"
          icon="🎛️"
        />
        <SensorCard
          label="Light Raw (ADC)"
          value={latest?.lightRaw ?? '–'}
          unit="/ 4095"
          color="#22d3ee"
          icon="📡"
        />
        <SensorCard
          label="Uptime ESP32"
          value={latest?.uptime ?? '–'}
          unit="detik"
          color="#34d399"
          icon="⏱️"
        />
      </div>

      {/* Kontrol LED Brightness */}
      <div style={{
        background: '#1e293b',
        border: '1px solid #334155',
        borderRadius: '12px',
        padding: '20px',
        marginBottom: '28px',
        maxWidth: '480px',
      }}>
        <h2 style={{ margin: '0 0 16px', fontSize: '16px', color: '#38bdf8' }}>
          💡 Kontrol Brightness LED (GPIO2)
        </h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <input
            type="range"
            min={0}
            max={255}
            value={brightness}
            onChange={e => setBrightness(Number(e.target.value))}
            style={{ flex: 1, accentColor: '#f59e0b' }}
          />
          <span style={{ width: '36px', textAlign: 'right', fontWeight: 700 }}>
            {brightness}
          </span>
        </div>
        <button
          onClick={sendBrightness}
          style={{
            marginTop: '12px',
            padding: '8px 20px',
            background: '#f59e0b',
            color: '#0f172a',
            border: 'none',
            borderRadius: '6px',
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          Kirim ke ESP32
        </button>
        {ledStatus && (
          <p style={{ marginTop: '8px', fontSize: '13px', color: '#86efac' }}>{ledStatus}</p>
        )}
      </div>

      {/* Tabel data */}
      <div style={{
        background: '#1e293b',
        border: '1px solid #334155',
        borderRadius: '12px',
        padding: '20px',
      }}>
        <h2 style={{ margin: '0 0 12px', fontSize: '16px', color: '#38bdf8' }}>
          📋 20 Pembacaan Terakhir
        </h2>
        <SensorTable readings={readings} />
      </div>
    </div>
  );
}
