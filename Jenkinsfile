pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        ENV_NAME = 'venv'
        REQUIREMENTS = 'requirements.txt'
        IMAGE_NAME = 'amenamaktouf/maktouf_amena_4ds5_mlops'
        TAG = 'v1'
        CONTAINER_NAME = 'mlops_container'
        MAIN_SCRIPT = 'main.py'
        TEST_DIR = 'tests/'
        SOURCE_DIR = 'model_pipeline.py'
    }

    stages {
        stage('Checkout Repository') {
            steps {
                script {
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-git-token', url: 'https://github.com/AmenaMaktouf/maktouf-amena-4DS5-ml_project.git']])
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    sh 'make setup'
                }
            }
        }

        stage('Verify Code Quality') {
            steps {
                script {
                    sh 'make verify'
                }
            }
        }

        stage('Prepare Data') {
            steps {
                script {
                    sh 'make prepare'
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    sh 'make train'
                }
            }
        }

        stage('Evaluate Model') {
            steps {
                script {
                    sh 'make evaluate'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh 'make test'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'make build_docker'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh 'make docker_login'
                    sh 'docker push ${IMAGE_NAME}:${TAG}'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh 'make run_docker'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh 'make deploy'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up after pipeline...'
            sh 'make clean'
        }

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
