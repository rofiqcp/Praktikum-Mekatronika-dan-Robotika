# PERCOBAAN 01: BACA HOLDING REGISTER PLC VIA MODBUS RTU (PYTHON)

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Komunikasi Modbus RTU — Membaca Data dari PLC  
**Platform:** MiniPC Python + PLC TM221/CP2E via RS-485  
**Estimasi Waktu:** 60 menit

---

## A. TUJUAN

1. Memahami konsep Modbus RTU dan arsitektur master-slave
2. Mengkonfigurasi PLC sebagai Modbus RTU Slave
3. Membaca Holding Register dan Coil dari PLC menggunakan Python pymodbus
4. Memahami pemetaan memori PLC ke register Modbus

---

## B. ALAT DAN BAHAN

- PLC Schneider TM221CE24R atau Omron CP2E
- MiniPC/Laptop dengan Python 3.9+
- Modul konverter USB-RS485 (CH340/FT232)
- Kabel twisted pair (RS-485)
- Push button 24VDC (2 buah)
- Lampu indikator 24VDC (1 buah)
- Catu daya 24VDC

---

## C. KONFIGURASI PLC

### Schneider TM221 – EcoStruxure Machine Expert Basic (EMEB)

**Konfigurasi Serial Modbus RTU Slave:**
```
Menu: TM221CE24R → Configuration → Serial Line → SL1
  Protocol:     Modbus Slave
  Slave ID:     1
  Baud Rate:    9600
  Data Bits:    8
  Parity:       None
  Stop Bits:    1
```

**Program Ladder (PLC TM221):**
```
Rung 1: Latch motor dari tombol START/STOP
|  %I0.0  |   %I0.1  |   %Q0.0  |
+--[ ]----+--[/]-----+----( )---+
  START      STOP       MOTOR

|  %Q0.0  |             |  %Q0.0  |
+--[ ]----+----( )-----+
  MOTOR_LATCH

Rung 2: Salin Analog Input ke %MW0
LD  P_On
MOV %IW0.0, %MW0       ; AI0 → MW0

Rung 3: Counter auto-increment setiap siklus scan
LD   P_On
INC  %MW1              ; MW1 = MW1 + 1
```

**Pemetaan Register (TM221):**
| Register Modbus | Alamat | Objek PLC | Keterangan |
|----------------|--------|-----------|-----------|
| Holding Reg 0 | 0 | %MW0 | Nilai AI0 (0–4095) |
| Holding Reg 1 | 1 | %MW1 | Counter scan |
| Holding Reg 2 | 2 | %MW2 | Nilai setpoint (diisi dari luar) |
| Coil 2048 | 2048 | %Q0.0 | Output relay 0 (MOTOR) |
| Coil 2049 | 2049 | %Q0.1 | Output relay 1 (LAMP) |
| Discrete Input 0 | 0 | %I0.0 | Input digital 0 (START) |
| Discrete Input 1 | 1 | %I0.1 | Input digital 1 (STOP) |

### Omron CP2E – CX-Programmer

**Konfigurasi Serial Modbus RTU Slave:**
```
PLC Properties → Built-in I/O Settings → Serial Port:
  Protocol:  Modbus RTU Slave
  Node No:   1
  Baud Rate: 9600
  Data:      8-N-1
```

**Program Ladder (CP2E):**
```
Rung 1: Latch output
LD   000.00          ; DI0
OR   100.00          ; Output self-hold
AND NOT 000.01       ; DI1 (STOP)
OUT  100.00          ; DO0

Rung 2: Copy AI ke DM
LD   P_On
MOVD AIW000, DM0000  ; AI0 → DM0
```

**Pemetaan Register (CP2E):**
| Register Modbus | Alamat | Objek CP2E |
|----------------|--------|-----------|
| Holding Reg 0 | 0 | DM0000 |
| Holding Reg 1 | 1 | DM0001 |
| Coil 0 | 0 | CIO 000.00 |
| Coil 100 | 100 | CIO 006.04 |

---

## D. PROGRAM MINIPC PYTHON

**File: `percobaan01_baca_register.py`**

