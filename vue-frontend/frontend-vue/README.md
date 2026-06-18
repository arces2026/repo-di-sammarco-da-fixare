# Lezioni Vue JS

## 🟢 1. Introduzione a Vue 3 (Composition API)

### 🎯 Obiettivi della lezione
- Configurare l’ambiente di sviluppo
- Installare Node.js
- Creare un progetto Vue con Vite
- Comprendere la Composition API
- Creare il primo componente: `Counter`
- Installare i plugin essenziali per lo sviluppo

---
### ⚙️ 1. Configurazione ambiente
---

### 📦 Installazione Node.js

A differenza del metodo CDN, che carica Vue come una semplice libreria esterna nel browser, l'installazione tramite Node.js permette di usare strumenti professionali per compilare file .vue e gestire progetti complessi. Node.js serve quindi a creare un ambiente di build ottimizzato, mentre la CDN è utile solo per prototipi rapidi o piccoli script pronti all'uso

👉 Scarica e installa da: https://nodejs.org

Verifica installazione sul terminale:

```bash
node -v
npm -v
```

---
### 🚀 2. Creazione progetto con Vite
---

Vite è il tool ufficiale consigliato per creare progetti Vue moderni.

```bash
npm create vite@latest
```

### 🧭 Scelte durante il setup

```text
✔ Project name: vue-counter  
✔ Select a framework: Vue  
✔ Select a variant: Customize with create-vue  
```

### ⚙️ Domande di configurazione

```text
✔ Project name: vue-counter  

✔ Add TypeScript? → No ❌  
✔ Add JSX Support? → No ❌  
✔ Add Vue Router for Single Page Application? → Yes ✅  
✔ Add Pinia for state management? → No ❌  
✔ Add Vitest for Unit Testing? → No ❌  
✔ Add an End-to-End Testing Solution? → No ❌  
✔ Add ESLint for code quality? → Yes ✅  
✔ Add Prettier for code formatting? → Yes ✅  
```

---
### 📦 3. Esecuzione progetto
---

Installa tutte le dipendenze del progetto:

```sh
npm install
```
Esegui progetto su server Vite:

```sh
npm run dev
```

In questo modo l'ambiente Vite
- Avvia un server locale (es: http://localhost:5173)
- Aggiorna automaticamente la pagina quando modifichi il codice (Hot Reload)
- Viene usato durante lo sviluppo

---
### 🏗️ 4. Compilazione e minificazione per ambiente di production
---

Con il comando di build si crea una build ottimizzata per la produzione cioè per applicazione finale da mettere su server:

```sh
npm run build
```

- Genera file ottimizzati e compressi
- Output nella cartella dist/
- Pronto per il deploy


## 🟢 2. Analisi applicazione di base creata da Vite

### 📄 main.js
È il punto di ingresso dell’app Vue. Qui viene creata l’applicazione e collegata al DOM.

Contiene l’inizializzazione di Vue e l’eventuale registrazione di plugin come il router.

---

### 📄 App.vue
È il componente root dell’applicazione.  
Tutti gli altri componenti vengono inseriti al suo interno.

Gestisce il layout principale e ospita il `<router-view />` quando si usa il routing.

---

### 📁 components/
Cartella dedicata ai componenti riutilizzabili.

Qui si inseriscono elementi UI indipendenti come:
- Counter
- Button personalizzati
- Card, input, ecc.

---

### 📁 views/
Contiene le “pagine” dell’applicazione.

Ogni file rappresenta una schermata associata a una rotta (es: Home, About).

---

### 📁 router/
Contiene la configurazione delle rotte dell’app.

Definisce quali componenti vengono mostrati in base all’URL.

---
```
vue-counter/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   └── index.js
│   ├── views/
│   │   └── HomeView.vue
│   └── components/
```
---

### 🧠 Idea chiave
- `components/` → blocchi riutilizzabili
- `views/` → pagine dell’app
- `router/` → navigazione tra pagine
- `App.vue` → struttura principale
- `main.js` → avvio dell’app


## 🧩 3. Componenti 
I componenti sono blocchi di costruzione riutilizzabili della UI. Sono piccole parti di interfaccia, focalizzate su uno specifico compito.
- Pensate per essere riutilizzate in più pagine o anche all’interno di altri componenti.

Esempi:  
- `<StudentForm />` — può essere usato, ad esempio, sia nella vista *Aggiungi* che *Modifica* di una applicazione di gestione impiegati.  

- `<StudentList />` — Può essere usato nella vista *Home* ma anche in una vista di riepilogo.
<br>
<br>
Non corrispondono direttamente a una route.
- Pensa a `components/` come ai mattoncini LEGO che puoi combinare per costruire le pagine.



## 🧩 5. Comunicazione col server 

La comunicazione tra client e server in JavaScript avviene oggi principalmente grazie alla funzione fetch(). Questa API moderna ha sostituito il vecchio approccio XMLHttpRequest, offrendo una sintassi più snella basata sulle Promise.

### 📡 I Verbi HTTP (Metodi)
Prima di inviare una richiesta, è fondamentale scegliere il "verbo" corretto in base all'operazione da compiere:
- GET: Per richiedere dati dal server (metodo predefinito).
- POST: Per inviare nuovi dati (es. creare un nuovo utente).
- PUT / PATCH: Per aggiornare dati esistenti.
- DELETE: Per rimuovere una risorsa.


### 🚀 Esempio 1: Richiesta POST (Sintassi .then)
Il metodo fetch() restituisce una Promise. Possiamo gestirla concatenando i metodi .then() per processare la risposta.

```javascript
fetch('https://server.com/api/student', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'Andrea', class: 'Java' })
})
.then(response => response.json())
.then(result => console.log('Successo:', result))
.catch(error => console.error('Errore:', error));
```

### ⏳ Esempio 2: Richiesta GET (Sintassi Async/Await)
L'approccio async/await è lo standard moderno: rende il codice asincrono più leggibile, facendolo sembrare "lineare".

```javascript
async function getStudentData() {
  try {
    const response = await fetch('https://server.com/api/student');
    
    // Verifica se la risposta è andata a buon fine (status 200-299)
    if (!response.ok) {
      throw new Error(`Errore HTTP: ${response.status}`);
    }

    const data = await response.json(); // Estrae il corpo JSON
    console.log(data);
  } catch (error) {
    console.error("Si è verificato un errore:", error);
  }
}
```

<b> Da ricordare </b>
1. JSON Serialization: Quando invii dati con POST o PUT, devi quasi sempre usare JSON.stringify(oggetto) nel body.

2. Due Livelli di Errore:
    1. Il catch rileva errori di connettività (connessione assente).
    2. L'if (!response.ok) rileva errori del server (pagina non trovata o server in crash).

3. CORS: Ricorda che per motivi di sicurezza, il browser potrebbe bloccare richieste verso domini diversi se il server non è configurato per accettarle (Cross-Origin Resource Sharing).

## Json Server
```
npx json-server db.json 
```