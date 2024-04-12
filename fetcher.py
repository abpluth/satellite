import requests
from models import SatelliteData, satellite_data
from datetime import datetime, timedelta


def fetch_satellite_data():
    response = requests.get('http://nestio.space/api/satellite/data')
    data = response.json()
    satellite_data.append(SatelliteData(data['altitude'], data['last_updated']))

    # drop data older than 5 minutes
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    while satellite_data and satellite_data[0].last_updated < five_minutes_ago:
        satellite_data.pop(0)
