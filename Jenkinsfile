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
        stage('Setup Environment') {
            steps {
                script {
                    sh 'make setup'  // Crée l'environnement virtuel et installe les dépendances
                }
            }
        }

        stage('Verify Code Quality') {
            steps {
                script {
                    sh 'make verify'  // Vérification du code avec Black et Pylint
                }
            }
        }

        stage('Prepare Data') {
            steps {
                script {
                    sh 'make prepare'  // Préparation des données
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    sh 'make train'  // Entraînement du modèle
                }
            }
        }

        stage('Evaluate Model') {
            steps {
                script {
                    sh 'make evaluate'  // Évaluation du modèle
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh 'make test'  // Exécution des tests unitaires
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'make build_docker'  // Construction de l'image Docker
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh 'make docker_login'  // Connexion à Docker Hub
                    sh 'docker push ${IMAGE_NAME}:${TAG}'  // Pousser l'image Docker
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh 'make run_docker'  // Exécution du conteneur Docker
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh 'make deploy'  // Déploiement complet de l'application avec Docker
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up after pipeline...'
            sh 'make clean'  // Nettoyage après exécution
        }

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}

