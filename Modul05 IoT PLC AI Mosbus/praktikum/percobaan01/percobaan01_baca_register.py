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
PORT      = "/dev/ttyUSB0"  # Linux; Windows: "COM3", "COM4"
BAUDRATE  = 9600
PARITY    = 'N'
STOPBITS  = 1
BYTESIZE  = 8
TIMEOUT   = 2
SLAVE_ID  = 1
INTERVAL  = 1.0
# ============================================================


def buat_client():
    return ModbusSerialClient(
        port=PORT, baudrate=BAUDRATE, parity=PARITY,
        stopbits=STOPBITS, bytesize=BYTESIZE, timeout=TIMEOUT
    )


def baca_holding_registers(client, alamat=0, jumlah=10):
    result = client.read_holding_registers(address=alamat, count=jumlah, slave=SLAVE_ID)
    if result.isError():
        print(f"[ERROR] Baca HR alamat {alamat}: {result}")
        return None
    return result.registers


def baca_coils(client, alamat=2048, jumlah=4):
    result = client.read_coils(address=alamat, count=jumlah, slave=SLAVE_ID)
    if result.isError():
        print(f"[ERROR] Baca Coil alamat {alamat}: {result}")
        return None
    return result.bits[:jumlah]


def baca_discrete_inputs(client, alamat=0, jumlah=4):
    result = client.read_discrete_inputs(address=alamat, count=jumlah, slave=SLAVE_ID)
    if result.isError():
        print(f"[ERROR] Baca DI alamat {alamat}: {result}")
        return None
    return result.bits[:jumlah]


def main():
    client = buat_client()
    print(f"Menghubungkan ke PLC via {PORT}...")

    if not client.connect():
        print(f"[GAGAL] Tidak dapat terhubung ke {PORT}")
        return

    print(f"[OK] Terhubung ke PLC (Slave ID: {SLAVE_ID}, {BAUDRATE}-8-N-1)")
    print("-" * 60)

    iterasi = 0
    try:
        while True:
            iterasi += 1
            print(f"\n--- Iterasi {iterasi} ---")

            regs = baca_holding_registers(client, alamat=0, jumlah=10)
            if regs:
                print("Holding Register (MW0-MW9):")
                for i, val in enumerate(regs):
                    print(f"  MW{i} = {val} (0x{val:04X})")

            coils = baca_coils(client, alamat=2048, jumlah=4)
            if coils is not None:
                print(f"Output (Q0.0-Q0.3): {['ON' if c else 'OFF' for c in coils]}")

            inputs = baca_discrete_inputs(client, alamat=0, jumlah=4)
            if inputs is not None:
                print(f"Input  (I0.0-I0.3): {['ON' if i else 'OFF' for i in inputs]}")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n[INFO] Program dihentikan (Ctrl+C)")
    finally:
        client.close()
        print("[INFO] Koneksi Modbus ditutup")


if __name__ == "__main__":
    main()
