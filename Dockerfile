# Utiliser l'image officielle de Python 3.10
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . /app/

# Exposer le port sur lequel l'application va fonctionner
EXPOSE 8000

# Définir la commande pour exécuter l'application avec gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tricount.wsgi:application"]
