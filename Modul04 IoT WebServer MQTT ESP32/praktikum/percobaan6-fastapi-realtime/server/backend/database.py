# Percobaan 6 – Backend: Koneksi MongoDB menggunakan Motor (async)

import motor.motor_asyncio
from pymongo import DESCENDING

MONGO_URL  = "mongodb://localhost:27017"
DB_NAME    = "iot_realtime"

_client: motor.motor_asyncio.AsyncIOMotorClient | None = None


def get_client() -> motor.motor_asyncio.AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    return _client


def get_db():
    return get_client()[DB_NAME]


def get_sensor_collection():
    return get_db()["sensor_readings"]


def get_alert_collection():
    return get_db()["alerts"]


async def init_indexes() -> None:
    """Buat index pada kolom timestamp untuk performa query."""
    sensors = get_sensor_collection()
    alerts  = get_alert_collection()
    await sensors.create_index([("timestamp", DESCENDING)])
    await alerts.create_index([("timestamp", DESCENDING)])
