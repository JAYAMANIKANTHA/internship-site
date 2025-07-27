# LiveFaceCamBot with Face Detection

Advanced Telegram bot that captures and sends a photo when a face is detected.

## Features

- ✅ Face detection using OpenCV
- ✅ Auto-send photo on /start or /photo if a face is found
- ✅ System info, IP-based geo-location, Android telemetry

## Setup

```bash
pip install -r requirements.txt
```

Replace `YOUR_BOT_TOKEN_HERE` in the Python file with your Telegram bot token.

## Commands

- `/start` – Start and detect face
- `/photo` – Capture and send photo if face is detected
- `/info` – Get system info
- `/geo` – Get location
- `/battery` – Mobile info (Android only)

