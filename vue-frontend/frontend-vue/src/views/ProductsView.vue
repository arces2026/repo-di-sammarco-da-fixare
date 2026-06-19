<script setup>
import Grid from '@/components/Grid.vue';
import ProductList from '@/components/ProductList.vue';
import { onMounted, ref } from 'vue';

const libri = ref([]);
const autori = ref([]);

const gridLibriColumns = ['titolo', 'anno', 'genere', 'autore.nome']
const gridAutoriColumns = ['nome', 'nazione']
const searchQuery = ref('')

onMounted(() => {
  fetch('http://localhost:8000/api/libri/')
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
      libri.value = data.results
    })
    
    // console.log(libri.value);

  fetch('http://localhost:8000/api/autori')
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
      autori.value = data.results
    })
    
    // console.log(autori.value);
});


</script>

<template>
  <main class="main" >
    <form id="search">
      Cerca <input name="query" v-model="searchQuery">
    </form>

    <Grid
      style="width: 45%;"
      :data="libri"
      :columns="gridLibriColumns"
      :filter-key="searchQuery">
    </Grid>
    
    <!-- <Grid
      style="width: 45%;"
      :data="autori"
      :columns="gridAutoriColumns"
      :filter-key="searchQuery">
    </Grid> -->
  </main>

</template>

<style>
  .main{
    display: flex;
    justify-content:space-between;
  }

</style>
