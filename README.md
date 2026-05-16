# EVAT SmartCharge AI Backend API

**Author:** Ngoc Phuong Van Nguyen  
**Student ID:** 225550064  
**Unit:** SIT753 / SIT223  
**Task:** 7.3HD DevOps Pipeline with Jenkins  

EVAT SmartCharge AI Backend API is a Python FastAPI backend service designed for EV charging recommendation. The project is developed for the SIT753 High Distinction Jenkins DevOps Pipeline task.

This project is backend-only, but it is suitable for a complete DevOps pipeline because it includes testable backend logic, multiple API endpoints, Docker containerisation, automated testing, code quality analysis, security scanning, staging deployment, production release, and monitoring.

---

## 1. Project Overview

The purpose of this project is to provide an API service that helps electric vehicle users identify suitable charging stations based on simple decision factors such as:

- Distance to the charger
- Charger availability
- Congestion level
- Charger capacity

The backend exposes API endpoints for charger listing, recommendation, congestion prediction, health checking, and Prometheus metrics.

The project demonstrates a complete Jenkins CI/CD pipeline with all seven required stages:

1. Build
2. Test
3. Code Quality
4. Security
5. Deploy
6. Release
7. Monitoring

---

## 2. Technologies Used

| Area | Technology |
|---|---|
| Backend framework | FastAPI |
| Programming language | Python |
| Testing | Pytest |
| Code coverage | Pytest-cov |
| Containerisation | Docker |
| Local orchestration | Docker Compose |
| CI/CD | Jenkins |
| Code quality | SonarCloud |
| Source code security | Bandit |
| Image vulnerability scanning | Trivy |
| Monitoring | Prometheus |
| Dashboard | Grafana |
| Alerting | Alertmanager |
| Version control | GitHub |

---

## 3. Project Structure

    evat-smartcharge-ai-backend/
    │
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   └── recommender.py
    │
    ├── tests/
    │   ├── test_health.py
    │   ├── test_recommender.py
    │   └── test_api_integration.py
    │
    ├── monitoring/
    │   ├── prometheus.yml
    │   ├── alert-rules.yml
    │   └── alertmanager.yml
    │
    ├── reports/
    │   └── .gitkeep
    │
    ├── Dockerfile
    ├── Jenkinsfile
    ├── docker-compose.staging.yml
    ├── docker-compose.prod.yml
    ├── requirements.txt
    ├── pytest.ini
    ├── sonar-project.properties
    ├── README.md
    └── .gitignore

### Folder and File Description

| Path | Description |
|---|---|
| `app/` | Main FastAPI backend application |
| `app/main.py` | Defines API routes, health check, metrics endpoint, and request tracking |
| `app/recommender.py` | Contains EV charger recommendation and congestion prediction logic |
| `tests/` | Contains automated unit and integration tests |
| `monitoring/` | Contains Prometheus, alert rule, and Alertmanager configuration |
| `reports/` | Stores generated Jenkins reports such as Pytest, coverage, Bandit, and Trivy outputs |
| `Dockerfile` | Defines how the backend application is built into a Docker image |
| `Jenkinsfile` | Defines the complete CI/CD pipeline |
| `docker-compose.staging.yml` | Deploys the application to a staging container |
| `docker-compose.prod.yml` | Deploys the production application with Prometheus, Grafana, and Alertmanager |
| `requirements.txt` | Python dependency list |
| `pytest.ini` | Pytest configuration |
| `sonar-project.properties` | SonarCloud project configuration |
| `.gitignore` | Excludes virtual environments, reports, cache files, and local artefacts |

---

## 4. API Documentation

FastAPI automatically provides interactive API documentation.

When running the application locally with Uvicorn, open:

    http://localhost:8000/docs

When running the production Docker Compose environment, open:

    http://localhost:8082/docs

---

## 5. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root endpoint that returns a welcome message |
| `GET` | `/health` | Health check endpoint used by Docker and Jenkins smoke tests |
| `GET` | `/chargers` | Returns a list of sample EV charging stations |
| `GET` | `/recommend` | Returns an EV charger recommendation based on distance, availability, and congestion |
| `GET` | `/predict-congestion` | Predicts charger congestion level based on usage and capacity |
| `GET` | `/metrics` | Exposes Prometheus metrics |
| `GET` | `/docs` | Opens FastAPI Swagger documentation |

