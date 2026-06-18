# 🚀 Progetto Integrato: Vue + Django

Questa è la documentazione principale per il progetto che combina un frontend **Vue.js** e un backend **Django REST Framework**, orchestrati tramite **Docker**.

## 📋 Indice

* [Struttura del Progetto](#-struttura-del-progetto)
* [Installazione e Avvio](#-installazione-e-avvio-con-docker)
* [Comandi Docker Utili](#comandi-docker-utili)
* [Debug e Troubleshooting](#-debug-e-troubleshooting)

---

## 📁 Struttura del Progetto

```text
VUE-DJANGO-FOLDER/
├── django-backend/      # Backend Django (API)
├── vue-frontend/        # Frontend Vue.js (Vite)
├── docker-compose.yml   # Orchestrazione dei container
└── .env                 # Variabili d'ambiente (DB, ecc.)

```

[↑ torna su](#-indice)

## 🐳 Installazione e Avvio con Docker

### 1. Clona il Repository

```bash
git clone <url-del-repository>
cd MONO-REPO-DJANGO-VUE
```

### 2. Configura le Variabili d'Ambiente

Crea un file `.env` nella **root del progetto** (dove si trova `docker-compose.yml`):

```bash
# .env
# Configurazione Database
DB_HOST=db
DB_PORT=3306
DB_NAME=vue_django
DB_USER=root
DB_PASSWORD=********

# Configurazione MariaDB
MARIADB_ROOT_PASSWORD=********
```

> **⚠️ IMPORTANTE**: Sostituisci `********` con una password sicura per l'ambiente di produzione. Il file `.env` NON deve essere committato nel repository (aggiungilo al `.gitignore`).

### 3. Costruisci e Avvia i Container

```bash
# Costruisci le immagini e avvia i container in background
docker-compose up -d --build

# Verifica che i container siano in esecuzione
docker ps
```

Dovresti vedere tre container attivi:

- `django-backend` - Django application (porta 8000)
- `mariadb` - Database MariaDB (porta 3306)
- `vue-frontend` - Vue application (porta 8080)

### 4. Applica le Migrazioni del Database

```bash
# Applica le migrazioni per creare le tabelle nel database
docker exec -it django-backend python manage.py migrate
```

### 5. Crea un Superutente (Admin)

```bash
# Crea un account amministratore per l'admin panel
docker exec -it django-backend python manage.py createsuperuser
```

Segui le istruzioni per inserire:
- **Username**: `admin` (o quello che preferisci)
- **Email**: `admin@example.com`
- **Password**: `admin123` (o una password sicura)

### 6. Verifica che tutto funzioni

Apri il browser e visita:
- **Vue Home**: http://localhost:8080
- **Admin Panel**: http://localhost:8000/admin/
- **API Books**: http://localhost:8000/api/libri/
- **API Authors**: http://localhost:8000/api/autori/
- **Register**: http://localhost:8000/api/register/

---
[↑ torna su](#-indice)
<a id='comandi-docker-utili'><a>

## 🛠️ Comandi Docker Utili

### Gestione dei Container

```bash
# Visualizza i container in esecuzione
docker ps

# Visualizza tutti i container (anche fermati)
docker ps -a

# Ferma i container (senza rimuoverli)
docker-compose stop

# Avvia i container fermati
docker-compose start

# Riavvia i container
docker-compose restart

# Ferma e rimuove i container (i volumi persistono)
docker-compose down

# Ferma, rimuove container e volumi (PERDE I DATI!)
docker-compose down -v
```

### Visualizzazione dei Log

```bash
# Visualizza i log del backend (in tempo reale)
docker logs -f django-backend

# Visualizza i log del database
docker logs -f mariadb

# Visualizza gli ultimi 100 log del backend
docker logs --tail 100 django-backend
```

### Comandi Django

```bash
# Entra nella shell del container
docker exec -it django-backend /bin/bash

# Esegui comandi Django senza entrare nel container
docker exec -it django-backend python manage.py <comando>

# Esempi:
docker exec -it django-backend python manage.py makemigrations
docker exec -it django-backend python manage.py migrate
docker exec -it django-backend python manage.py createsuperuser
docker exec -it django-backend python manage.py shell
```

### Riavvio dopo Modifiche al Codice

Il container è configurato con **hot-reload** grazie al volume montato (`./django-backend:/app`). Le modifiche al codice vengono rilevate automaticamente, ma in caso di problemi:

```bash
# Riavvia solo il backend
docker-compose restart web

# Oppure ricostruisci tutto
docker-compose up -d --build
```

[↑ Torna su](#-indice)

## 🔍 Debug e Troubleshooting

### Controllare i log in caso di errore

Se l'app non risponde, usa questi comandi per leggere i log in tempo reale:

* **Per il Backend**: `docker-compose logs -f backend`
* **Per il Frontend**: `docker-compose logs -f frontend`

### Entrare nei container (Shell)

Se hai bisogno di eseguire comandi all'interno dei container per debuggare:

* **Backend**: `docker-compose exec backend bash`
* **Frontend**: `docker-compose exec frontend sh`

### Errori Comuni

* **Porta occupata**: Se `8000` o `8080` sono occupate, controlla i processi attivi sul tuo PC (`netstat -ano | findstr :8000`).
* **Database non connesso**: Verifica che il container `mariadb` sia attivo (`docker-compose ps`) e che le variabili nel `.env` corrispondano a quelle in `settings.py`.
* **CORS**: Se il frontend non comunica col backend, verifica in `django-backend/bookshelf/settings.py` che `CORS_ALLOWED_ORIGINS` includa l'URL del frontend.

---
[↑ Torna su](#-indice)
