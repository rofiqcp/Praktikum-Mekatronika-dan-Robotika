package com.iot.praktikum.repository;

import com.iot.praktikum.model.SensorReading;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface SensorReadingRepository extends JpaRepository<SensorReading, Long> {

    List<SensorReading> findTop100ByOrderByRecordedAtDesc();

    List<SensorReading> findByRecordedAtBetween(LocalDateTime start, LocalDateTime end);

    @Query("SELECT s FROM SensorReading s WHERE s.device = :device ORDER BY s.recordedAt DESC")
    List<SensorReading> findLatestByDevice(@Param("device") String device, Pageable pageable);

    @Query("""
        SELECT new com.iot.praktikum.repository.SensorStats(
            MIN(s.temperature), MAX(s.temperature), AVG(s.temperature),
            MIN(s.humidity),    MAX(s.humidity),    AVG(s.humidity),
            MIN(s.light),       MAX(s.light),       AVG(CAST(s.light AS double)),
            MIN(s.soilMoisture),MAX(s.soilMoisture),AVG(CAST(s.soilMoisture AS double))
        ) FROM SensorReading s
    """)
    Optional<SensorStats> computeStats();

    List<SensorReading> findByOrderByRecordedAtDesc(Pageable pageable);
}