---

## 6. Example API Requests

### 6.1 Root Endpoint

    GET http://localhost:8000/

Example response:

    {
      "message": "Welcome to EVAT SmartCharge AI Backend API",
      "version": "1.0.0",
      "docs": "/docs"
    }

---

### 6.2 Health Check

    GET http://localhost:8000/health

Example response:

    {
      "status": "healthy",
      "service": "EVAT SmartCharge AI Backend API"
    }

---

### 6.3 Charger List

    GET http://localhost:8000/chargers

Example response:

    {
      "chargers": [
        {
          "id": 1,
          "name": "Melbourne Central EV Charger",
          "location": "Melbourne CBD",
          "available_ports": 4,
          "charger_type": "Fast Charger"
        },
        {
          "id": 2,
          "name": "Docklands EV Station",
          "location": "Docklands",
          "available_ports": 2,
          "charger_type": "Standard Charger"
        },
        {
          "id": 3,
          "name": "Southbank EV Hub",
          "location": "Southbank",
          "available_ports": 6,
          "charger_type": "Ultra-fast Charger"
        }
      ]
    }

---

### 6.4 EV Charger Recommendation

    GET http://localhost:8000/recommend?distance_km=2&availability=5&congestion=0.2

Parameters:

| Parameter | Type | Description |
|---|---|---|
| `distance_km` | float | Distance from user to charger in kilometres |
| `availability` | integer | Number of available charging ports |
| `congestion` | float | Congestion level between `0` and `1` |

Example response:

    {
      "distance_km": 2.0,
      "availability": 5,
      "congestion": 0.2,
      "score": 43.0,
      "recommendation": "Highly recommended"
    }

---

### 6.5 Congestion Prediction

    GET http://localhost:8000/predict-congestion?current_usage=8&charger_capacity=10

Parameters:

| Parameter | Type | Description |
|---|---|---|
| `current_usage` | integer | Number of charging ports currently in use |
| `charger_capacity` | integer | Total charger capacity |

Example response:

    {
      "current_usage": 8,
      "charger_capacity": 10,
      "congestion_rate": 0.8,
      "congestion_level": "High"
    }

---

### 6.6 Prometheus Metrics

    GET http://localhost:8000/metrics

This endpoint exposes Prometheus-compatible metrics, including request count and request latency.

Example metric names:

    evat_request_total
    evat_request_latency_seconds

---

## 7. Jenkins Pipeline Stages

The Jenkins pipeline is defined in the `Jenkinsfile`. It implements all seven required DevOps stages.

    GitHub main branch
            ↓
    Jenkins Checkout
            ↓
    Build
            ↓
    Test
            ↓
    Code Quality
            ↓
    Security
            ↓
    Deploy to Staging
            ↓
    Release to Production
            ↓
    Monitoring and Alerting

---

### 7.1 Build Stage

The Build stage creates a Docker image artefact for the backend API.

Main actions:

- Checks out the latest code from GitHub
- Generates a version number using the Jenkins build number and Git commit hash
- Builds a Docker image
- Tags the image with both a version tag and `latest`
- Archives key pipeline artefacts

Example image tag:

    evat-smartcharge-ai-backend:1.0.9-674754b

---

### 7.2 Test Stage

The Test stage runs automated tests using Pytest.

Main actions:

- Creates a Python virtual environment
- Installs dependencies from `requirements.txt`
- Runs unit and integration tests
- Generates a JUnit XML test report
- Generates a code coverage report

Generated reports:

    reports/pytest-report.xml
    reports/coverage.xml

---

### 7.3 Code Quality Stage

The Code Quality stage uses SonarCloud.

Main actions:

- Downloads Sonar Scanner inside the Jenkins pipeline
- Sends source code and coverage report to SonarCloud
- Analyses code smells, maintainability, duplication, reliability, and coverage
- Shows the result in the SonarCloud dashboard

Important note:

SonarCloud Automatic Analysis should be disabled for this project because Jenkins performs CI-based analysis.

