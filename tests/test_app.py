import unittest
from app import app
from models import satellite_data, SatelliteData
from datetime import datetime, timedelta

class TestStatsEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        satellite_data.clear()

    def test_no_data(self):
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "No data available"})

    def test_with_data(self):
        # Insert mock data
        now = datetime.utcnow()
        satellite_data.extend([
            SatelliteData(200, (now - timedelta(minutes=4)).isoformat() + 'Z'),
            SatelliteData(210, (now - timedelta(minutes=3)).isoformat() + 'Z'),
            SatelliteData(220, (now - timedelta(minutes=2)).isoformat() + 'Z'),
            SatelliteData(230, (now - timedelta(minutes=1)).isoformat() + 'Z'),
            SatelliteData(240, now.isoformat() + 'Z')
        ])

        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['min'], 200)
        self.assertEqual(response.json['max'], 240)
        self.assertAlmostEqual(response.json['average'], 220)

class TestHealthEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        satellite_data.clear()

    def test_no_recent_data(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Altitude is A-OK"})

    def test_average_below_threshold(self):
        now = datetime.utcnow()
        satellite_data.append(SatelliteData(150, now.isoformat() + 'Z'))
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "WARNING: RAPID ORBITAL DECAY IMMINENT"})

    def test_average_above_threshold(self):
        now = datetime.utcnow()
        satellite_data.append(SatelliteData(170, now.isoformat() + 'Z'))
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Sustained Low Earth Orbit Resumed"})

if __name__ == '__main__':
    unittest.main()
