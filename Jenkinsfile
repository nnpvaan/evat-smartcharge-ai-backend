pipeline {
    agent any

    options {
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    parameters {
        booleanParam(
            name: 'RUN_INCIDENT_SIMULATION',
            defaultValue: false,
            description: 'Trigger a monitoring alert simulation after production release'
        )
    }

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"

        APP_NAME = 'evat-smartcharge-ai-backend'
        IMAGE_NAME = "${APP_NAME}"

        STAGING_COMPOSE = 'docker-compose.staging.yml'
        PROD_COMPOSE = 'docker-compose.prod.yml'

        SONAR_PROJECT_KEY = 'nnpvaan_evat-smartcharge-ai-backend'
        SONAR_ORGANIZATION = 'nnpvaan'
        SONAR_HOST_URL = 'https://sonarcloud.io'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                script {
                    env.GIT_SHORT_COMMIT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()

                    env.VERSION = "1.0.${BUILD_NUMBER}-${GIT_SHORT_COMMIT}"
                    env.IMAGE_TAG = "${IMAGE_NAME}:${VERSION}"
                    env.LATEST_TAG = "${IMAGE_NAME}:latest"
                }

                echo "Checked out source code"
                echo "Build version: ${VERSION}"
                echo "Docker image: ${IMAGE_TAG}"
            }
        }

        stage('Build') {
            steps {
                echo "Building local Docker image artefact..."

                sh """
                    docker build \
                      --build-arg APP_VERSION=${VERSION} \
                      -t ${IMAGE_TAG} \
                      -t ${LATEST_TAG} .
                """

                sh "docker image inspect ${IMAGE_TAG}"

                archiveArtifacts(
                    artifacts: 'Dockerfile,docker-compose*.yml,Jenkinsfile',
                    fingerprint: true
                )

                echo "Build completed successfully: ${IMAGE_TAG}"
            }
        }

        stage('Test') {
            steps {
                echo "Running unit and integration tests..."

                sh """
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov

                    mkdir -p reports

                    PYTHONPATH=. pytest tests/ \
                      --junitxml=reports/pytest-report.xml \
                      --cov=app \
                      --cov-report=xml:reports/coverage.xml \
                      --cov-report=term
                """
            }

            post {
                always {
                    junit 'reports/pytest-report.xml'
                    archiveArtifacts artifacts: 'reports/coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo "Running SonarCloud code quality analysis..."
                withCredentials([string(credentialsId: 'sonarcloud-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-6.2.1.4610-macosx-aarch64.zip
                        unzip -o sonar-scanner.zip
                        ./sonar-scanner-6.2.1.4610-macosx-aarch64/bin/sonar-scanner -Dsonar.token=$SONAR_TOKEN
                    '''
                }

                echo "SonarCloud analysis completed successfully."
            }
        }

        stage('Security') {
            steps {
                echo "Running source code and Docker image security scans..."

                sh '''
                    mkdir -p reports

                    python3 -m venv security-venv
                    . security-venv/bin/activate

                    pip install --upgrade pip
                    pip install bandit

                    bandit -r app \
                    -f json \
                    -o reports/bandit-report.json \
                    || true
                '''

                sh '''
                    rm -rf trivy trivy.tar.gz

                    curl -sSLo trivy.tar.gz https://github.com/aquasecurity/trivy/releases/download/v0.69.3/trivy_0.69.3_macOS-ARM64.tar.gz

                    tar -xzf trivy.tar.gz

                    ./trivy image \
                    --severity HIGH,CRITICAL \
                    --scanners vuln \
                    --skip-version-check \
                    --format table \
                    --output reports/trivy-image-report.txt \
                    ${IMAGE_TAG}

                    echo "===== Trivy Image Scan Report ====="
                    cat reports/trivy-image-report.txt
                '''
            }

            post {
                always {
                    archiveArtifacts artifacts: 'reports/bandit-report.json,reports/trivy-image-report.txt', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying validated image to local staging environment..."

                sh """
                    export IMAGE_TAG=${IMAGE_TAG}
                    docker compose -f ${STAGING_COMPOSE} down || true
                    docker compose -f ${STAGING_COMPOSE} up -d
                """

                echo "Running staging smoke test..."

                sh """
                    sleep 10
                    curl --fail --retry 5 --retry-delay 5 http://localhost:8081/health
                """

                echo "Staging deployment verified successfully."
            }
        }

        stage('Release') {
            steps {
                echo "Promoting validated local Docker image to production..."

                sh """
                    export IMAGE_TAG=${IMAGE_TAG}
                    docker compose -f ${PROD_COMPOSE} down || true
                    docker compose -f ${PROD_COMPOSE} up -d
                """

                echo "Running production health check..."

                sh """
                    sleep 10
                    curl --fail --retry 5 --retry-delay 5 http://localhost:8082/health
                """

                sh """
                    git config user.email "jenkins@evat.local"
                    git config user.name "Jenkins CI"

                    git tag -a v${VERSION} -m "Local release v${VERSION}" || true
                """

                echo "Local production release completed successfully: v${VERSION}"
            }
        }

        stage('Monitoring') {
            steps {
                echo "Validating production monitoring and alerting..."

                sh """
                    curl --fail http://localhost:8082/health
                    curl --fail http://localhost:8082/metrics
                    curl --fail http://localhost:9090/-/ready || true
                    curl --fail http://localhost:9093/-/ready || true
                """

                script {
                    if (params.RUN_INCIDENT_SIMULATION) {
                        echo "Running incident simulation for alert validation..."

                        sh """
                            docker stop evat-smartcharge-prod || true
                            sleep 20
                            docker start evat-smartcharge-prod || true
                            sleep 10
                            curl --fail --retry 5 --retry-delay 5 http://localhost:8082/health
                        """
                    } else {
                        echo "Incident simulation skipped. Enable RUN_INCIDENT_SIMULATION to test alerts."
                    }
                }

                echo "Monitoring validation completed."
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. All 7 stages passed with full automation."
        }

        failure {
            echo "Pipeline failed. Deployment or release has been blocked to protect application quality."
        }

        always {
            sh """
                docker ps || true
                docker images | grep ${APP_NAME} || true
            """

            echo "Workspace cleanup skipped to keep local Docker Compose monitoring files available."
        }
    }
}
