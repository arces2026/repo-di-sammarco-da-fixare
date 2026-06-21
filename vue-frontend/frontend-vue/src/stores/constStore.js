import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useConstStore = defineStore('constant', () => {
  // seleziona campo per ricerca libri
  const titolo = ref(false)
  const anno = ref(false)
  const genere = ref(false)
  const autore = ref(false)
  const all = ref(true)

    console.log({titolo: titolo.value})

  return {
    titolo,
    anno,
    genere,
    autore,
    all,
  }
})
