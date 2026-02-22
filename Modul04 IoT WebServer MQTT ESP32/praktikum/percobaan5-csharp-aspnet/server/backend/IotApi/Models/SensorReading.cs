// Percobaan 5 – Backend: Model SensorReading

namespace IotApi.Models;

/// <summary>
/// Merepresentasikan satu pembacaan sensor yang diterima dari ESP32.
/// </summary>
public class SensorReading
{
    public int      Id         { get; set; }
    public string   Device     { get; set; } = string.Empty;
    public int      LightRaw   { get; set; }
    public int      LightPct   { get; set; }
    public int      PotRaw     { get; set; }
    public int      PotPct     { get; set; }
    public long     Uptime     { get; set; }
    public DateTime ReceivedAt { get; set; }
}
