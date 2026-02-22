"""
Percobaan 6 – Database: Inisialisasi MongoDB
Membuat collection dengan schema validation, index, dan data sample.

Jalankan sekali sebelum menjalankan backend:
    python init_mongo.py
"""

from datetime import datetime, timezone
import pymongo

MONGO_URL = "mongodb://localhost:27017"
DB_NAME   = "iot_realtime"

client = pymongo.MongoClient(MONGO_URL)
db     = client[DB_NAME]


def init_sensor_collection():
    """Buat collection sensor_readings dengan validasi skema."""
    if "sensor_readings" in db.list_collection_names():
        print("[INFO] Collection 'sensor_readings' sudah ada.")
    else:
        db.create_collection(
            "sensor_readings",
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["device", "temperature", "humidity", "gas_ppm", "motion", "timestamp"],
                    "properties": {
                        "device":      {"bsonType": "string"},
                        "temperature": {"bsonType": ["double", "int"]},
                        "humidity":    {"bsonType": ["double", "int"]},
                        "gas_level":   {"bsonType": ["int", "double"]},
                        "gas_ppm":     {"bsonType": ["double", "int"]},
                        "motion":      {"bsonType": "bool"},
                        "uptime":      {"bsonType": ["int", "long"]},
                        "timestamp":   {"bsonType": ["date", "string"]},
                    }
                }
            },
            validationAction="warn",   # warn agar data lama tidak ditolak
        )
        print("[OK] Collection 'sensor_readings' dibuat.")

    # Index pada timestamp untuk query cepat
    db["sensor_readings"].create_index(
        [("timestamp", pymongo.DESCENDING)], name="idx_timestamp_desc"
    )
    db["sensor_readings"].create_index(
        [("device", pymongo.ASCENDING)], name="idx_device"
    )
    print("[OK] Index 'sensor_readings' dibuat.")


def init_alerts_collection():
    """Buat collection alerts."""
    if "alerts" in db.list_collection_names():
        print("[INFO] Collection 'alerts' sudah ada.")
    else:
        db.create_collection("alerts")
        print("[OK] Collection 'alerts' dibuat.")

    db["alerts"].create_index(
        [("timestamp", pymongo.DESCENDING)], name="idx_alert_timestamp"
    )
    print("[OK] Index 'alerts' dibuat.")


def insert_sample_data():
    """Masukkan data sample untuk testing."""
    now = datetime.now(timezone.utc)

    sample_sensors = [
        {
            "device":      "ESP32-RT",
            "temperature": 25.5 + i * 0.3,
            "humidity":    60.0 - i * 0.5,
            "gas_level":   200 + i * 10,
            "gas_ppm":     28.0 + i * 1.5,
            "motion":      i % 5 == 0,
            "uptime":      i * 5,
            "_type":       "sensor",
            "timestamp":   now,
        }
        for i in range(10)
    ]

    sample_alerts = [
        {
            "device":    "ESP32-RT",
            "alert":     "motion_detected",
            "_type":     "alert",
            "timestamp": now,
        },
        {
            "device":    "ESP32-RT",
            "alert":     "anomaly_detected",
            "anomalies": [{"field": "temperature", "value": 45.2, "z_score": 2.8}],
            "_type":     "alert",
            "timestamp": now,
        },
    ]

    if db["sensor_readings"].count_documents({}) == 0:
        db["sensor_readings"].insert_many(sample_sensors)
        print(f"[OK] {len(sample_sensors)} data sensor sample dimasukkan.")
    else:
        print("[INFO] Data sensor sudah ada, skip insert sample.")

    if db["alerts"].count_documents({}) == 0:
        db["alerts"].insert_many(sample_alerts)
        print(f"[OK] {len(sample_alerts)} alert sample dimasukkan.")
    else:
        print("[INFO] Data alert sudah ada, skip insert sample.")


def main():
    print(f"=== Inisialisasi MongoDB: {DB_NAME} ===")
    init_sensor_collection()
    init_alerts_collection()
    insert_sample_data()

    print("\n=== Ringkasan ===")
    for col in ["sensor_readings", "alerts"]:
        count = db[col].count_documents({})
        print(f"  {col}: {count} dokumen")

    print("\nInisialisasi selesai.")
    client.close()


if __name__ == "__main__":
    main()
