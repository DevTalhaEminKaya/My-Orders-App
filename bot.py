import pika
import time
import random
import json

def trendyol(username, password):
    print(f" [✔] trendyol {username} - {password}")

def hepsiburada(username, password):
    print(f" [✔] hepsiburada {username} - {password}")

def n11(username, password):
    print(f" [✔] n11 {username} - {password}")

def callback(ch, method, properties, body):
    task = body.decode()
    parsed_data = json.loads(task)
    website = parsed_data["Website"]

    print(f" [x] {task} alındı. ")
    
    if (website == "trendyol"):
        trendyol
        print(f" [✔] {task} tamamlandı!")
    elif (website == "hepsiburada"):
        hepsiburada
        print(f" [✔] {task} tamamlandı!")
    elif (website == "n11"):
        n11
        print(f" [✔] {task} tamamlandı!")
    else:
        print(f" [x] {task} bulunamadı!")
    
    # Mesajın işlendiğini bildir
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='bot_queue')

# RabbitMQ'ya mesajları adil dağıtmasını söyle (Fair Dispatch)
channel.basic_qos(prefetch_count=1)

# Mesajı al ve işle
channel.basic_consume(queue='bot_queue', on_message_callback=callback)

print(" [*] Bot çalışıyor, mesaj bekleniyor...")
channel.start_consuming()
