import { Component, OnInit, OnDestroy } from '@angular/core';
import { SensorService, SensorReading, SensorStats } from '../sensor.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit, OnDestroy {

  readings: SensorReading[]  = [];
  stats: SensorStats | null  = null;
  latest: SensorReading | null = null;
  lastUpdated = '—';
  errorMessage = '';

  private pollTimer: ReturnType<typeof setInterval> | null = null;
  readonly POLL_INTERVAL_MS = 5000;

  constructor(private sensorService: SensorService) {}

  ngOnInit(): void {
    this.fetchAll();
    this.pollTimer = setInterval(() => this.fetchAll(), this.POLL_INTERVAL_MS);
  }

  ngOnDestroy(): void {
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
    }
  }

  fetchAll(): void {
    this.sensorService.getRecent(20).subscribe({
      next: data => {
        this.readings = data;
        this.latest   = data.length > 0 ? data[0] : null;
        this.lastUpdated = new Date().toLocaleTimeString('id-ID');
        this.errorMessage = '';
      },
      error: err => {
        this.errorMessage = `Gagal mengambil data: ${err.message}`;
      },
    });

    this.sensorService.getStats().subscribe({
      next: data => { this.stats = data; },
      error: ()  => {},
    });
  }

  humidityClass(value: number | undefined): string {
    if (value === undefined || value === null) return 'neutral';
    if (value < 30) return 'low';
    if (value > 80) return 'high';
    return 'normal';
  }

  tempClass(value: number | undefined): string {
    if (value === undefined || value === null) return 'neutral';
    if (value < 15) return 'cold';
    if (value > 35) return 'hot';
    return 'normal';
  }

  soilClass(value: number | undefined): string {
    if (value === undefined || value === null) return 'neutral';
    if (value < 20) return 'dry';
    if (value > 80) return 'wet';
    return 'normal';
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '—';
    return new Date(dateStr).toLocaleString('id-ID');
  }
}
