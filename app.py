import pika
import time
import random
import json
import gzip
import os

from selenium import webdriver
from selenium.webdriver import FirefoxOptions, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver

def trendyol(username, password):
    # Configure Firefox options
    firefox_options = FirefoxOptions()
    
    # Configure Selenium Wire options
    seleniumwire_options = {
        'disable_capture': False,
        'enable_har': False,  # Disable HAR to avoid cookie issues
    }
    
    # Initialize Firefox with Selenium Wire
    driver = webdriver.Firefox(
        options=firefox_options,
        seleniumwire_options=seleniumwire_options
    )

    try:
        # Clear existing requests
        driver.requests.clear()
        
        # Login process
        driver.get("https://www.trendyol.com/Login")
        time.sleep(2)

        # Enter credentials
        driver.find_element(By.ID, "login-email").send_keys(username)
        driver.find_element(By.ID, "login-password-input").send_keys(password)
        driver.find_element(By.ID, "login-password-input").send_keys(Keys.RETURN)
        time.sleep(2)

        # Go to orders page
        driver.get("https://www.trendyol.com/hesabim/siparislerim")
        time.sleep(2)
        
        # Process captured requests
        for request in driver.requests:
            if "orders?page" in request.url.lower() and request.response:
                try:
                    # Trendyol API genellikle gzip sıkıştırma kullanır
                    body = request.response.body
                    
                    # Gzip sıkıştırılmış mı kontrol et
                    if request.response.headers.get('Content-Encoding') == 'gzip':
                        body = gzip.decompress(body)
                    
                    response_text = body.decode('utf-8')
                    
                    # JSON olarak parse edip düzenli yazdır
                    response_json = json.loads(response_text)
                    print(json.dumps(response_json, indent=4, ensure_ascii=False))

                except Exception as decode_error:
                    print(f"Response decode hatası: {decode_error}")

        print(f" [✔] Trendyol isteği tamamlandı!")
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
    finally:
        driver.quit()

def hepsiburada(username, password):
    print(f" [✔] hepsiburada | {username} - {password}")

def n11(username, password):
    print(f" [✔] n11 | {username} - {password}")

def callback(ch, method, properties, body):
    task = body.decode()
    parsed_data = json.loads(task)
    website = parsed_data["Website"]
    username = parsed_data["Username"]
    password = parsed_data["Password"]

    print(f" [x] {website} isteği alındı.")
    
    if website == "trendyol":
        results = trendyol(username, password)
    elif (website == "hepsiburada"):
        hepsiburada(username, password)
        print(f" [✔] {website} isteği tamamlandı!")
    elif (website == "n11"):
        n11(username, password)
        print(f" [✔] {website} isteği tamamlandı!")
    else:
        print(f" [x] {website} servisi bulunamadı!")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

host = os.getenv('RABBITMQ_HOST', 'rabbitmq')  
connection = pika.BlockingConnection(pika.ConnectionParameters(host))
channel = connection.channel()

channel.queue_declare(queue='bot_queue')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='bot_queue', on_message_callback=callback)

print(" [*] Bot çalışıyor, mesaj bekleniyor...")
channel.start_consuming()