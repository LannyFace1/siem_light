# Base Image 
FROM python:3.10-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# non root user erstellen, Datenordner anlegen und Berechtigungen setzen
RUN useradd -m appuser && mkdir -p /app/data && chown -R appuser:appuser /app/data
USER appuser

# Port freigeben
EXPOSE 5000

# Healthcheck hinzufügen
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Startbefehl
CMD ["python", "main.py"]
