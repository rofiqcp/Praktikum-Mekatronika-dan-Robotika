/**
 * Percobaan 04: ESP32 Modbus RTU Master
 * Membaca Holding Register dan Coil dari PLC TM221/CP2E
 *
 * Library: emelianov/modbus-esp8266
 * Hardware: ESP32 + MAX485 + PLC via RS-485
 */

#include <Arduino.h>
#include <ModbusRTU.h>

#define RXD2         16
#define TXD2         17
#define RS485_DE_RE   4

#define PLC_SLAVE_ID  1
#define REG_START     0
#define REG_COUNT    10
#define COIL_START 2048
#define COIL_COUNT    4

#define POLL_INTERVAL_MS 1000

ModbusRTU mb;

uint16_t regData[REG_COUNT];
bool     coilData[COIL_COUNT];
bool     regReady   = false;
bool     coilReady  = false;
uint32_t lastPoll   = 0;
uint32_t errorCount = 0;

bool cbReadRegs(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        regReady = true;
    } else {
        Serial.printf("[ERROR] ReadHreg: 0x%02X\n", event);
        errorCount++;
    }
    return true;
}

bool cbReadCoils(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        coilReady = true;
    } else {
        Serial.printf("[ERROR] ReadCoil: 0x%02X\n", event);
        errorCount++;
    }
    return true;
}

void tampilkanData() {
    Serial.println("--------------------------------------");
    Serial.print("Holding Registers (MW0-MW9): ");
    for (int i = 0; i < REG_COUNT; i++) {
        Serial.printf("MW%d=%d ", i, regData[i]);
    }
    Serial.println();
    Serial.print("Coils (Q0.0-Q0.3): ");
    for (int i = 0; i < COIL_COUNT; i++) {
        Serial.printf("Q0.%d=%s ", i, coilData[i] ? "ON" : "OFF");
    }
    Serial.println();
    Serial.printf("Errors: %lu\n", errorCount);
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
    mb.begin(&Serial2, RS485_DE_RE);
    mb.master();
    Serial.println("=== ESP32 Modbus RTU Master ===");
    Serial.printf("RX=%d TX=%d DE/RE=%d Slave=%d\n",
                  RXD2, TXD2, RS485_DE_RE, PLC_SLAVE_ID);
}

void loop() {
    mb.task();

    uint32_t now = millis();
    if (now - lastPoll >= POLL_INTERVAL_MS) {
        lastPoll = now;
        if (!mb.slave()) {
            mb.readHreg(PLC_SLAVE_ID, REG_START, regData, REG_COUNT, cbReadRegs);
        }
    }

    if (regReady) {
        regReady = false;
        tampilkanData();
        mb.readCoil(PLC_SLAVE_ID, COIL_START, coilData, COIL_COUNT, cbReadCoils);
    }
}
