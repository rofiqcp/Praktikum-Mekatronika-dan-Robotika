# PERCOBAAN 02: TULIS HOLDING REGISTER DAN COIL PLC VIA MODBUS RTU (PYTHON)

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Komunikasi Modbus RTU — Menulis Data ke PLC  
**Platform:** MiniPC Python + PLC TM221/CP2E via RS-485  
**Estimasi Waktu:** 60 menit

---

## A. TUJUAN

1. Menulis nilai ke Holding Register PLC melalui Modbus RTU (FC06 & FC16)
2. Mengontrol output (Coil) PLC dari Python (FC05 & FC15)
3. Memahami konsep setpoint remote: Python sebagai HMI virtual
4. Memvalidasi data yang ditulis dengan membacanya kembali

---

## B. KONFIGURASI PLC

### Schneider TM221 – Program Ladder

```
Rung 1: Motor ON/OFF berdasarkan nilai MW2
|  P_On  |                      | Compare %MW2 >= 1 | | %Q0.0 |
+--[ ]---+---[GE %MW2, #0001]---+----( )------------+
                                   MOTOR berdasarkan MW2

Rung 2: Lampu berdasarkan setpoint MW3
|  P_On  |                      | Compare %MW3 >= 100 | | %Q0.1 |
+--[ ]---+---[GE %MW3, #0064]---+----( )-------------+
                                   LAMP jika MW3 >= 100

Rung 3: Copy nilai setpoint ke output analog (jika tersedia)
LD  P_On
MOV %MW4, %QW0.0       ; MW4 → Analog Output 0
```

**Pemetaan yang dipakai:**
- MW2 = kontrol motor (0=OFF, 1=ON), dapat ditulis dari luar
- MW3 = setpoint nilai (0–1000), dapat ditulis dari luar
- MW4 = setpoint analog output (0–4095)
- Q0.0 = motor ON/OFF (dapat dikontrol via coil atau MW2)

---

## C. PROGRAM MINIPC PYTHON

**File: `percobaan02_tulis_register.py`**

