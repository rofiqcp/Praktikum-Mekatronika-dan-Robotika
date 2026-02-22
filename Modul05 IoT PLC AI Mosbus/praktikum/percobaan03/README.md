# PERCOBAAN 03: KOMUNIKASI MODBUS TCP – MINIPC PYTHON

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Modbus TCP — Baca dan Tulis Register PLC via Ethernet  
**Platform:** MiniPC Python + PLC TM221/CP2E via Ethernet  
**Estimasi Waktu:** 60 menit

---

## A. TUJUAN

1. Memahami perbedaan Modbus RTU dan Modbus TCP pada level implementasi
2. Mengkonfigurasi PLC dengan IP address statis untuk Modbus TCP
3. Membaca dan menulis register PLC melalui Ethernet/WiFi menggunakan pymodbus TCP
4. Mengukur dan membandingkan waktu respons Modbus RTU vs TCP

---

## B. KONFIGURASI JARINGAN

```
MiniPC (192.168.1.20) ──┐
                         ├── Switch/Router ── PLC TM221 (192.168.1.10)
ESP32  (192.168.1.30) ──┘                   PLC CP2E  (192.168.1.11)
```

### Schneider TM221 – Konfigurasi Ethernet

```
EMEB → TM221CE24R → Configuration → Ethernet:
  IP Mode:      Fixed
  IP Address:   192.168.1.10
  Subnet:       255.255.255.0
  Gateway:      192.168.1.1
  Modbus TCP:   Port 502 (aktif otomatis)
```

### Omron CP2E-E – Konfigurasi Ethernet

```
CX-Programmer → IO Table → Built-in Ethernet → TCP/IP Settings:
  IP Address:   192.168.1.11
  Subnet:       255.255.255.0
  Modbus TCP Port: 502 (default, selalu aktif)
```

---

## C. PROGRAM MINIPC PYTHON

**File: `percobaan03_modbus_tcp.py`**

```python
#!/usr/bin/env python3
"""
Percobaan 03: Komunikasi Modbus TCP dengan PLC
Baca dan tulis register melalui Ethernet
"""

from pymodbus.client import ModbusTcpClient
import time

PLC_IP   = "192.168.1.10"   # Ganti sesuai IP PLC di lab
PLC_PORT = 502
SLAVE_ID = 1

client = ModbusTcpClient(host=PLC_IP, port=PLC_PORT, timeout=3)


def cek_koneksi():
    """Verifikasi konektivitas jaringan"""
    import subprocess
    result = subprocess.run(
        ['ping', '-c', '3', PLC_IP],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"[OK] Ping ke {PLC_IP} berhasil")
    else:
        print(f"[WARN] Ping ke {PLC_IP} gagal. Cek koneksi jaringan")
    return result.returncode == 0


def baca_register_tcp():
    """Baca holding register via Modbus TCP"""
    t_start = time.perf_counter()
    rr = client.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
    t_elapsed = (time.perf_counter() - t_start) * 1000  # ms
    
    if not rr.isError():
        return rr.registers, t_elapsed
    return None, t_elapsed


def tulis_register_tcp(alamat, nilai):
    """Tulis holding register via Modbus TCP"""
    t_start = time.perf_counter()
    wr = client.write_register(address=alamat, value=nilai, slave=SLAVE_ID)
    t_elapsed = (time.perf_counter() - t_start) * 1000
    return not wr.isError(), t_elapsed


def benchmark_vs_rtu():
    """
    Ukur waktu rata-rata 20 pembacaan TCP
    Bandingkan dengan RTU jika tersedia
    """
    print("\n=== BENCHMARK MODBUS TCP ===")
    times = []
    N = 20
    for i in range(N):
        _, t = baca_register_tcp()
        times.append(t)
        time.sleep(0.1)
    
    avg = sum(times) / len(times)
    mn  = min(times)
    mx  = max(times)
    print(f"Hasil ({N}x pembacaan 10 register via TCP):")
    print(f"  Rata-rata: {avg:.2f} ms")
    print(f"  Min:       {mn:.2f} ms")
    print(f"  Max:       {mx:.2f} ms")
    print("\nCatatan: RTU biasanya 10–30 ms lebih rendah dari TCP")


def main():
    print("=== PERCOBAAN 03: MODBUS TCP ===")
    cek_koneksi()
    
    if not client.connect():
        print(f"[GAGAL] Tidak dapat koneksi Modbus TCP ke {PLC_IP}:{PLC_PORT}")
        print("Pastikan:")
        print("  1. IP PLC sudah sesuai dan dikonfigurasi static")
        print("  2. MiniPC dalam satu subnet dengan PLC")
        print("  3. Tidak ada firewall yang memblokir port 502")
        return
    
    print(f"[OK] Modbus TCP terhubung ke {PLC_IP}:{PLC_PORT}")
    
    # Demo baca/tulis
    print("\n=== BACA REGISTER ===")
    for i in range(5):
        regs, t = baca_register_tcp()
        if regs:
            print(f"[{i+1}] MW0-4={regs[:5]} | waktu={t:.2f}ms")
        time.sleep(1)
    
    print("\n=== TULIS REGISTER ===")
    for val in [100, 500, 999, 0]:
        ok, t = tulis_register_tcp(alamat=2, nilai=val)
        print(f"Tulis MW2={val}: {'OK' if ok else 'ERROR'} ({t:.2f}ms)")
        time.sleep(0.5)
    
    # Kontrol output via TCP
    print("\n=== KONTROL OUTPUT (COIL) VIA TCP ===")
    client.write_coil(address=2048, value=True, slave=SLAVE_ID)
    print("Q0.0 ON via TCP")
    time.sleep(2)
    client.write_coil(address=2048, value=False, slave=SLAVE_ID)
    print("Q0.0 OFF via TCP")
    
    benchmark_vs_rtu()
    
    client.close()
    print("\n[SELESAI] Percobaan 03 selesai")


if __name__ == "__main__":
    main()
```

---

## D. TABEL PENGAMATAN

### D.1 Konfigurasi Jaringan

| Parameter | Nilai |
|-----------|-------|
| IP PLC | |
| IP MiniPC | |
| Subnet Mask | |
| Port Modbus TCP | 502 |
| Ping ke PLC (ms) | |

### D.2 Perbandingan RTU vs TCP

| Metrik | Modbus RTU | Modbus TCP | Selisih |
|--------|-----------|-----------|---------|
| Waktu respons rata-rata (ms) | | | |
| Waktu respons minimum (ms) | | | |
| Waktu respons maksimum (ms) | | | |
| Error rate (%) | | | |

---

## E. PERTANYAAN ANALISIS

1. Mengapa Modbus TCP umumnya memiliki latensi lebih tinggi dari RTU meski kecepatan fisik Ethernet (100 Mbps) jauh lebih tinggi dari RS-485 (9600 bps)?

2. Sebutkan skenario industri di mana Modbus TCP lebih sesuai digunakan dibanding Modbus RTU.

3. Apa risiko keamanan dari Modbus TCP yang tidak ada pada Modbus RTU? Bagaimana mitigasinya?

---

## F. REFERENSI

- Modbus TCP Specification: https://modbus.org/docs/Modbus_Messaging_on_TCP-IP_Implementation_Guide_V1_0b.pdf
- pymodbus ModbusTcpClient: https://pymodbus.readthedocs.io
