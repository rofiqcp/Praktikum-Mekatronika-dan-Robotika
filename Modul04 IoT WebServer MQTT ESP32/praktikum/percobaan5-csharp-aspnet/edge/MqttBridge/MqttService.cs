// Percobaan 5 – Edge: MqttService
// Membungkus MQTTnet v4 untuk koneksi, subscribe, dan publish.

using MQTTnet;
using MQTTnet.Client;

namespace MqttBridge;

/// <summary>
/// Mengelola koneksi MQTT menggunakan MQTTnet v4.
/// </summary>
public sealed class MqttService
{
    private readonly string _host;
    private readonly int    _port;
    private readonly IMqttClient _client;
    private readonly MqttFactory _factory;

    /// <summary>
    /// Event yang dipancarkan ketika pesan diterima.
    /// Parameter: topic (string), payload (string).
    /// </summary>
    public event Func<string, string, Task>? MessageReceived;

    public MqttService(string host, int port)
    {
        _host    = host;
        _port    = port;
        _factory = new MqttFactory();
        _client  = _factory.CreateMqttClient();

        // Tangani pesan masuk
        _client.ApplicationMessageReceivedAsync += async e =>
        {
            string topic   = e.ApplicationMessage.Topic;
            string payload = e.ApplicationMessage.ConvertPayloadToString() ?? string.Empty;

            if (MessageReceived is not null)
            {
                await MessageReceived.Invoke(topic, payload).ConfigureAwait(false);
            }
        };

        // Tangani reconnect saat koneksi terputus
        _client.DisconnectedAsync += async e =>
        {
            Console.WriteLine($"[MQTT] Koneksi terputus: {e.Exception?.Message}. Reconnect dalam 5 detik...");
            await Task.Delay(TimeSpan.FromSeconds(5)).ConfigureAwait(false);
            try
            {
                await ConnectAsync().ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[MQTT] Reconnect gagal: {ex.Message}");
            }
        };
    }

    /// <summary>Menghubungkan klien ke MQTT broker.</summary>
    public async Task ConnectAsync()
    {
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(_host, _port)
            .WithClientId($"CSharpBridge-{Guid.NewGuid():N}")
            .WithCleanSession(true)
            .WithKeepAlivePeriod(TimeSpan.FromSeconds(60))
            .Build();

        Console.WriteLine($"[MQTT] Menghubungkan ke {_host}:{_port}...");
        await _client.ConnectAsync(options, CancellationToken.None).ConfigureAwait(false);
        Console.WriteLine("[MQTT] Terhubung!");
    }

    /// <summary>Berlangganan ke sebuah topik MQTT.</summary>
    public async Task SubscribeAsync(string topic)
    {
        var subscribeOptions = _factory.CreateSubscribeOptionsBuilder()
            .WithTopicFilter(f => f.WithTopic(topic))
            .Build();

        await _client.SubscribeAsync(subscribeOptions, CancellationToken.None).ConfigureAwait(false);
        Console.WriteLine($"[MQTT] Subscribe ke topik: {topic}");
    }

    /// <summary>Mempublikasikan payload ke sebuah topik MQTT.</summary>
    public async Task PublishAsync(string topic, string payload)
    {
        var message = new MqttApplicationMessageBuilder()
            .WithTopic(topic)
            .WithPayload(payload)
            .WithQualityOfServiceLevel(MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce)
            .Build();

        await _client.PublishAsync(message, CancellationToken.None).ConfigureAwait(false);
    }
}