---

### 7.4 Security Stage

The Security stage performs automated security analysis.

Tools used:

| Tool | Purpose |
|---|---|
| Bandit | Scans Python source code for security issues |
| Trivy | Scans Docker image dependencies for HIGH and CRITICAL vulnerabilities |

Generated reports:

    reports/bandit-report.json
    reports/trivy-image-report.txt

For the assignment demonstration, the security report can be generated without blocking later stages. In a production environment, Trivy can be configured with `--exit-code 1` to stop the pipeline when unresolved HIGH or CRITICAL vulnerabilities are detected.

---

### 7.5 Deploy Stage

The Deploy stage deploys the validated Docker image to the staging environment.

Main actions:

- Uses `docker-compose.staging.yml`
- Starts the staging container
- Runs a smoke test against `/health`

Staging URL:

    http://localhost:8081/health

---

### 7.6 Release Stage

The Release stage promotes the validated image to the production environment.

Main actions:

- Uses `docker-compose.prod.yml`
- Starts the production container
- Runs a production health check
- Creates a local Git tag for traceability

Production URL:

    http://localhost:8082/health

Port `8082` is used for the production backend because Jenkins normally runs on port `8080`.

---

### 7.7 Monitoring Stage

The Monitoring stage validates that the production application is observable.

Main actions:

- Checks the production `/health` endpoint
- Checks the production `/metrics` endpoint
- Checks Prometheus readiness
- Checks Alertmanager readiness
- Optionally runs an incident simulation

Monitoring services:

| Service | URL |
|---|---|
| Production API | `http://localhost:8082/health` |
| Metrics endpoint | `http://localhost:8082/metrics` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |
| Alertmanager | `http://localhost:9093` |

---

## 8. Setup Instructions

### 8.1 Prerequisites

Install the following tools:

| Tool | Purpose |
|---|---|
| Git | Clone and push the repository |
| Python 3 | Run the backend and tests |
| Docker Desktop | Build and run containers |
| Jenkins | Run the CI/CD pipeline |
| ngrok | Optional, used for GitHub webhook testing with local Jenkins |

Check installed tools:

    git --version
    python3 --version
    docker --version
    docker compose version
    curl --version

---

### 8.2 Clone Repository

    git clone https://github.com/YOUR_USERNAME/evat-smartcharge-ai-backend.git
    cd evat-smartcharge-ai-backend

---

### 8.3 Run Backend Locally

Create virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install --upgrade pip
    pip install -r requirements.txt

Run tests:

    PYTHONPATH=. pytest tests/

Run the app:

    uvicorn app.main:app --reload

Open:

    http://localhost:8000/health

---

### 8.4 Run with Docker

Build image:

    docker build --no-cache -t evat-smartcharge-ai-backend:local .

Run container:

    docker run --name evat-test -p 8000:8000 evat-smartcharge-ai-backend:local

Open:

    http://localhost:8000/health

Stop container:

    docker stop evat-test
    docker rm evat-test

---

### 8.5 Run Staging Environment

    export IMAGE_TAG=evat-smartcharge-ai-backend:local
    docker compose -f docker-compose.staging.yml up -d

Open:

    http://localhost:8081/health

Stop staging:

    docker compose -f docker-compose.staging.yml down

---

### 8.6 Run Production Environment with Monitoring

    export IMAGE_TAG=evat-smartcharge-ai-backend:local
    docker compose -f docker-compose.prod.yml up -d

Open:

    Production API:  http://localhost:8082/health
    Metrics:         http://localhost:8082/metrics
    Prometheus:      http://localhost:9090
    Grafana:         http://localhost:3000
    Alertmanager:    http://localhost:9093

Default Grafana login:

    Username: admin
    Password: admin

Stop production:

    docker compose -f docker-compose.prod.yml down

---

## 9. Demo URLs

| Environment | URL |
|---|---|
| Local Uvicorn | `http://localhost:8000` |
| Staging | `http://localhost:8081` |
| Production | `http://localhost:8082` |
| Jenkins | `http://localhost:8080` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |
| Alertmanager | `http://localhost:9093` |
