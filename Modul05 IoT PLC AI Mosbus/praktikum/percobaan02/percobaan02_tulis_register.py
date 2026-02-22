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
    rr = client.read_holding_registers(address=alamat, count=1, slave=SLAVE_ID)
    if not rr.isError():
        nilai_baca = rr.registers[0]
        status = "OK" if nilai_baca == nilai_ditulis else "MISMATCH"
        print(f"  Verifikasi {nama}[{alamat}]: tulis={nilai_ditulis}, baca={nilai_baca} [{status}]")
        return nilai_baca == nilai_ditulis
    return False


def demo_tulis_single_register():
    print("\n=== FC06: Write Single Holding Register ===")
    client.write_register(address=2, value=1, slave=SLAVE_ID)
    print("Tulis MW2=1 (Motor ON)")
    verifikasi_tulis("MW2", 2, 1)
    time.sleep(2)

    client.write_register(address=3, value=500, slave=SLAVE_ID)
    print("Tulis MW3=500 (Setpoint)")
    verifikasi_tulis("MW3", 3, 500)
    time.sleep(1)

    client.write_register(address=2, value=0, slave=SLAVE_ID)
    print("Tulis MW2=0 (Motor OFF)")
    verifikasi_tulis("MW2", 2, 0)


def demo_tulis_multiple_registers():
    print("\n=== FC16: Write Multiple Holding Registers ===")
    nilai = [100, 200, 300]
    client.write_registers(address=5, values=nilai, slave=SLAVE_ID)
    print(f"Tulis MW5-MW7 = {nilai}")
    rr = client.read_holding_registers(address=5, count=3, slave=SLAVE_ID)
    if not rr.isError():
        print(f"Verifikasi MW5-MW7: {rr.registers}")


def demo_tulis_coil():
    print("\n=== FC05: Write Single Coil ===")
    client.write_coil(address=2048, value=True, slave=SLAVE_ID)
    print("Aktifkan Q0.0 → LED harus ON")
    time.sleep(2)
    client.write_coil(address=2048, value=False, slave=SLAVE_ID)
    print("Matikan Q0.0 → LED harus OFF")
    time.sleep(1)
    client.write_coil(address=2049, value=True, slave=SLAVE_ID)
    print("Aktifkan Q0.1")
    time.sleep(1)
    client.write_coil(address=2049, value=False, slave=SLAVE_ID)
    print("Matikan Q0.1")


def demo_tulis_multiple_coils():
    print("\n=== FC15: Write Multiple Coils ===")
    status = [True, True, False, False]
    client.write_coils(address=2048, values=status, slave=SLAVE_ID)
    print(f"Tulis Q0.0-Q0.3 = {status}")
    time.sleep(2)
    client.write_coils(address=2048, values=[False] * 4, slave=SLAVE_ID)
    print("Matikan Q0.0-Q0.3")


def demo_ramp_setpoint():
    print("\n=== DEMO RAMP SETPOINT MW3: 0 → 1000 → 0 ===")
    for setpoint in range(0, 1001, 100):
        client.write_register(address=3, value=setpoint, slave=SLAVE_ID)
        print(f"  Setpoint: {setpoint}")
        time.sleep(0.3)
    for setpoint in range(1000, -1, -100):
        client.write_register(address=3, value=setpoint, slave=SLAVE_ID)
        print(f"  Setpoint: {setpoint}")
        time.sleep(0.3)


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
        client.write_coils(address=2048, values=[False] * 4, slave=SLAVE_ID)
        client.write_register(address=2, value=0, slave=SLAVE_ID)
        client.close()
        print("[INFO] Semua output dimatikan, koneksi ditutup")


if __name__ == "__main__":
    main()
