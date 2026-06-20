import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import ProductsView from '@/views/ProductsView.vue'
import RegisterView from '@/views/RegisterView.vue'
import UsersView from '@/views/UsersView.vue'
import { createRouter, createWebHistory } from 'vue-router'
// import { jwtDecode } from 'jwt-decode';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',                // L'URL del browser
      name: 'home',             // Un nome univoco per la rotta (opzionale ma consigliato)
      component: HomeView       // Il componente associato
    },
    {
      path: '/products',            // L'URL del browser
      name: 'products',             // Un nome univoco per la rotta (opzionale ma consigliato)
      component: ProductsView       // Il componente associato
    },
    {
      path:'/users',
      name:'users',
      component: UsersView,
      meta: { richiedeAuth: true }
    },
    {
      path:'/login',
      name:'login',
      component: LoginView
    },
    {
      path:'/register',
      name:'register',
      component: RegisterView
    }
  ],
})

// --- IL CONTROLLO ACCESSI (Navigation Guard) ---
router.beforeEach((to, from) => {
  const token = localStorage.getItem('token');

  // Caso 1: La rotta richiede l'autenticazione?
  if (to.meta.richiedeAuth) {
    
    // Se il token non esiste, rimanda al login
    if (!token) {
      return '/login';
    }

    try {
      // Decodifichiamo il token per leggere la scadenza e il ruolo
      //const decoded = jwtDecode(token);

      // // SOTTO-CONTROLLO opzionale: Il token è scaduto? (exp è in secondi, Date.now() in millisecondi)
      // if (decoded.exp && decoded.exp * 1000 < Date.now()) {
      //   localStorage.removeItem('token'); // Cancella il token scaduto
      //   return next('/login');
      // }

      // // Caso 2: La rotta richiede un ruolo specifico?
      // if (to.meta.ruoliConsentiti) {
      //   // Se il ruolo dell'utente non è tra quelli consentiti, blocca l'accesso
      //   if (!to.meta.ruoliConsentiti.includes(decoded.role)) {
      //     alert("Non hai i permessi per accedere a questa pagina!");
      //     return next('/dashboard'); // Rimanda a una pagina sicura
      //   }
      // }

    } catch (error) {
      // Se il token è corrotto o non decodificabile, pulisci e rimanda al login
      localStorage.removeItem('token');
      return '/login';
    }
  }

  // Se i controlli passano (o la rotta è pubblica), procedi normalmente
  return;
});

export default router
