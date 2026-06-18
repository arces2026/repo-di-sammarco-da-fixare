// mouse.js
import { ref, onMounted, onUnmounted } from 'vue'

// per convenzione, i nomi delle funzioni composable iniziano con "use"
export function useMouse() {
  // stato incapsulato e gestito dal composable
  const x = ref(0)
  const y = ref(0)

  // un composable può aggiornare il suo stato gestito nel tempo.
  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  // un composable può anche collegarsi all'hook del ciclo di vita del suo componente
  // per configurare ed eliminare gli effetti collaterali.
  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  // espone lo stato gestito con un `return`
  return { x, y }
}