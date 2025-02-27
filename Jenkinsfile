kkpipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'amenamaktouf/maktouf_amena_4ds5_mlops'
        IMAGE_NAME = 'amenamaktouf/maktouf_amena_4ds5_mlops'
        TAG = 'v1'
        CONTAINER_NAME = 'mlops_container'
    }
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    echo 'Cloning GitHub Repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-git-token', url: 'https://github.com/iQuantC/MLOps01.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setting up the virtual environment...'
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip install --upgrade pip'
                    sh './venv/bin/pip install -r requirements.txt'
                    echo 'Virtual environment setup completed!'
                }
            }
        }

        stage('Lint Code') {
            steps {
                script {
                    echo 'Linting Python Code...'
                    sh './venv/bin/python -m black --exclude "venv|mlops_env" .'
                    sh './venv/bin/python -m pylint --disable=C,R model_pipeline.py || true'
                    echo 'Code linted successfully!'
                }
            }
        }

        stage('Test Code') {
            steps {
                script {
                    echo 'Running Unit Tests...'
                    sh './venv/bin/python -m pytest tests/'
                    echo 'Tests completed successfully!'
                }
            }
        }

        stage('Prepare Data') {
            steps {
                script {
                    echo 'Preparing data...'
                    sh './venv/bin/python model_pipeline.py --prepare'
                    echo 'Data prepared successfully!'
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    echo 'Training model...'
                    sh './venv/bin/python model_pipeline.py --train'
                    echo 'Model trained successfully!'
                }
            }
        }

        stage('Evaluate Model') {
            steps {
                script {
                    echo 'Evaluating model...'
                    sh './venv/bin/python model_pipeline.py --evaluate'
                    echo 'Model evaluation completed!'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t ${IMAGE_NAME}:${TAG} .'
                    echo 'Docker image built successfully!'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        sh 'docker push ${IMAGE_NAME}:${TAG}'
                    }
                    echo 'Docker image pushed to DockerHub successfully!'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying to production...'
                    sh 'aws ecs update-service --cluster iquant-ecs --service iquant-ecs-svc --force-new-deployment'
                    echo 'Deployment completed successfully!'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo 'Cleaning up...'
                    sh 'rm -rf venv'
                    echo 'Clean up completed!'
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for errors.'
        }
    }
}

