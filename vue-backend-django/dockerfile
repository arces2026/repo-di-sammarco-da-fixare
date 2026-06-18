# Usa l'immagine di base ufficiale di Python 3.12 in versione "slim" (più leggera)
FROM python:3.12-slim

# Impedisce a Python di scrivere file .pyc (bytecode) sul disco
ENV PYTHONDONTWRITEBYTECODE=1
# Assicura che i log di Python vengano inviati direttamente al terminale senza buffering
ENV PYTHONUNBUFFERED=1

# Imposta la directory di lavoro all'interno del container come /app
WORKDIR /app

# Copia il file dei requisiti dal tuo computer locale alla directory corrente del container
COPY requirements.txt .

# Installa le dipendenze Python elencate nel file, evitando di memorizzare la cache locale
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutti i restanti file del progetto dal tuo computer locale al container
COPY . .

# Indica a Docker che il container sarà in ascolto sulla porta 8000
EXPOSE 8000

# Definisce il comando predefinito per avviare il server di sviluppo Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]