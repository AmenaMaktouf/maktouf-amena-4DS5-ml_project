# Déclaration des variables
PYTHON=python3
ENV_NAME=venv
REQUIREMENTS=requirements.txt
SOURCE_DIR=model_pipeline.py
MAIN_SCRIPT=main.py
TEST_DIR=tests/

# Nom de l'image Docker et tag
IMAGE_NAME=amenamaktouf/maktouf_amena_4ds5_mlops
TAG=v1
CONTAINER_NAME=mlops_container

# Configuration de l'environnement virtuel
setup:
	@echo "Création de l'environnement virtuel et installation des dépendances..."
	@$(PYTHON) -m venv $(ENV_NAME)
	@./$(ENV_NAME)/bin/python3 -m pip install --upgrade pip
	@./$(ENV_NAME)/bin/python3 -m pip install -r $(REQUIREMENTS)
	@echo "Environnement configuré avec succès !"

# Vérification du code avec Black et Pylint
verify:
	@echo "Vérification de la qualité du code..."
	@. $(ENV_NAME)/bin/activate && $(PYTHON) -m black --exclude 'venv|mlops_env' .
	@. $(ENV_NAME)/bin/activate && $(PYTHON) -m pylint --disable=C,R $(SOURCE_DIR) || true
	@echo "Code vérifié avec succès !"

# Préparation des données
prepare:
	@echo "Préparation des données..."
	@./$(ENV_NAME)/bin/python3 $(MAIN_SCRIPT) --prepare
	@echo "Données préparées avec succès !"

# Entraînement du modèle
train:
	@echo "Entraînement du modèle..."
	@./$(ENV_NAME)/bin/python3 $(MAIN_SCRIPT) --train
	@echo "Modèle entraîné avec succès !"

# Évaluation du modèle
evaluate:
	@echo "Évaluation du modèle..."
	@./$(ENV_NAME)/bin/python3 $(MAIN_SCRIPT) --evaluate
	@echo "Évaluation terminée !"

# Exécution des tests
test:
	@echo "Exécution des tests unitaires..."
	@. $(ENV_NAME)/bin/activate && pytest $(TEST_DIR)
	@echo "Tests terminés avec succès !"

# Nettoyage des fichiers temporaires et environnement
clean:
	@echo "Suppression des fichiers temporaires..."
	rm -rf $(ENV_NAME)
	rm -f model.pkl scaler.pkl pca.pkl
	rm -rf __pycache__ .pytest_cache .pylint.d
	@echo "Nettoyage terminé !"

# Réinstallation complète de l'environnement
reinstall: clean setup

# Pipeline complet
all: setup verify prepare train test evaluate build_docker test push_docker
	@echo "Pipeline MLOps exécuté avec succès !"

# Exécuter le conteneur Docker
run_docker:
	@echo "Démarrage du conteneur Docker..."
	@docker run -d -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME):$(TAG)
	@echo "Conteneur démarré avec succès !"

# Arrêter et supprimer le conteneur Docker
stop_docker:
	@echo "Arrêt du conteneur Docker..."
	@docker stop $(CONTAINER_NAME) || true
	@docker rm $(CONTAINER_NAME) || true
	@echo "Conteneur supprimé !"

### ---- Gestion de Docker ---- ###

# Construire l'image Docker
build_docker:
	@echo "Construction de l'image Docker..."
	@docker build -t $(IMAGE_NAME):$(TAG) .
	@echo "Image Docker construite avec succès !"

# Taguer l'image Docker (optionnel si build déjà fait)
tag_docker:
	@echo "Tag de l'image Docker..."
	@docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):latest
	@echo "Tagging terminé !"

# Se connecter à Docker Hub
docker_login:
	@echo "Connexion à Docker Hub..."
	@docker login
	@echo "Connexion réussie !"

# Pousser l'image sur Docker Hub
run_docker:
	@echo "Démarrage du conteneur Docker..."
	@docker run -d -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME):$(TAG)
	@echo "Conteneur démarré avec succès !"

# Arrêter et supprimer le conteneur Docker
stop_docker:
	@echo "Arrêt du conteneur Docker..."
	@docker stop $(CONTAINER_NAME) || true
	@docker rm $(CONTAINER_NAME) || true
	@echo "Conteneur supprimé !"

# Pipeline complet avec Docker
deploy: build_docker push_docker run_docker
	@echo "Déploiement complet effectué !"

