<template>
    <form @submit.prevent="submitForm">
        <input type="text" placeholder="Cognome" v-model="form.cognome" required>
        <span>{{ form.cognome }}</span>
        <input type="text" placeholder="Nome" v-model="form.nome" required>
        <input type="number" placeholder="Età" v-model.number="form.eta" required>
        <input type="email" placeholder="Email" v-model="form.email" required>
        <button type="submit">Aggiungi Utente</button>
    </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';

// Dichiarazione dell'evento per evitare l'avviso "Extraneous non-emits"
const emit = defineEmits(['add-user']);

const form = reactive({
    cognome: '',
    nome: '',
    eta: null,
    email: ''
});

const submitForm = () => {
    emit('add-user', {
        cognome: form.cognome.trim(),
        nome: form.nome.trim(),
        eta: form.eta,
        email: form.email.trim()
    });

    // Reset dei campi del form dopo l'invio
    form.cognome = '';
    form.nome = '';
    form.eta = null;
    form.email = '';
};
</script>
