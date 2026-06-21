<script setup>
import Grid from '@/components/Grid.vue'
import ProductList from '@/components/ProductList.vue'
import { onMounted, ref } from 'vue'
import { useConstStore } from '@/stores/constStore'

const constStore = useConstStore()

const libri = ref([])
const autori = ref([])

const gridLibriColumns = ['titolo', 'anno', 'genere', 'autore.nome']
const radioSelection = ['titolo', 'anno', 'genere', 'autore.nome', 'all']
const gridAutoriColumns = ['nome', 'nazione']
const searchQuery = ref('')
const selectedField = ref('all')
console.log({selectedField: selectedField.value})
onMounted(() => {
  fetch('http://localhost:8000/api/v1/libri/')
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
      console.log({ dataResults: data.results })
      console.log({ libriKeys: Object.keys(data.results[0]) })
      libri.value = data.results
    })

  console.log(libri.value)

  fetch('http://localhost:8000/api/v1/autori')
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
})
</script>

<template>
  <main class="main">
    <form id="search">
      Cerca <input name="query" v-model="searchQuery" />
      <ul v-for="key in radioSelection" :key="key">
        <label for="key">{{ key }}</label>
        <input type="radio" name="radio" v-model="selectedField" checked="key"/>
      </ul>
      <!-- <label for="all">All</label>
      <input id="all" type="radio" name="radio" /> -->
    </form>

    <Grid style="width: 45%" :data="libri" :columns="gridLibriColumns" :filter-key="searchQuery" :selected-field="selectedField">
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
.main {
  display: flex;
  justify-content: space-between;
}
</style>
