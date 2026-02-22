// Percobaan 5 – Edge: MQTT Bridge entry point
// Menerima data dari ESP32 via MQTT → forward ke ASP.NET Core API via HTTP POST

using MqttBridge;

const string MqttBrokerHost = "127.0.0.1";
const int    MqttBrokerPort = 1883;
const string BackendUrl     = "http://localhost:5000/api/sensors";
const string SubscribeTopic = "bridge/sensors/raw";

Console.WriteLine("=== MQTT-HTTP Bridge ===");
Console.WriteLine($"Broker : {MqttBrokerHost}:{MqttBrokerPort}");
Console.WriteLine($"Backend: {BackendUrl}");
Console.WriteLine($"Topic  : {SubscribeTopic}");
Console.WriteLine();

using HttpClient httpClient = new();
httpClient.Timeout = TimeSpan.FromSeconds(10);

var forwarder   = new HttpForwarder(httpClient, BackendUrl);
var mqttService = new MqttService(MqttBrokerHost, MqttBrokerPort);

// Daftarkan handler saat pesan diterima
mqttService.MessageReceived += async (topic, payload) =>
{
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Pesan diterima [{topic}]:");
    Console.WriteLine($"  Payload: {payload}");

    bool success = await forwarder.ForwardAsync(payload).ConfigureAwait(false);
    Console.WriteLine(success
        ? "  → HTTP forward: BERHASIL"
        : "  → HTTP forward: GAGAL");
};

// Hubungkan ke broker dan subscribe
await mqttService.ConnectAsync().ConfigureAwait(false);
await mqttService.SubscribeAsync(SubscribeTopic).ConfigureAwait(false);

Console.WriteLine("Bridge berjalan. Tekan Ctrl+C untuk berhenti.\n");

// Tetap berjalan hingga dibatalkan
var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) =>
{
    e.Cancel = true;
    cts.Cancel();
};

try
{
    await Task.Delay(Timeout.Infinite, cts.Token).ConfigureAwait(false);
}
catch (OperationCanceledException)
{
    Console.WriteLine("\nBridge dihentikan.");
}
