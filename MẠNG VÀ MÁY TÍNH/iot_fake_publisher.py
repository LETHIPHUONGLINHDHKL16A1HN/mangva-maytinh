import paho.mqtt.client as mqtt
import json
import time
import random

broker = "broker.hivemq.com"
port = 1883
topic = "iot/khdl/esp32"

client = mqtt.Client()
client.connect(broker, port, 60)

while True:
    data = {
        "temperature": round(random.uniform(23, 28), 2),
        "humidity": round(random.uniform(35, 55), 2),
        "timestamp": time.time()
    }
    client.publish(topic, json.dumps(data))
    print("📤 Đã gửi:", data)
    time.sleep(2)