```python
#!/usr/bin/env python3
"""
Percobaan 02: Menulis Holding Register dan Coil ke PLC
via Modbus RTU menggunakan Python pymodbus
"""

from pymodbus.client import ModbusSerialClient
import time

PORT     = "/dev/ttyUSB0"
BAUDRATE = 9600
SLAVE_ID = 1

client = ModbusSerialClient(
    port=PORT, baudrate=BAUDRATE,
    parity='N', stopbits=1, bytesize=8, timeout=2
)


def verifikasi_tulis(nama, alamat, nilai_ditulis):
    """Tulis register lalu baca kembali untuk verifikasi"""
    rr = client.read_holding_registers(address=alamat, count=1, slave=SLAVE_ID)
    if not rr.isError():
        nilai_baca = rr.registers[0]
        status = "OK" if nilai_baca == nilai_ditulis else "MISMATCH"
        print(f"  Verifikasi {nama}[{alamat}]: tulis={nilai_ditulis}, baca={nilai_baca} [{status}]")
        return nilai_baca == nilai_ditulis
    return False


def demo_tulis_single_register():
    """Demo FC06: Write Single Register"""
    print("\n=== FC06: Write Single Holding Register ===")
    
    # Tulis MW2 = 1 (aktifkan motor)
    wr = client.write_register(address=2, value=1, slave=SLAVE_ID)
    print(f"Tulis MW2=1 (Motor ON): {wr}")
    time.sleep(0.5)
    verifikasi_tulis("MW2", 2, 1)
    time.sleep(2)
    
    # Tulis MW3 = 500 (setpoint)
    wr = client.write_register(address=3, value=500, slave=SLAVE_ID)
    print(f"Tulis MW3=500 (Setpoint): {wr}")
    verifikasi_tulis("MW3", 3, 500)
    time.sleep(1)
    
    # Tulis MW2 = 0 (matikan motor)
    wr = client.write_register(address=2, value=0, slave=SLAVE_ID)
    print(f"Tulis MW2=0 (Motor OFF): {wr}")
    verifikasi_tulis("MW2", 2, 0)


def demo_tulis_multiple_registers():
    """Demo FC16: Write Multiple Registers"""
    print("\n=== FC16: Write Multiple Holding Registers ===")
    
    # Tulis MW5=100, MW6=200, MW7=300 sekaligus
    nilai = [100, 200, 300]
    wr = client.write_registers(address=5, values=nilai, slave=SLAVE_ID)
    print(f"Tulis MW5-MW7 = {nilai}: {wr}")
    
    # Verifikasi
    rr = client.read_holding_registers(address=5, count=3, slave=SLAVE_ID)
    if not rr.isError():
        print(f"Verifikasi MW5-MW7: {rr.registers}")
        match = rr.registers == nilai
        print(f"  Status: {'OK' if match else 'MISMATCH'}")


def demo_tulis_coil():
    """Demo FC05: Write Single Coil"""
    print("\n=== FC05: Write Single Coil ===")
    
    # Aktifkan Q0.0 (alamat Modbus 2048)
    wc = client.write_coil(address=2048, value=True, slave=SLAVE_ID)
    print(f"Aktifkan Q0.0: {wc}")
    print("  → Lampu/motor seharusnya ON sekarang")
    time.sleep(2)
    
    # Matikan Q0.0
    wc = client.write_coil(address=2048, value=False, slave=SLAVE_ID)
    print(f"Matikan Q0.0: {wc}")
    print("  → Lampu/motor seharusnya OFF sekarang")
    time.sleep(1)
    
    # Aktifkan Q0.1
    wc = client.write_coil(address=2049, value=True, slave=SLAVE_ID)
    print(f"Aktifkan Q0.1: {wc}")
    time.sleep(1)
    wc = client.write_coil(address=2049, value=False, slave=SLAVE_ID)
    print(f"Matikan Q0.1: {wc}")


def demo_tulis_multiple_coils():
    """Demo FC15: Write Multiple Coils"""
    print("\n=== FC15: Write Multiple Coils ===")
    
    # Aktifkan Q0.0 dan Q0.1, matikan Q0.2 dan Q0.3
    status = [True, True, False, False]
    wc = client.write_coils(address=2048, values=status, slave=SLAVE_ID)
    print(f"Tulis Q0.0-Q0.3 = {status}: {wc}")
    time.sleep(2)
    
    # Matikan semua
    wc = client.write_coils(address=2048, values=[False]*4, slave=SLAVE_ID)
    print(f"Matikan Q0.0-Q0.3: {wc}")


def demo_ramp_setpoint():
    """Demo: ramp setpoint dari 0 ke 1000 secara bertahap"""
    print("\n=== DEMO RAMP SETPOINT (MW3: 0 → 1000 → 0) ===")
    
    # Naik dari 0 ke 1000 dalam 10 langkah
    for setpoint in range(0, 1001, 100):
        client.write_register(address=3, value=setpoint, slave=SLAVE_ID)
        rr = client.read_holding_registers(address=3, count=1, slave=SLAVE_ID)
        if not rr.isError():
            print(f"  Setpoint: {rr.registers[0]}")
        time.sleep(0.5)
    
    # Turun kembali ke 0
    for setpoint in range(1000, -1, -100):
        client.write_register(address=3, value=setpoint, slave=SLAVE_ID)
        rr = client.read_holding_registers(address=3, count=1, slave=SLAVE_ID)
        if not rr.isError():
            print(f"  Setpoint: {rr.registers[0]}")
        time.sleep(0.5)


def main():
    if not client.connect():
        print(f"[GAGAL] Tidak dapat terhubung ke {PORT}")
        return

    print(f"[OK] Terhubung ke PLC Slave {SLAVE_ID} via {PORT}")

    try:
        demo_tulis_single_register()
        demo_tulis_multiple_registers()
        demo_tulis_coil()
        demo_tulis_multiple_coils()
        demo_ramp_setpoint()
        print("\n[SELESAI] Semua demo percobaan 02 selesai")
    except KeyboardInterrupt:
        print("\n[INFO] Dihentikan pengguna")
    finally:
        # Pastikan semua output mati saat selesai
        client.write_coils(address=2048, values=[False]*4, slave=SLAVE_ID)
        client.write_register(address=2, value=0, slave=SLAVE_ID)
        client.close()
        print("[INFO] Semua output dimatikan, koneksi ditutup")


if __name__ == "__main__":
    main()
```

---

## D. LANGKAH PERCOBAAN

1. Pastikan program PLC sudah di-download dan berjalan
2. Hubungkan USB-RS485 ke MiniPC
3. Jalankan: `python percobaan02_tulis_register.py`
4. Amati perubahan LED output PLC saat perintah dikirim
5. Verifikasi di EMEB/CX-Programmer bahwa nilai register berubah

---

## E. TABEL PENGAMATAN

| Operasi | Alamat | Nilai Ditulis | Nilai Dibaca | Match? | LED PLC? |
|---------|--------|--------------|-------------|--------|---------|
| Write Single Reg (MW2=1) | 2 | 1 | | | |
| Write Single Reg (MW3=500) | 3 | 500 | | | |
| Write Multiple Regs (MW5-7) | 5 | [100,200,300] | | | |
| Write Coil (Q0.0=ON) | 2048 | True | | | Q0.0 ON? |
| Write Coil (Q0.0=OFF) | 2048 | False | | | Q0.0 OFF? |
| Write Multiple Coils | 2048 | [T,T,F,F] | | | |

---

## F. PERTANYAAN ANALISIS

1. Apa perbedaan FC06 (Write Single Register) vs FC16 (Write Multiple Registers)? Kapan lebih efisien menggunakan FC16?

2. Mengapa menulis nilai ke Coil Q0.0 (FC05) berbeda hasilnya dibanding menulis MW2 untuk mengontrol motor? Jelaskan dua cara kontrol ini.

3. Bagaimana cara memastikan nilai yang ditulis ke PLC benar-benar tersimpan? Mengapa verifikasi baca-setelah-tulis penting?

---

## G. REFERENSI

- Modbus FC05/FC06/FC15/FC16 Specification: https://modbus.org
- pymodbus write functions: https://pymodbus.readthedocs.io
