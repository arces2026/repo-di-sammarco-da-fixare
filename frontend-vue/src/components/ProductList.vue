<script setup>
import { computed, reactive, ref } from 'vue';

const showOnlyInStock = ref(true);
const products = ref([
    { id: 1, nome: "Scarpe Nike Air", prezzo: 150, inStock: true },
    { id: 2, nome: "Maglietta Adidas", prezzo: 45, inStock: true },
    { id: 3, nome: "Jeans Levi's", prezzo: 85, inStock: false },
    { id: 4, nome: "Orologio Casio", prezzo: 60, inStock: true },
    { id: 5, nome: "Zaino Eastpak", prezzo: 70, inStock: true },
    { id: 6, nome: "Cuffie Sony", prezzo: 120, inStock: false },
    { id: 7, nome: "Occhiali Ray-Ban", prezzo: 130, inStock: true },
    { id: 8, nome: "Portafoglio Pelle", prezzo: 40, inStock: true },
    { id: 9, nome: "Giacca Invernale", prezzo: 180, inStock: false },
    { id: 10, nome: "Smartphone Xiaomi", prezzo: 299, inStock: true }
]);

const author = reactive({
  name: 'John Doe',
  books: [
    'Vue 2 - Advanced Guide',
    'Vue 3 - Basic Guide',
    'Vue 4 - The Mystery'
  ]
})


const publishedBooksMessage = computed(() => {
  return author.books.length > 0 ? 'Si' : 'No'
})

function calculateBooksMessage() {
  return author.books.length > 0 ? 'Yes' : 'No'
}


const filteredProducts = computed(() => {
  return products.value.filter(product => {
    return !showOnlyInStock.value || product.inStock
  })
})

</script>

<template>
    <div>
      <button @click="showOnlyInStock = !showOnlyInStock">
        {{ showOnlyInStock ? 'Mostra tutti' : 'Mostra solo disponibili' }}
      </button>

      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="product-div"
      >
          <p>{{ product.nome }}</p>
          <p>{{ product.prezzo }}</p>
          <p class="blue" v-if="product.inStock">Disponibile</p>
          <p class="red" v-else>Esaurito</p>
      </div> 

    </div>
    


<!--     
    <p>{{ author.name}}</p>
    <p>Has published books:</p>
    <span>{{ publishedBooksMessage }}</span>
    <br>
    <span>{{ calculateBooksMessage() }}</span> -->


</template>

<style scoped>
    .product-div{
        margin-bottom: 20px;
        background-color: aquamarine;
        border-radius: 15px;
        border: 1px rgb(190, 139, 139) solid;
        padding: 10px;
    }
    
    .red{
        color: red;
    }
    .blue{
        color: blue;
    }

    button{
        width: 100%;
        padding: 10px;
        font-size: large;
        background-color: rgb(49, 97, 81);
        color: aliceblue;
        margin-bottom: 30px;
        border-radius: 30px;
    }
</style>