# 📚 Bookshelf API - Django Backend

API REST per un sistema di gestione di una libreria con autenticazione JWT, containerizzata con Docker e MariaDB.

---

## 📋 Indice

- [Panoramica](#-panoramica)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Prerequisiti](#-prerequisiti)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Installazione e Avvio con Docker](#-installazione-e-avvio-con-docker)
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

```text
MONO-REPO-DJANGO-VUE/
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
│   ├── db.sqlite3                     # Database SQLite (solo sviluppo locale)
│   └── README.md                      # Questo file
│
├── vue-frontend/                      # Frontend Vue.js (progetto separato)
│
├── docker-compose.yml                 # Orchestrazione container Docker
├── .env                               # Variabili d'ambiente
├── .gitignore                         # ignora i file non utili nei repositories
├── .dockerignore                      # ignora i file non utili nei containers
└── README.md                          # Readme generale

```

---

[↑ torna su](#-indice)
<a id='gestione-del-database'><a>


---

## 🐳 Installazione e Avvio con Docker

Questa sezione ti guida attraverso l'installazione e l'avvio dell'intero stack (backend Django + MariaDB) utilizzando Docker e Docker Compose.

### 1. Clonare il Repository

```bash
# Clona il repository
git clone https://github.com/[tuo-username]/[nome-del-repository].git

# Entra nella directory del progetto
cd [nome-del-repository]
```

### 2. Configurare le Variabili d'Ambiente

Crea un file `.env` nella root del progetto con le seguenti variabili:

```bash
# Crea il file .env
touch .env
```

Aggiungi queste variabili al file `.env`:

```env
# Database Configuration
DB_NAME=vue_django
DB_USER=root
DB_PASSWORD=your_secure_password_here
DB_HOST=db # <--- nome del servizio nel docker-compose.yml
DB_PORT=3306

# MariaDB Root Password (same as DB_PASSWORD per semplicità)
MARIADB_ROOT_PASSWORD=your_secure_password_here

<!-- le seguenti config non sono applicate al presente progetto -->
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)
```

> **⚠️ IMPORTANTE**: Sostituisci `your_secure_password_here` con una password sicura e `your-secret-key-here` con una chiave segreta unica. In produzione, usa chiavi generate casualmente.

### 3. Avviare i Container

#### Avvio in Background (Modalità Detached)

```bash
# Costruisci le immagini e avvia i container in background
docker-compose up -d --build
```

#### Avvio con Log in Tempo Reale (Modalità Attached)

```bash
# Costruisci e avvia mostrando i log in console
docker-compose up --build
```

Premi `Ctrl+C` per fermare i container in questa modalità.

### 4. Verificare lo Stato dei Container

```bash
# Controlla che tutti i container siano in esecuzione
docker-compose ps

# Dovresti vedere qualcosa simile a:
# NAME                IMAGE                   STATUS
# django-backend      django-backend_web      Up 0.0.0.0:8000->8000/tcp
# mariadb             mariadb:11              Up 0.0.0.0:3307->3306/tcp
```

### 5. Applicare le Migrazioni al Database

```bash
# Applica le migrazioni iniziali
docker exec -it django-backend python manage.py migrate

# Output atteso:
# Operations to perform:
#   Apply all migrations: admin, auth, catalog, contenttypes, sessions
#   Running migrations:
#     Applying contenttypes.0001_initial... OK
#     Applying auth.0001_initial... OK
#     ...
```

### 6. Creare un Superutente (Admin)

```bash
# Crea un utente amministratore
docker exec -it django-backend python manage.py createsuperuser

# Segui le istruzioni interattive:
# Username (leave blank to use 'root'): admin
# Email address: admin@example.com
# Password: ********
# Password (again): ********
# Superuser created successfully.
```

### 7. Popolare il Database con Dati di Test (Opzionale)

Se hai un file di dump o dati di test:

```bash
# Carica dati di test da un file fixture
docker exec -it django-backend python manage.py loaddata initial_data.json

# Oppure usa il comando per caricare dati di esempio
docker exec -it django-backend python manage.py shell -c "
from catalog.models import Autore, Libro
autore = Autore.objects.create(nome='J.R.R.', cognome='Tolkien')
Libro.objects.create(titolo='Il Signore degli Anelli', anno=1954, genere='Fantasy', autore=autore)
print('Dati di test creati con successo!')
"
```

### 8. Accedere all'Applicazione

| Servizio | URL | Descrizione |
|----------|-----|-------------|
| **API Backend** | http://localhost:8000/ | Endpoint dell'API Django (404 dopo la creazione del progetto è normale) |
| **Admin Panel** | http://localhost:8000/admin/ | Pannello di amministrazione Django |
| **API Docs** | http://localhost:8000/api/v1 | Root dell'API |
| **Health Check** | http://localhost:8000/health/ | Verifica stato dell'applicazione (non implementato) | 

### 9. Comandi Utili per la Gestione dei Container

#### Fermare i Container

```bash
# Ferma tutti i container
docker-compose down

# Ferma e rimuovi anche i volumi (cancella i dati del database)
docker-compose down -v
```

#### Riavvio dei Container

```bash
# Riavvio tutti i container
docker-compose restart

# Riavvio solo il backend
docker-compose restart web

# Riavvio solo il database
docker-compose restart mariadb
```

#### Visualizzare i Log

```bash
# Visualizza tutti i log
docker-compose logs

# Visualizza solo i log del backend
docker-compose logs web

# Visualizza gli ultimi 100 log e segui nuovi log in tempo reale
docker-compose logs -f --tail=100 web

# Visualizza i log del database
docker-compose logs mariadb
```

#### Eseguire Comandi nei Container

```bash
# Apri una shell interattiva nel container backend
docker exec -it django-backend bash

# Esegui un comando singolo nel backend
docker exec -it django-backend python manage.py shell

# Connettiti al database MariaDB
docker exec -it mariadb mariadb -u root -p
# Inserisci la password configurata nel .env
```

### 10. Verificare che tutto funzioni

#### Test dell'API con curl

```bash
# Verifica che l'API risponda
curl http://localhost:8000/api/v1/autori/

# Dovresti ricevere una risposta JSON (anche vuota se non ci sono autori)
# []
```

#### Test dell'Admin Panel

1. Apri il browser su http://localhost:8000/admin/
2. Accedi con le credenziali del superutente create al punto 6
3. Dovresti vedere il pannello di amministrazione Django

#### Test del Database

```bash
# Verifica la connessione al database
docker exec -it django-backend python manage.py dbshell

# Esegui una query di test
SHOW TABLES;
# Dovresti vedere le tabelle create da Django
```

### 11. Stop e Pulizia Completa

Quando hai finito di lavorare:

```bash
# Ferma e rimuovi tutti i container
docker-compose down

# Rimuovi anche i volumi (ATTENZIONE: cancella tutti i dati)
docker-compose down -v

# Rimuovi le immagini non utilizzate (opzionale)
docker system prune -f

# Rimuovi anche le immagini specifiche del progetto
docker rmi django-backend_web
```


### Tempi di Avvio Stimati

| Fase | Tempo stimato |
|------|---------------|
| Download immagini Docker | 2-5 minuti (primo avvio) |
| Build del container backend | 1-3 minuti |
| Avvio dei container | 10-30 secondi |
| Migrazioni database | 10-20 secondi |
| **Totale primo avvio** | **~5-10 minuti** |
| **Avvio successivo** | **~30-60 secondi** |

---

## 🔄 Flusso di Sviluppo Tipico con Docker

### Per sviluppatori che lavorano con il backend

```bash
# 1. Avvia i container in background
docker-compose up -d

# 2. Applica migrazioni (se hai modificato i modelli)
docker exec -it django-backend python manage.py makemigrations
docker exec -it django-backend python manage.py migrate

# 3. Modifica il codice localmente (i cambiamenti si riflettono automaticamente)

# 4. Esegui i test
docker exec -it django-backend python manage.py test

# 5. Visualizza i log in tempo reale durante lo sviluppo
docker-compose logs -f web
```

### Per sviluppatori che lavorano con il frontend

Se stai sviluppando anche il frontend Vue, assicurati che le impostazioni CORS siano configurate correttamente:

```python
# In settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite default port
    'http://localhost:8080',  # Vue CLI default port
]

# O per sviluppo (meno sicuro ma più pratico)
CORS_ALLOW_ALL_ORIGINS = True  # Solo per sviluppo!
```

---
[↑ torna su](#-indice)

## 🗄️ Gestione del Database

### Accesso diretto a MariaDB

```bash
# Connettiti al database tramite terminale
docker exec -it mariadb mariadb -u root -p
# Inserisci la tua password: ********

# Una volta dentro mariadb:
USE vue_django;
SHOW TABLES;
SELECT * FROM auth_user;
SELECT * FROM catalog_libro;
SELECT * FROM catalog_autore;
```

### Backup del Database

```bash
# Crea un backup del database
docker exec mariadb mysqldump -u root -p[your-password] vue_django > backup_$(date +%Y%m%d).sql

# Backup di tutti i database
docker exec mariadb mysqldump -u root -p[your-password] --all-databases > backup_full.sql
```

### Ripristino del Database

```bash
# Ripristina da backup
cat [nome_file].sql | docker exec -i mariadb mariadb -u root -p[your-password] vue_django
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

### Collegamento al container mariadb da Dbeaver (se mariadb è installato anche in locale)

```bash
# Se mariadb è installato in locale bisogna mappare una porta host diversa dalla 3306
# altrimenti Dbeaver si colleghera con l'istanza locale.
...
 environment:
      MARIADB_ROOT_PASSWORD: ${MARIADB_ROOT_PASSWORD}
      MARIADB_DATABASE: ${DB_NAME}
    ports:
      - "3307:3306" # <--- la porta host (a sx) deve essere diversa dalla 3306
    volumes:
...
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
| **POST** | `/api/v1/register/` | Registrazione nuovo utente |
| **POST** | `/api/v1/login` | Login - ottenere JWT |
| **POST** | `/api/v1/token/refresh` | Rinnovare JWT |
| **GET** | `/api/v1/libri/` | Lista di tutti i libri |
| **GET** | `/api/v1/libri/{id}/` | Dettaglio di un libro |
| **GET** | `/api/v1/autori/` | Lista di tutti gli autori |
| **GET** | `/api/v1/autori/{id}/` | Dettaglio di un autore |
| **GET** | `/api/v1/profilo/` | Profilo utente |

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

### Errore: "env: 'bash\r': No such file or directory"

**Problema**: I file script (come `wait-for-it.sh`) hanno terminazioni di riga Windows (CRLF) invece di Unix (LF). Questo errore si verifica quando si esegue uno script con shebang `#!/usr/bin/env bash` su un sistema Linux/Docker, e il carattere `\r` (carriage return) viene interpretato come parte del nome dell'interprete.

**Soluzione**:

```bash
# Converti il file da formato Windows (CRLF) a Unix (LF)
dos2unix wait-for-it.sh

# Oppure usa sed (disponibile su tutti i sistemi)
sed -i 's/\r$//' wait-for-it.sh

# Verifica la conversione (non dovresti vedere ^M alla fine delle righe)
cat -v wait-for-it.sh
```

**Prevenzione**: Per evitare questo problema in futuro, configura Git per gestire correttamente le terminazioni di riga:

```bash
# Imposta Git per convertire automaticamente in LF al checkout
git config --global core.autocrlf input

# O per questo repository specifico
git config core.autocrlf input
```

Puoi anche aggiungere questa conversione al Dockerfile per correggere automaticamente il file durante la build:

```dockerfile
# Dopo COPY . .
RUN sed -i 's/\r$//' /app/wait-for-it.sh
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