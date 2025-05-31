import paho.mqtt.client as mqtt
import sqlite3
import time
import json
import matplotlib.pyplot as plt

# ==== Cấu hình cơ bản ====
DB_FILE = "sensor_data.db"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/khdl/esp32"

# ==== Kết nối SQLite và tạo bảng nếu chưa có ====
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    timestamp REAL,
    temperature REAL,
    humidity REAL
)
""")
conn.commit()

# ==== Danh sách lưu dữ liệu để vẽ biểu đồ ====
temps, hums, times = [], [], []

# ==== Hàm xử lý khi kết nối MQTT thành công ====
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Đã kết nối MQTT broker.")
        client.subscribe(MQTT_TOPIC)
    else:
        print("❌ Kết nối thất bại, mã lỗi:", rc)

# ==== Hàm xử lý khi nhận dữ liệu từ MQTT ====
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        timestamp = data.get("timestamp", time.time())
        temp = data.get("temperature", 0)
        hum = data.get("humidity", 0)

        print(f"📥 Dữ liệu nhận: {timestamp}, {temp}, {hum}")

        # Ghi vào SQLite
        cursor.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, temp, hum))
        conn.commit()

        # Thêm vào danh sách để vẽ
        temps.append(temp)
        hums.append(hum)
        times.append(timestamp)

        # Cập nhật biểu đồ mỗi 2 điểm
        if len(temps) % 2 == 0:
            plt.clf()
            plt.subplot(2, 1, 1)
            plt.plot(times, temps, 'r-', label='Nhiệt độ (°C)')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(times, hums, 'b-', label='Độ ẩm (%)')
            plt.legend()

            plt.pause(0.1)

    except Exception as e:
        print("⚠️ Lỗi xử lý:", e)

# ==== Khởi tạo MQTT client ====
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# ==== Kết nối và chạy vòng lặp ====
client.connect(MQTT_BROKER, MQTT_PORT, 60)
plt.ion()  # Bật chế độ vẽ tương tác
client.loop_forever()
