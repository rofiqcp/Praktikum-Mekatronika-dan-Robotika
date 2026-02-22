package com.iot.praktikum.controller;

import com.iot.praktikum.model.SensorReading;
import com.iot.praktikum.service.SensorService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/sensors")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class SensorController {

    private final SensorService sensorService;

    /**
     * POST /api/sensors
     * Save a new sensor reading from the edge processor.
     */
    @PostMapping
    public ResponseEntity<SensorReading> saveSensorReading(@Valid @RequestBody SensorReading reading) {
        SensorReading saved = sensorService.save(reading);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    /**
     * GET /api/sensors?limit=100
     * Return the most recent sensor readings.
     */
    @GetMapping
    public ResponseEntity<List<SensorReading>> getRecentReadings(
            @RequestParam(defaultValue = "100") int limit) {
        return ResponseEntity.ok(sensorService.getRecent(limit));
    }

    /**
     * GET /api/sensors/stats
     * Return min/max/avg statistics for each sensor field.
     */
    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getStats() {
        return ResponseEntity.ok(sensorService.getStats());
    }

    /**
     * GET /api/sensors/device/{device}
     * Return readings for a specific device (max 100).
     */
    @GetMapping("/device/{device}")
    public ResponseEntity<List<SensorReading>> getByDevice(@PathVariable String device) {
        return ResponseEntity.ok(sensorService.getByDevice(device));
    }

    /**
     * GET /api/sensors/range?start=...&end=...
     * Return readings within a time range (ISO-8601 datetime).
     */
    @GetMapping("/range")
    public ResponseEntity<List<SensorReading>> getByTimeRange(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime end) {
        return ResponseEntity.ok(sensorService.getByTimeRange(start, end));
    }
}
