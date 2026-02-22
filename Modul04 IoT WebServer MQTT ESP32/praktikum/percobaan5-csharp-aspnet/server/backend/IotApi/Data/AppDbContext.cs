// Percobaan 5 – Backend: EF Core DbContext

using IotApi.Models;
using Microsoft.EntityFrameworkCore;

namespace IotApi.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<SensorReading> SensorReadings => Set<SensorReading>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<SensorReading>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Device).HasMaxLength(64).IsRequired();
            entity.Property(e => e.ReceivedAt).IsRequired();
            // Index untuk query terbaru
            entity.HasIndex(e => e.ReceivedAt);
        });
    }
}