```python
#!/usr/bin/env python3
"""
Percobaan 01: Membaca Holding Register dan Coil dari PLC
via Modbus RTU menggunakan Python pymodbus
"""

from pymodbus.client import ModbusSerialClient
import time

# ============================================================
# KONFIGURASI – Sesuaikan dengan setup lab Anda
# ============================================================
PORT      = "/dev/ttyUSB0"  # Linux; Windows: "COM3", "COM4", dll.
BAUDRATE  = 9600
PARITY    = 'N'             # N=None, E=Even, O=Odd
STOPBITS  = 1
BYTESIZE  = 8
TIMEOUT   = 2
SLAVE_ID  = 1
INTERVAL  = 1.0             # detik antar pembacaan
# ============================================================

def buat_client():
    return ModbusSerialClient(
        port=PORT,
        baudrate=BAUDRATE,
        parity=PARITY,
        stopbits=STOPBITS,
        bytesize=BYTESIZE,
        timeout=TIMEOUT
    )

def baca_holding_registers(client, alamat=0, jumlah=10):
    """Baca Holding Register dari PLC (FC03)"""
    result = client.read_holding_registers(
        address=alamat,
        count=jumlah,
        slave=SLAVE_ID
    )
    if result.isError():
        print(f"[ERROR] Baca HR alamat {alamat}: {result}")
        return None
    return result.registers

def baca_coils(client, alamat=2048, jumlah=4):
    """Baca status Coil/Output dari PLC (FC01)"""
    result = client.read_coils(
        address=alamat,
        count=jumlah,
        slave=SLAVE_ID
    )
    if result.isError():
        print(f"[ERROR] Baca Coil alamat {alamat}: {result}")
        return None
    return result.bits[:jumlah]

def baca_discrete_inputs(client, alamat=0, jumlah=4):
    """Baca status Discrete Input dari PLC (FC02)"""
    result = client.read_discrete_inputs(
        address=alamat,
        count=jumlah,
        slave=SLAVE_ID
    )
    if result.isError():
        print(f"[ERROR] Baca DI alamat {alamat}: {result}")
        return None
    return result.bits[:jumlah]

def main():
    client = buat_client()
    print(f"Menghubungkan ke PLC via {PORT}...")
    
    if not client.connect():
        print(f"[GAGAL] Tidak dapat terhubung ke {PORT}")
        print("Pastikan:")
        print("  1. USB-RS485 terpasang dan terdeteksi sistem")
        print("  2. Kabel RS-485 terhubung dengan benar (A+, B-, GND)")
        print("  3. PLC dalam mode RUN dan Modbus Slave aktif")
        print(f"  4. Port yang benar: ls /dev/ttyUSB* (Linux) atau Device Manager (Windows)")
        return
    
    print(f"[OK] Terhubung ke PLC (Slave ID: {SLAVE_ID}, {BAUDRATE}-8-N-1)")
    print("-" * 60)
    
    iterasi = 0
    try:
        while True:
            iterasi += 1
            print(f"\n--- Iterasi {iterasi} ---")
            
            # 1. Baca Holding Register (MW0 – MW9)
            regs = baca_holding_registers(client, alamat=0, jumlah=10)
            if regs:
                print(f"Holding Register (MW0-MW9):")
                for i, val in enumerate(regs):
                    print(f"  MW{i} = {val} (0x{val:04X})")
            
            # 2. Baca Coil (Q0.0 – Q0.3)
            coils = baca_coils(client, alamat=2048, jumlah=4)
            if coils is not None:
                print(f"Output (Q0.0-Q0.3): {['ON' if c else 'OFF' for c in coils]}")
            
            # 3. Baca Discrete Input (I0.0 – I0.3)
            inputs = baca_discrete_inputs(client, alamat=0, jumlah=4)
            if inputs is not None:
                print(f"Input (I0.0-I0.3):  {['ON' if i else 'OFF' for i in inputs]}")
            
            time.sleep(INTERVAL)
    
    except KeyboardInterrupt:
        print("\n[INFO] Program dihentikan oleh pengguna (Ctrl+C)")
    finally:
        client.close()
        print("[INFO] Koneksi Modbus ditutup")

if __name__ == "__main__":
    main()
```

---

## E. LANGKAH PERCOBAAN

1. Rangkai hardware: PLC → RS-485 → USB-RS485 → MiniPC
2. Download program PLC dan verifikasi PLC dalam mode RUN
3. Pasang USB-RS485 ke MiniPC, identifikasi port: `ls /dev/ttyUSB*`
4. Jalankan script: `python percobaan01_baca_register.py`
5. Amati output terminal — nilai register harus berubah (MW1 counter naik)
6. Tekan tombol START (I0.0) — amati perubahan Discrete Input
7. Catat minimal 5 pembacaan pada tabel pengamatan

---

## F. TABEL PENGAMATAN

| Iterasi | MW0 (AI) | MW1 (Counter) | MW2 | Q0.0 | Q0.1 | I0.0 | I0.1 |
|---------|---------|--------------|-----|------|------|------|------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

**Error yang ditemukan:** _______________________________________________

---

## G. PERTANYAAN ANALISIS

1. Mengapa nilai MW1 (counter) terus bertambah secara otomatis? Register mana yang bersesuaian di PLC?

2. Apa perbedaan antara Discrete Input (FC02) dan Coil (FC01) pada Modbus? Mengapa input dan output PLC menggunakan alamat berbeda?

3. Jika nilai AI0 PLC adalah 2048 (nilai tengah ADC 12-bit), berapa tegangan input analog yang diukur? (Asumsi range AI 0–10V)

---

## H. REFERENSI

- pymodbus: https://pymodbus.readthedocs.io
- Schneider TM221 Modbus Guide: https://www.se.com
- Omron CP2E Serial Manual: https://www.ia.omron.com
