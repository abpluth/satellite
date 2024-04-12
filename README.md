# Satellite Health Monitoring API

This web application monitors the health of a satellite by fetching real-time data from an external API and provides statistics on the satellite's altitude.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following tools installed:
- Python 3.12 or higher
- Poetry for dependency management

### Installing

```bash
# Clone the repository to your local machine:
git clone git@github.com:abpluth/satellite.git
# Navigate to the cloned directory:
cd satellite
# Install the required dependencies using Poetry:
poetry install
```

### Running the Application

To start the server, run the following command:

```bash
poetry run python app.py
```

The server will start on `http://localhost:8000`. You can access the endpoints `/stats` for altitude statistics and `/health` for the health status of the satellite.

### Endpoints

- `/stats`: Returns the minimum, maximum, and average altitude of the satellite for the last 5 minutes.
- `/health`: Checks the average altitude of the satellite for the last minute and returns a health status.

### Testing

To run the unit tests for the application, use the following command:
```bash
poetry run python -m unittest
```

This will execute all the tests defined in the `test_app.py` file.
