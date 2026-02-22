package com.iot.praktikum.repository;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Projection / DTO for aggregate statistics returned by JPQL constructor expression.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SensorStats {

    private Double tempMin;
    private Double tempMax;
    private Double tempAvg;

    private Double humMin;
    private Double humMax;
    private Double humAvg;

    private Integer lightMin;
    private Integer lightMax;
    private Double  lightAvg;

    private Integer soilMin;
    private Integer soilMax;
    private Double  soilAvg;
}
