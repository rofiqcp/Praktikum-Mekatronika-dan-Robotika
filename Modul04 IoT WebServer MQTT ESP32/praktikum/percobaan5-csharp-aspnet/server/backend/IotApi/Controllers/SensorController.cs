// Percobaan 5 – Backend: SensorController
// Endpoint REST untuk menerima dan mengambil data sensor.

using IotApi.Data;
using IotApi.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace IotApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class SensorsController : ControllerBase
{
    private readonly AppDbContext _db;

    public SensorsController(AppDbContext db)
    {
        _db = db;
    }

    // ── POST /api/sensors ──────────────────────────────────────────────────
    /// <summary>Menerima data sensor dari MQTT Bridge dan menyimpan ke SQLite.</summary>
    [HttpPost]
    public async Task<IActionResult> PostSensor([FromBody] SensorPayloadDto dto)
    {
        if (dto is null)
        {
            return BadRequest(new { error = "Payload tidak valid." });
        }

        var reading = new SensorReading
        {
            Device     = dto.Device     ?? "UNKNOWN",
            LightRaw   = dto.LightRaw,
            LightPct   = dto.LightPct,
            PotRaw     = dto.PotRaw,
            PotPct     = dto.PotPct,
            Uptime     = dto.Uptime,
            ReceivedAt = DateTime.UtcNow,
        };

        _db.SensorReadings.Add(reading);
        await _db.SaveChangesAsync().ConfigureAwait(false);

        return CreatedAtAction(nameof(GetLatest), new { id = reading.Id }, reading);
    }

    // ── GET /api/sensors?limit=50 ──────────────────────────────────────────
    /// <summary>Mengembalikan pembacaan sensor terbaru (default 50).</summary>
    [HttpGet]
    public async Task<IActionResult> GetSensors([FromQuery] int limit = 50)
    {
        limit = Math.Clamp(limit, 1, 200);
        var readings = await _db.SensorReadings
            .OrderByDescending(r => r.ReceivedAt)
            .Take(limit)
            .ToListAsync()
            .ConfigureAwait(false);
        return Ok(readings);
    }

    // ── GET /api/sensors/latest ────────────────────────────────────────────
    /// <summary>Mengembalikan pembacaan sensor paling baru.</summary>
    [HttpGet("latest")]
    public async Task<IActionResult> GetLatest()
    {
        var reading = await _db.SensorReadings
            .OrderByDescending(r => r.ReceivedAt)
            .FirstOrDefaultAsync()
            .ConfigureAwait(false);

        if (reading is null)
        {
            return NotFound(new { error = "Belum ada data sensor." });
        }
        return Ok(reading);
    }

    // ── POST /api/led/brightness ───────────────────────────────────────────
    // Endpoint ini ada di LedController terpisah (lihat catatan README).
}

// ── DTO untuk payload dari MQTT Bridge ────────────────────────────────────────
public record SensorPayloadDto(
    string? Device,
    int     LightRaw,
    int     LightPct,
    int     PotRaw,
    int     PotPct,
    long    Uptime
);
