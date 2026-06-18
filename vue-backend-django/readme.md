# 📚 Bookshelf API - Django Backend

API REST per un sistema di gestione di una libreria con autenticazione JWT, containerizzata con Docker e MariaDB.

---

## 📋 Indice

- [Panoramica](#-panoramica)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Prerequisiti](#-prerequisiti)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Installazione e Avvio con Docker](#-installazione-e-avvio-con-docker)
- [Comandi Utili Docker](#comandi-utili-docker)
- [Gestione del Database](#gestione-del-database)
- [Autenticazione JWT](#autenticazione-jwt)
- [Endpoints API](#-endpoints-api)
- [Testing](#-testing)
- [Sviluppo Senza Docker](#sviluppo-senza-docker)
- [Risoluzione dei Problemi](#-risoluzione-dei-problemi)

---
[↑ torna su](#-indice)

## 🎯 Panoramica

**Bookshelf API** è un backend RESTful sviluppato con Django REST Framework per la gestione di una libreria. Il sistema permette di:

- Gestire **libri** e **autori** (CRUD completo)
- Registrare e autenticare **utenti** con JWT (JSON Web Tokens)
- Definire **permessi differenziati** per utenti autenticati e amministratori

L'architettura è completamente **containerizzata con Docker**, garantendo riproducibilità e facilità di deployment.

---
[↑ torna su](#-indice)

## Tecnologie Utilizzate

### Backend Framework
| Tecnologia | Versione | Scopo |
|------------|----------|-------|
| **Django** | 6.0.5 | Framework web principale |
| **Django REST Framework** | 3.17.1 | Creazione dell'API REST |
| **djangorestframework-simplejwt** | 5.5.1 | Autenticazione JWT |
| **django-cors-headers** | 4.9.0 | Gestione CORS per il frontend Vue |

### Database
| Tecnologia | Versione | Scopo |
|------------|----------|-------|
| **MariaDB** | 11 | Database relazionale (alternativa a MySQL) |
| **PyMySQL** | 1.2.0 | Driver per la connessione Python-MariaDB |

### Containerizzazione
| Tecnologia | Scopo |
|------------|-------|
| **Docker** | Containerizzazione dell'applicazione |
| **Docker Compose** | Orchestrazione dei container (backend + database) |

### Perché Queste Scelte?

- **Django + DRF**: Framework maturo con sistema di autenticazione integrato, admin panel e ORM potente. DRF semplifica la creazione di API RESTful.
- **MariaDB**: Database open-source, performante e compatibile con MySQL. Scelto per la sua affidabilità e facilità di integrazione con Docker.
- **JWT**: Autenticazione stateless ideale per API REST e integrazione con frontend moderni (Vue.js). I token JWT sono sicuri, auto-contenuti e non richiedono sessioni server-side.
- **Docker**: Isolamento dell'ambiente di sviluppo, eliminando il problema "funziona sulla mia macchina". Semplifica il deployment e garantisce che tutti gli sviluppatori lavorino con le stesse versioni delle dipendenze.
- **CORS**: Necessario per permettere al frontend Vue (in esecuzione su porta diversa) di comunicare con l'API.

---
[↑ torna su](#-indice)

## 📋 Prerequisiti

Prima di iniziare, assicurati di avere installato:

- **[Docker](https://www.docker.com/products/docker-desktop/)** (versione 24.0+)
- **[Docker Compose](https://docs.docker.com/compose/install/)** (versione 2.0+)
- **[Git](https://git-scm.com/downloads)** (per clonare il repository)
- **Python 3.12** (solo per sviluppo senza Docker)

---

## 📁 Struttura del Progetto

```
VUE-DJANGO-FOLDER/
│
├── django-backend/                    # Backend Django
│   ├── bookshelf/                     # Configurazione progetto Django
│   │   ├── __init__.py
│   │   ├── settings.py                # Settings principali
│   │   ├── urls.py                    # URL root del progetto
│   │   └── wsgi.py
│   │
│   ├── catalog/                       # Applicazione principale
│   │   ├── migrations/                # Migrazioni del database
│   │   ├── __init__.py
│   │   ├── admin.py                   # Configurazione admin panel
│   │   ├── models.py                  # Modelli: Libro, Autore, User
│   │   ├── serializers.py             # Serializer DRF
│   │   ├── urls.py                    # URL dell'applicazione
│   │   └── views.py                   # ViewSet e API views
│   │
│   ├── manage.py                      # Script di gestione Django
│   ├── requirements.txt               # Dipendenze Python
│   ├── dockerfile                     # Dockerfile per il backend
│   ├── wait-for-it.sh                 # Script di attesa per il database
│   └── db.sqlite3                     # Database SQLite (solo sviluppo locale)
│
├── vue-frontend/                      # Frontend Vue.js (progetto separato)
│
├── docker-compose.yml                 # Orchestrazione container Docker
├── .env                               # Variabili d'ambiente
└── README.md                          # Questo file
```

---
[↑ torna su](#-indice)

## 🐳 Installazione e Avvio con Docker

### 1. Clona il Repository

```bash
git clone <url-del-repository>
cd VUE-DJANGO-FOLDER
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
MYSQL_ROOT_PASSWORD=********
```

> **⚠️ IMPORTANTE**: Sostituisci `********` con una password sicura per l'ambiente di produzione. Il file `.env` NON deve essere committato nel repository (aggiungilo al `.gitignore`).

### 3. Costruisci e Avvia i Container

```bash
# Costruisci le immagini e avvia i container in background
docker-compose up -d --build

# Verifica che i container siano in esecuzione
docker ps
```

Dovresti vedere due container attivi:
- `django-backend` - Django application (porta 8000)
- `mariadb` - Database MariaDB (porta 3306)

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

- **Admin Panel**: http://localhost:8000/admin/
- **API Books**: http://localhost:8000/api/libri/
- **API Authors**: http://localhost:8000/api/autori/
- **Register**: http://localhost:8000/api/register/

---
[↑ torna su](#-indice)
<a id='comandi-utili-docker'><a>

## 🛠️ Comandi Utili Docker

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

---
[↑ torna su](#-indice)
<a id='gestione-del-database'><a>

## 🗄️ Gestione del Database

### Accesso diretto a MariaDB

```bash
# Connettiti al database tramite terminale
docker exec -it mariadb mysql -u root -p
# Inserisci la password: sciamano

# Una volta dentro MySQL:
USE vue_django;
SHOW TABLES;
SELECT * FROM auth_user;
SELECT * FROM catalog_libro;
SELECT * FROM catalog_autore;
```

### Backup del Database

```bash
# Crea un backup del database
docker exec mariadb mysqldump -u root -psciamano vue_django > backup_$(date +%Y%m%d).sql

# Backup di tutti i database
docker exec mariadb mysqldump -u root -psciamano --all-databases > backup_full.sql
```

### Ripristino del Database

```bash
# Ripristina da backup
cat backup.sql | docker exec -i mariadb mysql -u root -psciamano vue_django
```

### Migrazioni del Database

```bash
# Crea nuove migrazioni dopo aver modificato i modelli
docker exec -it django-backend python manage.py makemigrations

# Applica le migrazioni
docker exec -it django-backend python manage.py migrate

# Visualizza lo SQL generato da una migrazione
docker exec -it django-backend python manage.py sqlmigrate catalog 0001
```

---
[↑ torna su](#-indice)

## 🔐 Autenticazione JWT

L'API utilizza **JSON Web Tokens (JWT)** per l'autenticazione. Questo sistema è:

- **Stateless**: non richiede sessioni server-side
- **Sicuro**: i token sono firmati digitalmente
- **Scalabile**: perfetto per applicazioni distribuite

### Flusso di Autenticazione

1. **Registrazione** → Crea un nuovo utente
2. **Login** → Ricevi `access` token e `refresh` token
3. **Autenticazione** → Invia il token `access` nell'header delle richieste
4. **Refresh** → Usa il token `refresh` per ottenere un nuovo `access` token

### 1️⃣ Registrazione Nuovo Utente

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario_rossi",
    "password": "password123",
    "email": "mario@example.com"
  }'
```

**Risposta:**
```json
{
  "message": "User mario_rossi created successfully",
  "user_id": 2,
  "username": "mario_rossi"
}
```

### 2️⃣ Login - Ottenere i Token

```bash
curl -X POST http://localhost:8000/api/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario_rossi",
    "password": "password123"
  }'
```

**Risposta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs... (token di breve durata)",
  "refresh": "eyJhbGciOiJIUzI1NiIs... (token di lunga durata)"
}
```

### 3️⃣ Usare il Token per Richieste Autenticate

```bash
curl -X GET http://localhost:8000/api/profilo/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Risposta:**
```json
{
  "username": "mario_rossi",
  "user_id": 2
}
```

### 4️⃣ Refresh del Token

Quando il token `access` scade (dopo 60 minuti), usa il `refresh` token:

```bash
curl -X POST http://localhost:8000/api/token/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIs... (refresh token)"
  }'
```

**Risposta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs... (nuovo access token)"
}
```

---
[↑ torna su](#-indice)

## 📡 Endpoints API

### Endpoints Pubblici (Accesso Libero)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| **POST** | `/api/register/` | Registrazione nuovo utente |
| **POST** | `/api/token` | Login - ottenere JWT |
| **POST** | `/api/token/refresh` | Rinnovare JWT |
| **GET** | `/api/libri/` | Lista di tutti i libri |
| **GET** | `/api/libri/{id}/` | Dettaglio di un libro |
| **GET** | `/api/autori/` | Lista di tutti gli autori |
| **GET** | `/api/autori/{id}/` | Dettaglio di un autore |

### Endpoints Protetti (Autenticazione Richiesta)

| Metodo | Endpoint | Descrizione | Permesso |
|--------|----------|-------------|----------|
| **GET** | `/api/profilo/` | Profilo utente corrente | Utente autenticato |
| **POST** | `/api/libri/` | Creare un nuovo libro | Utente autenticato |
| **PUT** | `/api/libri/{id}/` | Aggiornare un libro | Utente autenticato |
| **PATCH** | `/api/libri/{id}/` | Aggiornamento parziale | Utente autenticato |
| **DELETE** | `/api/libri/{id}/` | Eliminare un libro | Admin |
| **POST** | `/api/autori/` | Creare un nuovo autore | Utente autenticato |
| **PUT** | `/api/autori/{id}/` | Aggiornare un autore | Utente autenticato |
| **DELETE** | `/api/autori/{id}/` | Eliminare un autore | Admin |

### Esempi di Richieste

**Creare un nuovo libro (autenticato):**

```bash
curl -X POST http://localhost:8000/api/libri/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "titolo": "Il Nome della Rosa",
    "anno": 1980,
    "genere": "Romanzo storico",
    "autore": 1
  }'
```

**Aggiornare un libro:**
```bash
curl -X PUT http://localhost:8000/api/libri/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "titolo": "Il Nome della Rosa - Edizione Speciale",
    "anno": 1980,
    "genere": "Giallo storico",
    "autore": 1
  }'
```

---
[↑ torna su](#-indice)

## 🧪 Testing

### Esecuzione dei Test

```bash
# Esegui tutti i test
docker exec -it django-backend python manage.py test

# Esegui i test di un'app specifica
docker exec -it django-backend python manage.py test catalog

# Esegui uno specifico test file
docker exec -it django-backend python manage.py test catalog.tests.test_models

# Con verbosità aumentata
docker exec -it django-backend python manage.py test --verbosity=2
```

---
[↑ torna su](#-indice)
<a id='sviluppo-senza-docker'><a>

## 🛠️ Sviluppo Senza Docker

Se preferisci sviluppare senza Docker:

### 1. Crea un Ambiente Virtuale

```bash
# Crea il virtual environment
python -m venv venv

# Attiva su Windows
venv\Scripts\activate

# Attiva su Linux/Mac
source venv/bin/activate
```

### 2. Installa le Dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configura il Database

Modifica `bookshelf/settings.py` per usare il database locale:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "vue_django",
        "USER": "root",
        "PASSWORD": "la_tua_password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

Oppure usa SQLite per test rapidi:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 4. Applica Migrazioni e Avvia

```bash
# Applica migrazioni
python manage.py migrate

# Crea superutente
python manage.py createsuperuser

# Avvia il server
python manage.py runserver 0.0.0.0:8000
```

---
[↑ torna su](#-indice)

## 🔧 Risoluzione dei Problemi

### Errore: "Address already in use"

**Problema**: La porta 8000 è già occupata.

**Soluzione**:
```bash
# Su Windows - trova e termina il processo
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Su Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Errore: "Can't connect to MySQL server"

**Problema**: Django non riesce a connettersi al database.

**Soluzione**:
```bash
# Verifica che MariaDB sia in esecuzione
docker ps | grep mariadb

# Verifica i log del database
docker logs mariadb

# Controlla che le variabili d'ambiente siano corrette
docker exec -it django-backend python -c "import os; print(os.getenv('DB_HOST'))"
```

### Errore: "ModuleNotFoundError: No module named 'catalog'"

**Problema**: Django non trova l'applicazione.

**Soluzione**:
```bash
# Verifica che 'catalog' sia in INSTALLED_APPS
docker exec -it django-backend python manage.py shell -c "import django; print(django.apps.apps.get_app_config('catalog'))"
```

### Errore CORS

**Problema**: Il frontend Vue non riesce a comunicare con l'API.

**Soluzione**:
Verifica che in `settings.py` siano configurati correttamente:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Porta del frontend Vue
    'http://127.0.0.1:5173',
]
CORS_ALLOW_ALL_ORIGINS = True  # Solo per sviluppo
```

### Riavvio Completo

Se tutto fallisce, riparti da zero:

```bash
# Ferma e rimuovi tutto
docker-compose down -v

# Rimuovi le immagini
docker rmi django-backend_web

# Ricostruisci da zero
docker-compose up -d --build

# Applica migrazioni
docker exec -it django-backend python manage.py migrate

# Crea superutente
docker exec -it django-backend python manage.py createsuperuser
```

---
[↑ torna su](#-indice)

## 📦 Dipendenze Dettagliate

### `requirements.txt` - Versione Completa

```txt
asgiref==3.11.1                    # ASGI server interface
Django==6.0.5                      # Web framework
django-cors-headers==4.9.0         # CORS handling
django-restframework==0.0.1        # (placeholder - non usare)
djangorestframework==3.17.1        # REST API framework
djangorestframework_simplejwt==5.5.1  # JWT authentication
neo4j==6.2.0                       # Neo4j database driver
PyJWT==2.13.0                      # JWT library
PyMySQL==1.2.0                     # MySQL/MariaDB driver
pytz==2026.2                       # Timezone handling
sqlparse==0.5.5                    # SQL parsing
tzdata==2026.2                     # Timezone database
```

> **Nota**: `django-restframework==0.0.1` è un placeholder. La libreria corretta è `djangorestframework`. Tieni presente che questo potrebbe causare conflitti. Consiglio di rimuoverlo e usare solo `djangorestframework`.

### Dipendenze per Ambiente di Sviluppo

```bash
# Per eseguire test e debug
pip install pytest pytest-django
pip install ipython  # Shell interattiva migliorata
pip install django-debug-toolbar  # Debug toolbar
```

---
[↑ torna su](#-indice)

## 🤝 Contribuire

1. **Fork** il repository
2. **Crea un branch** per la tua feature:
   ```bash
   git checkout -b feature/nuova-funzionalita
   ```
3. **Fai le modifiche** e testa
4. **Fai commit** delle modifiche:
   ```bash
   git commit -m "Aggiunta nuova funzionalità"
   ```
5. **Push** sul tuo fork:
   ```bash
   git push origin feature/nuova-funzionalita
   ```
6. Apri una **Pull Request**

---
[↑ torna su](#-indice)

## 📝 Licenza

[Specifica la licenza del tuo progetto]

---

## 📧 Contatti

[Inserisci i tuoi contatti o informazioni di supporto]

---

**Buon Coding! 🚀**