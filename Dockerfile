# Utiliser une image Python officielle comme image de base
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . /app/

# Exposer le port de l'application
EXPOSE 8000

# Définir la commande de démarrage par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tricount.wsgi:application"]
