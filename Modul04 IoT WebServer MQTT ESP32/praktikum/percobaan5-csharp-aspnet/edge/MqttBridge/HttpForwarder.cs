// Percobaan 5 – Edge: HttpForwarder
// Meneruskan payload JSON ke ASP.NET Core API via HTTP POST.

using System.Net.Http.Headers;
using System.Text;

namespace MqttBridge;

/// <summary>
/// Meneruskan data sensor (JSON string) ke backend HTTP.
/// </summary>
public sealed class HttpForwarder
{
    private readonly HttpClient _httpClient;
    private readonly string     _backendUrl;

    public HttpForwarder(HttpClient httpClient, string backendUrl)
    {
        _httpClient = httpClient;
        _backendUrl = backendUrl;
    }

    /// <summary>
    /// Mengirim payload JSON ke backend via HTTP POST.
    /// </summary>
    /// <param name="json">String JSON yang akan dikirim.</param>
    /// <returns>True jika HTTP 2xx, false jika terjadi kesalahan.</returns>
    public async Task<bool> ForwardAsync(string json)
    {
        try
        {
            using var content = new StringContent(json, Encoding.UTF8, "application/json");
            using HttpResponseMessage response = await _httpClient
                .PostAsync(_backendUrl, content)
                .ConfigureAwait(false);

            if (response.IsSuccessStatusCode)
            {
                return true;
            }

            string body = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
            Console.WriteLine($"[HTTP] Status {(int)response.StatusCode}: {body}");
            return false;
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"[HTTP] Request error: {ex.Message}");
            return false;
        }
        catch (TaskCanceledException)
        {
            Console.WriteLine("[HTTP] Request timeout.");
            return false;
        }
    }
}
