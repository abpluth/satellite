import threading
import time
from datetime import datetime, timedelta, timezone

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv
from flask import Flask, jsonify

import fetcher
from models import satellite_data

load_dotenv()
app = Flask(__name__)
asgi_app = WsgiToAsgi(app)


# TODO: add config
def fetch_data_periodically():
    while True:
        fetcher.fetch_satellite_data()
        time.sleep(10)


@app.route("/stats")
def stats():
    if not satellite_data:
        return jsonify({"message": "No data available"}), 200

    altitudes = [data.altitude for data in satellite_data]
    return jsonify(
        {
            "min": min(altitudes),
            "max": max(altitudes),
            "average": sum(altitudes) / len(altitudes),
        }
    )


@app.route("/health")
def health():
    one_minute_ago = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(
        minutes=1
    )
    recent_data = [
        data for data in satellite_data if data.last_updated >= one_minute_ago
    ]

    if not recent_data:
        return jsonify({"message": "Altitude is A-OK"})

    avg_altitude = sum(data.altitude for data in recent_data) / len(recent_data)
    if avg_altitude < 160:
        return jsonify({"message": "WARNING: RAPID ORBITAL DECAY IMMINENT"})
    else:
        return jsonify({"message": "Sustained Low Earth Orbit Resumed"})


if __name__ == "__main__":
    thread = threading.Thread(target=fetch_data_periodically)
    thread.start()
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)
