# Utiliser une version stable de Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers du projet
COPY . /app

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer les dépendances sans sqlite3
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de FastAPI
EXPOSE 8000

# Démarrer l'API FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

