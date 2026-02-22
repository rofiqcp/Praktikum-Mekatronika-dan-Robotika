#!/usr/bin/env python3
"""Percobaan 08: Gateway Modbus RTU → REST API (HTTP POST)"""

import time, logging, requests
from pymodbus.client import ModbusSerialClient

PORT     = "/dev/ttyUSB0"
SLAVE_ID = 1
API_URL  = "http://localhost:8000/api/v1/plc/data"
INTERVAL = 2.0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("rest_gateway")

modbus = ModbusSerialClient(port=PORT, baudrate=9600,
                             parity='N', stopbits=1, bytesize=8, timeout=1)
if not modbus.connect():
    log.error(f"Gagal connect Modbus ke {PORT}")
    exit(1)

log.info(f"Gateway REST berjalan → {API_URL}")

while True:
    rr = modbus.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
    rc = modbus.read_coils(address=2048, count=4, slave=SLAVE_ID)

    if not rr.isError():
        payload = {
            "plc_id":    SLAVE_ID,
            "registers": rr.registers,
            "outputs":   [bool(b) for b in rc.bits[:4]] if not rc.isError() else []
        }
        try:
            resp = requests.post(API_URL, json=payload, timeout=5)
            log.info(f"POST {resp.status_code}: {resp.json()}")
        except requests.exceptions.ConnectionError:
            log.warning("API server tidak terjangkau")
        except requests.exceptions.Timeout:
            log.warning("Request timeout")
    else:
        log.error(f"Modbus error: {rr}")

    time.sleep(INTERVAL)
