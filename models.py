from datetime import datetime


class SatelliteData:
    def __init__(self, altitude, last_updated):
        self.altitude = float(altitude)
        self.last_updated = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))


# Use a list to store the satellite data objects
satellite_data = []
