#!/usr/bin/env python3
"""Percobaan 03: Modbus TCP — Baca/Tulis PLC via Ethernet"""

from pymodbus.client import ModbusTcpClient
import time

PLC_IP   = "192.168.1.10"
PLC_PORT = 502
SLAVE_ID = 1

client = ModbusTcpClient(host=PLC_IP, port=PLC_PORT, timeout=3)


def baca_register_tcp():
    t0 = time.perf_counter()
    rr = client.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
    t  = (time.perf_counter() - t0) * 1000
    return (rr.registers if not rr.isError() else None), t


def main():
    if not client.connect():
        print(f"[GAGAL] Tidak dapat koneksi Modbus TCP ke {PLC_IP}:{PLC_PORT}")
        return

    print(f"[OK] Modbus TCP terhubung ke {PLC_IP}:{PLC_PORT}")

    for i in range(10):
        regs, t = baca_register_tcp()
        if regs:
            print(f"[{i+1:02d}] MW0-4={regs[:5]} | {t:.2f}ms")
        time.sleep(1)

    # Tulis register
    for val in [100, 500, 999, 0]:
        client.write_register(address=2, value=val, slave=SLAVE_ID)
        print(f"Tulis MW2={val}")
        time.sleep(0.5)

    # Kontrol output
    client.write_coil(address=2048, value=True, slave=SLAVE_ID)
    print("Q0.0 ON")
    time.sleep(2)
    client.write_coil(address=2048, value=False, slave=SLAVE_ID)
    print("Q0.0 OFF")

    client.close()
    print("[SELESAI]")


if __name__ == "__main__":
    main()
