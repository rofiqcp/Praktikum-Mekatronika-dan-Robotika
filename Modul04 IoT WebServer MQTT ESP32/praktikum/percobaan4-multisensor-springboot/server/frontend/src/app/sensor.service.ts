import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SensorReading {
  id?: number;
  device: string;
  temperature: number;
  humidity: number;
  light: number;
  soilMoisture: number;
  battery: number;
  recordedAt: string;
  location?: string;
}

export interface SensorFieldStats {
  min: number;
  max: number;
  avg: number;
}

export interface SensorStats {
  temperature:  SensorFieldStats;
  humidity:     SensorFieldStats;
  light:        SensorFieldStats;
  soilMoisture: SensorFieldStats;
}

@Injectable({ providedIn: 'root' })
export class SensorService {

  private readonly BASE = 'http://localhost:8080/api/sensors';

  constructor(private http: HttpClient) {}

  getRecent(limit: number = 20): Observable<SensorReading[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<SensorReading[]>(this.BASE, { params });
  }

  getStats(): Observable<SensorStats> {
    return this.http.get<SensorStats>(`${this.BASE}/stats`);
  }

  getByDevice(device: string): Observable<SensorReading[]> {
    return this.http.get<SensorReading[]>(`${this.BASE}/device/${encodeURIComponent(device)}`);
  }
}
