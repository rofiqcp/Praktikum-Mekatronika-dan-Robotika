# Percobaan 6 – Backend: Pydantic Models

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    """Data pembacaan sensor dari ESP32."""
    device:      str           = Field(..., description="ID perangkat ESP32")
    temperature: float         = Field(..., description="Suhu dalam Celsius")
    humidity:    float         = Field(..., description="Kelembaban relatif (%)")
    gas_level:   int           = Field(..., description="Nilai ADC MQ-2 (0-4095)")
    gas_ppm:     float         = Field(..., description="Estimasi konsentrasi gas (ppm)")
    motion:      bool          = Field(..., description="Status deteksi gerak PIR")
    uptime:      int           = Field(..., description="Uptime ESP32 dalam detik")
    timestamp:   Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = {"json_schema_extra": {
        "example": {
            "device":      "ESP32-RT",
            "temperature": 26.5,
            "humidity":    58.0,
            "gas_level":   312,
            "gas_ppm":     45.2,
            "motion":      False,
            "uptime":      12345,
        }
    }}


class Alert(BaseModel):
    """Alert yang dikirim dari edge/ESP32."""
    device:    str            = Field(..., description="ID perangkat")
    alert:     str            = Field(..., description="Jenis alert")
    details:   Optional[dict] = Field(default=None, description="Detail tambahan")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = {"json_schema_extra": {
        "example": {
            "device": "ESP32-RT",
            "alert":  "motion_detected",
        }
    }}


class LedCommand(BaseModel):
    """Perintah kontrol LED ke ESP32."""
    brightness: int = Field(..., ge=0, le=255, description="Brightness 0-255")
