# Utiliser une image Python comme base
FROM python:3.10-slim

# Installer les outils nécessaires au système
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans le conteneur
COPY . .

# Exposer le port de l'application
EXPOSE 8000

# Démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
