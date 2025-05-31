from flask import Flask, request, render_template_string, url_for

app = Flask(__name__)

# Biến mô phỏng trạng thái LED
led_state = {"value": False}

# HTML giao diện có hình ảnh LED
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>LED Control</title>
</head>
<body style="text-align:center; font-family:Arial">
<h1>LED is currently: {{ state }}</h1>
<img src="{{ url_for('static', filename=image_file) }}" width="120"><br><br>
<a href="/?led=on"><button style="padding:10px 20px;">Turn ON</button></a>
<a href="/?led=off"><button style="padding:10px 20px;">Turn OFF</button></a>
</body>
</html>
"""

@app.route('/')
def index():
    led = request.args.get("led")
    if led == "on":
        led_state["value"] = True
    elif led == "off":
        led_state["value"] = False

    image_file = "led_on_white_120.png" if led_state["value"] else "led_off_white_120.png"
    return render_template_string(
        HTML_TEMPLATE,
        state="ON" if led_state["value"] else "OFF",
        image_file=image_file
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

