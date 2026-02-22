#!/usr/bin/env python3
"""Percobaan 06: Gateway Modbus RTU → MQTT Broker"""

import time, json, logging
from pymodbus.client import ModbusSerialClient
import paho.mqtt.client as mqtt

PORT          = "/dev/ttyUSB0"
BAUDRATE      = 9600
SLAVE_ID      = 1
MQTT_HOST     = "localhost"
MQTT_PORT     = 1883
MQTT_TOPIC    = "plc/line1/data"
TOPIC_ALARM   = "plc/line1/alarm"
POLL_INTERVAL = 1.0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("gateway")

modbus = ModbusSerialClient(port=PORT, baudrate=BAUDRATE,
                             parity='N', stopbits=1, bytesize=8, timeout=1)
mq = mqtt.Client(client_id="plc_gateway_rtu")
mq.reconnect_delay_set(min_delay=1, max_delay=30)


def on_connect(c, u, f, rc):
    log.info("MQTT OK" if rc == 0 else f"MQTT error rc={rc}")


mq.on_connect = on_connect


def baca_plc():
    rr = modbus.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
    if rr.isError():
        log.warning(f"Gagal baca HR: {rr}")
        return None
    rc = modbus.read_coils(address=2048, count=4, slave=SLAVE_ID)
    ri = modbus.read_input_registers(address=256, count=2, slave=SLAVE_ID)
    return {
        "registers": rr.registers,
        "outputs": [bool(b) for b in rc.bits[:4]] if not rc.isError() else [],
        "analog": ri.registers if not ri.isError() else []
    }


def cek_alarm(data):
    alarms = []
    regs = data.get("registers", [])
    if regs and regs[0] > 3000:
        alarms.append({"type": "HIGH_AI0", "value": regs[0], "threshold": 3000})
    return alarms


def main():
    if not modbus.connect():
        log.error(f"Gagal connect Modbus RTU ke {PORT}")
        return
    mq.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    mq.loop_start()
    log.info(f"Gateway berjalan → topic: {MQTT_TOPIC}")

    count = 0
    try:
        while True:
            data = baca_plc()
            if data:
                payload = {"timestamp": time.time(), "plc_id": SLAVE_ID,
                           "registers": data["registers"],
                           "outputs": data["outputs"],
                           "analog": data["analog"]}
                mq.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
                count += 1
                log.info(f"[{count}] regs={data['registers'][:4]}")
                for alarm in cek_alarm(data):
                    mq.publish(TOPIC_ALARM,
                               json.dumps({"timestamp": time.time(), "alarm": alarm}), qos=2)
                    log.warning(f"ALARM: {alarm}")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        log.info(f"Selesai. Total: {count} pesan")
    finally:
        modbus.close()
        mq.loop_stop()
        mq.disconnect()


if __name__ == "__main__":
    main()
