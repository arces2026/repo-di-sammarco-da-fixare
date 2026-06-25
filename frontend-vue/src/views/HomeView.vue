<script setup>
import { onMounted, ref } from 'vue'
import ProductCard from '@/components/ProductCard.vue'
import getProducts from '@/services/productService'
import { useCartStore } from '@/stores/cartStore'

const cartStore = useCartStore()

console.log({ cart: cartStore.totalItems })

// defineProps({
//   nome: String,
//   prezzo: Number,
//   sconto: { type: Number, default: 0 },
//   prezzo_scontato: Number, // ← arriva già calcolato
//   valuta: { type: String, default: 'EUR' },
//   descrizione: String,
//   categoria: String,
//   materiale: String,
//   disponibilita: { type: Boolean, default: true },

//   // Array di taglie (JSONField Django → Array JS)
//   taglie_disponibili: {
//     type: Array,
//     default: () => [], //Array/Object: default SEMPRE come funzione
//   },

//   // URL immagine (nullable)
//   immagine_url: {
//     type: String,
//     default: null,
//   },

//   // Sconto (DecimalField → Number in JS)
//   sconto: {
//     type: Number,
//     default: 0.0,
//     validator: (val) => val >= 0 && val <= 100,
//   },
//   prezzo_scontato: Number,
// })

const products = ref([])
const error = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    products.value = await getProducts()
  } catch (err) {
    error.value = 'Impossibile caricare i prodotti.'
  } finally {
    loading.value = false
  }
  // console.log(products.value)
})
</script>

<template>
  <main class="grid">
    <ProductCard v-for="product in products" :key="product.id">
      <template #image>
        <div class="badge-wrapper">
          <span class="badge">sconto {{ product.sconto }} %</span>
          <img :src="product.immagine_url" :alt="product.nome" />
        </div>
      </template>

      <template #content>
        <span class="category">{{ product.categoria }}</span>
        <h3 class="custom-title">{{ product.nome }}</h3>
        <p class="custom-desc">
          {{ product.descrizione }}
        </p>
      </template>

      <template #footer>
        <div class="price-container">
          <span class="old-price">{{ product.prezzo }}</span>
          <span class="new-price">{{ product.prezzo_scontato }}</span>
        </div>
        <button class="add-btn" @click="cartStore.addToCart">Aggiungi</button>
      </template>
    </ProductCard>
  </main>
</template>

<style scoped>
.grid {
  display: grid;
  grid: auto-flow / repeat(3, 1fr);
  gap: 20px;
}

.badge {
  position: absolute;
  left: 5px;
  top: 5px;
  color: rgb(245, 229, 229);
  background-color: rgb(57, 113, 8);
  border-radius: 10px;
  font-size: 0.8em;
  padding: 4px;
}

.add-btn {
  padding: 10px;
}

.old-price {
  font-size: 0.9rem;
  color: #757575;
  /* Grigio sbiadito */
  text-decoration: line-through;
  /* Barra il testo */
  margin-right: 10px;
}

/* Stile per il nuovo prezzo */
.new-price {
  font-size: 1.25rem;
  font-weight: bold;
  color: #d32f2f;
  /* Un rosso per l'offerta, oppure usa il verde/colore del tuo brand */
}
</style>
