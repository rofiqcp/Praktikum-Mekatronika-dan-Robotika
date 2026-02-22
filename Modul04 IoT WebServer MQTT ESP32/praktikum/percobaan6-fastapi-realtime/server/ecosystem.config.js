// Percobaan 6 – PM2 Ecosystem Config
// Mengelola proses backend uvicorn dengan PM2.
//
// Jalankan:
//   pm2 start ecosystem.config.js
//   pm2 save
//   pm2 startup   (opsional: autostart saat boot)

module.exports = {
  apps: [
    {
      name:         "iot-backend",
      cwd:          "./backend",
      script:       "uvicorn",
      args:         "main:app --host 0.0.0.0 --port 8000 --workers 1",
      interpreter:  "none",
      watch:        false,
      autorestart:  true,
      max_restarts: 10,
      restart_delay: 3000,
      env: {
        PYTHONUNBUFFERED: "1",
      },
      error_file: "./logs/backend-error.log",
      out_file:   "./logs/backend-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
    {
      // Anomaly detector berjalan di edge, tapi bisa dikelola PM2 juga
      name:         "iot-anomaly-detector",
      cwd:          "../edge",
      script:       "python",
      args:         "anomaly_detector.py",
      interpreter:  "none",
      watch:        false,
      autorestart:  true,
      max_restarts: 10,
      restart_delay: 5000,
      env: {
        PYTHONUNBUFFERED: "1",
      },
      error_file: "./logs/anomaly-error.log",
      out_file:   "./logs/anomaly-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
  ],
};
