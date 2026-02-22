package com.iot.praktikum.service;

import com.iot.praktikum.model.SensorReading;
import com.iot.praktikum.repository.SensorReadingRepository;
import com.iot.praktikum.repository.SensorStats;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class SensorService {

    private final SensorReadingRepository repository;

    @Transactional
    public SensorReading save(SensorReading reading) {
        if (reading.getRecordedAt() == null) {
            reading.setRecordedAt(LocalDateTime.now());
        }
        return repository.save(reading);
    }

    @Transactional(readOnly = true)
    public List<SensorReading> getRecent(int limit) {
        int capped = Math.min(Math.max(limit, 1), 500);
        return repository.findByOrderByRecordedAtDesc(PageRequest.of(0, capped));
    }

    @Transactional(readOnly = true)
    public Map<String, Object> getStats() {
        Optional<SensorStats> opt = repository.computeStats();
        Map<String, Object> result = new HashMap<>();

        if (opt.isEmpty()) {
            return result;
        }

        SensorStats s = opt.get();

        Map<String, Object> temp = new HashMap<>();
        temp.put("min", round(s.getTempMin(), 1));
        temp.put("max", round(s.getTempMax(), 1));
        temp.put("avg", round(s.getTempAvg(), 1));
        result.put("temperature", temp);

        Map<String, Object> hum = new HashMap<>();
        hum.put("min", round(s.getHumMin(), 1));
        hum.put("max", round(s.getHumMax(), 1));
        hum.put("avg", round(s.getHumAvg(), 1));
        result.put("humidity", hum);

        Map<String, Object> light = new HashMap<>();
        light.put("min", s.getLightMin());
        light.put("max", s.getLightMax());
        light.put("avg", round(s.getLightAvg(), 1));
        result.put("light", light);

        Map<String, Object> soil = new HashMap<>();
        soil.put("min", s.getSoilMin());
        soil.put("max", s.getSoilMax());
        soil.put("avg", round(s.getSoilAvg(), 1));
        result.put("soilMoisture", soil);

        return result;
    }

    @Transactional(readOnly = true)
    public List<SensorReading> getByTimeRange(LocalDateTime start, LocalDateTime end) {
        return repository.findByRecordedAtBetween(start, end);
    }

    @Transactional(readOnly = true)
    public List<SensorReading> getByDevice(String device) {
        return repository.findLatestByDevice(device, PageRequest.of(0, 100));
    }

    private static Double round(Double value, int decimals) {
        if (value == null) return null;
        double factor = Math.pow(10, decimals);
        return Math.round(value * factor) / factor;
    }
}
