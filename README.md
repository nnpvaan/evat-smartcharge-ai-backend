# EVAT SmartCharge AI Backend API

EVAT SmartCharge AI Backend API is a Python FastAPI backend service designed for EV charging recommendation.

The application provides API endpoints for health checking, charger recommendation, congestion prediction, and Prometheus monitoring metrics.

This repository is used for the SIT753 High Distinction DevOps Pipeline with Jenkins task.

## Technologies Used

- Python
- FastAPI
- Pytest
- Docker
- Jenkins
- SonarQube
- Bandit
- Trivy
- Docker Compose
- Prometheus
- Grafana
- Alertmanager

## Pipeline Stages

The Jenkins pipeline includes all seven required stages:

1. Build
2. Test
3. Code Quality
4. Security
5. Deploy
6. Release
7. Monitoring

## API Endpoints

| Endpoint | Description |
|---|---|
| `/health` | Checks whether the backend service is running |
| `/recommend` | Returns an EV charger recommendation |
| `/metrics` | Exposes Prometheus metrics |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload