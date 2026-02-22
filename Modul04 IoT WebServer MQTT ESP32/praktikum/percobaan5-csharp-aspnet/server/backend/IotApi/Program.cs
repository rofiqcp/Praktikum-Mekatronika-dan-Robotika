// Percobaan 5 – Backend: Program.cs
// Minimal hosting ASP.NET Core 8 dengan EF Core SQLite dan CORS.

using IotApi.Data;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// ─── Services ─────────────────────────────────────────────────────────────────
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

// EF Core SQLite
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")
        ?? "Data Source=iot_sensor.db"));

// CORS – izinkan semua origin (untuk development)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader());
});

var app = builder.Build();

// ─── Auto Migrate ─────────────────────────────────────────────────────────────
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();
}

// ─── Middleware ───────────────────────────────────────────────────────────────
app.UseRouting();
app.UseCors("AllowAll");
app.MapControllers();

// Health check sederhana
app.MapGet("/", () => Results.Ok(new { status = "IoT API berjalan", time = DateTime.UtcNow }));

app.Run();
