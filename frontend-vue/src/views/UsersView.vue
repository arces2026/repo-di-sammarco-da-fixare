<script setup>
import UserForm from '@/components/UserForm.vue';
import UsersList from '@/components/UsersList.vue';
import { onMounted, ref } from 'vue';


const users = ref([]);
let etichetta = ref("")

onMounted(() => {
  fetch('http://localhost:3000/users')
    .then((response) => {
      // Controllo manuale dello stato HTTP
      if (!response.ok) {
        throw new Error(`Errore HTTP: ${response.status}`)
      }
      // Converte la risposta in JSON (ritorna una nuova Promise)
      return response.json()
    })
    .then((data) => {
      // Aggiorna lo stato reattivo con i dati ricevuti
      users.value = data
    })
    
    console.log(users.value);

})


function addUser(data){
    
    fetch('http://localhost:3000/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cognome: data.cognome,
            nome: data.nome,
            eta: data.eta,
            email: data.email
        })
    })
    .then(response => response.json())
    .then(data => {
      console.log("Dato aggiunto:", data)
      users.value.push(data);
    }
      
    )
    .catch(error => console.error("Errore:", error));   

}


</script>

<template>
    <!-- CORREZIONE: L'evento viene ascoltato qui, dove viene effettivamente emesso -->
    <UserForm @add-user="addUser"></UserForm>
    <span>{{ etichetta }}</span>
    <!-- La lista deve solo ricevere i dati aggiornati -->
    <UsersList :users="users"></UsersList>
</template>
