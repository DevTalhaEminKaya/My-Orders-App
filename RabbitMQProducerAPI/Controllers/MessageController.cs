using Microsoft.AspNetCore.Mvc;
using RabbitMQ.Client;
using System;
using System.Text;
using Newtonsoft.Json;

namespace RabbitMQProducerAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MessageController : ControllerBase
    {
        [HttpPost("{website}/{username}/{password}")]
        public IActionResult Trendyol()
        {
            try
            {
                // Bağlantıyı RabbitMQ'ya bağla
                var factory = new ConnectionFactory() { HostName = "localhost" };

                using var connection = factory.CreateConnection();
                using var channel = connection.CreateModel();

                channel.QueueDeclare(queue: "bot_queue",
                                     durable: false,
                                     exclusive: false,
                                     autoDelete: false,
                                     arguments: null);

                var message = new
                {
                    Website = website
                    Username = username, 
                    Password = password
                };

                var jsonMessage = JsonConvert.SerializeObject(message);
                var body = Encoding.UTF8.GetBytes(jsonMessage);

                channel.BasicPublish(exchange: "",
                                     routingKey: "bot_queue",
                                     basicProperties: null,
                                     body: body);

                return Ok($"Mesaj kuyruğa eklendi: {task}");
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Hata: {ex.Message}");
            }
        }
    }
}
