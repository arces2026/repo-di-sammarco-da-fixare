import { defineStore } from 'pinia'
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {

    const token = ref(localStorage.getItem('token') || null);

    function saveToken(nuovoToken) {
        localStorage.setItem('token', nuovoToken);
        token.value = nuovoToken;
    }

    function removeToken() {
        localStorage.removeItem('token');
        token.value = null;
    }

    return { 
        token,
        saveToken,
        removeToken
    };
  
})