# Utiliser une image Python comme base
FROM python:3.10-slim

# Installer les outils nécessaires au système
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans le conteneur
COPY . .

# Vérification : lister les fichiers dans le répertoire de travail pour s'assurer que 'manage.py' est présent
RUN ls -l /app

# Exposer le port de l'application
EXPOSE 8000

# Donner les permissions appropriées au fichier manage.py
RUN chmod +x /app/manage.py

# Démarrer le serveur Django (avec l'adresse IP 0.0.0.0 et le port 8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

