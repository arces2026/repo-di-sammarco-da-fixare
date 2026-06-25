<script setup>
defineProps({
  product: Object //Optional, for internal use
})

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
</script>

<template>
  <div class="product-card">
    <div class="product-card__image-container">
      <slot name="image" :product="product">
      </slot>
    </div>

    <div class="product-card__content">
      <slot name="content" :product="product">
      </slot>
    </div>

    <div class="product-card__footer">
      <slot name="footer" :product="product">
      </slot>
    </div>
  </div>
</template>

<style scoped>

.product-card {
  position: relative;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  background-color: #fff;
  display: flex;
  flex-direction: column;
  max-width: 320px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.product-card__image-container :deep(img) {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.product-card__content {
  padding: 16px;
  flex-grow: 1; /* Spinge il footer sempre in fondo se le card hanno altezze diverse */
}

.product-card__title {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  color: #333;
}

.product-card__description {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.product-card__footer {
  padding: 16px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fafafa;
}

.product-card__price {
  font-weight: bold;
  font-size: 1.2rem;
  color: #2c3e50;
}

.product-card__btn {
  background-color: #42b883;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.product-card__btn:hover {
  background-color: #35495e;
}
</style>