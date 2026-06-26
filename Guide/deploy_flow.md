# Step-by-Step Flow: Deploy della Webapp (Didattica)

Questo documento descrive il flusso completo, passo dopo passo, per il deploy della vostra applicazione web containerizzata (Frontend Vue e Backend Django + MariaDB), sfruttando l'integrazione con GitHub per la CI/CD.

L'architettura proposta separa il **Frontend statico**, hostato gratuitamente su Vercel, dal **Backend e Database**, eseguiti tramite Docker su un server VPS gratuito o economico.

---

## Fase 1: Deploy Automatico del Frontend (Vue) su Vercel
Vercel è la strada più rapida e indolore per Vue: si aggancia a GitHub e compie le operazioni di build e deploy in modo autonomo a ogni `git push`.

1. **Preparazione su GitHub:** Assicuratevi che il progetto Vue si trovi in una cartella specifica del repository (es. `/frontend`) o in un repository dedicato.
2. **Collegamento a Vercel:**
   * Accedete a Vercel utilizzando il vostro account GitHub.
   * Cliccate su **Add New Project** e importate il repository.
   * Vercel riconoscerà automaticamente il framework Vite/Vue e configurerà il comando di build.
3. **Variabili d'ambiente:** Andate nelle impostazioni del progetto su Vercel (`Settings` -> `Environment Variables`) e aggiungete l'URL di produzione del vostro backend (es. `VUE_APP_API_BASE_URL=https://vostro-ip-backend.com`).
4. **Deploy Iniziale e CI/CD:** Cliccate su **Deploy**. Da questo momento in poi, ogni `git push` sul branch principale farà scattare il build e aggiornerà il frontend live automaticamente.

---

## Fase 2: Configurazione del Backend (Django) e Database (MariaDB)

1. **Predisporre il server:**
   * Create la vostra macchina virtuale in cloud (es. VPS o Oracle Cloud Free Tier) ed accedete via SSH.
   * Installate **Docker** e **Docker Compose** sul server.
2. **Adattare la configurazione per la produzione:**
   * Nel file `docker-compose.prod.yml` (o `docker-compose.yml`), mappate la porta del backend (es. 8000) e assicuratevi che il volume di MariaDB punti a una cartella fisica del server per salvare i dati in modo permanente.
   * Impostate `DEBUG = False` nel file `settings.py` di Django e aggiungete l'IP pubblico del server o il dominio in `ALLOWED_HOSTS`.
   * Configurate il pacchetto `django-cors-headers` per permettere all'URL di Vercel di comunicare con Django.
3. **Trasferimento dei file:**
   * Caricate i file del progetto (inclusi Dockerfile e docker-compose) sul server, ad esempio clonando il repository GitHub direttamente nella macchina virtuale (`git clone ...`).
4. **Primo avvio manuale:**
   * Entrate nella cartella del progetto via SSH.
   * Lanciate il comando `docker-compose up -d --build` per avviare i container in background.
   * Eseguite le migrazioni di Django all'interno del container: `docker-compose exec backend python manage.py migrate`.

---

## Fase 3: Automatizzare il Backend con GitHub Actions (CI/CD)
Per evitare di dover accedere via SSH a ogni modifica del backend, potete configurare una pipeline di GitHub Actions.

1. **Creazione dei Secret su GitHub:**
   * Andate su GitHub nel vostro repository -> `Settings` -> `Secrets and variables` -> `Actions`.
   * Aggiungete le variabili di accesso al server: `VPS_IP`, `VPS_USER`, `VPS_SSH_KEY` (la chiave privata SSH).
2. **Scrittura del Workflow:**
   * Create la cartella `.github/workflows/` nel vostro progetto.
   * Al suo interno, create il file `deploy-backend.yml` per eseguire il pull del codice aggiornato sul server e il restart dei container tramite SSH.
3. **Test del flusso:**
   * Modificate il codice del backend in locale ed effettuate commit e push su GitHub.
   * Controllate la scheda **Actions** su GitHub per verificare lo stato della pipeline.
   * A pipeline completata, il server remoto avrà scaricato l'aggiornamento e riavviato i container.
