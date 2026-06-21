<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'


const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  password2: '',
})

// const username = ref('')
// const password = ref('')
// const password2 = ref('')
// const email = ref('')
// const firstName = ref('')
// const lastName = ref('')
const registrationMessage = ref('')
const registrationError = ref('')
const loading = ref(false)
const errors = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
})

// New registration function with DRF
const HandleRegister = async () => {
  registrationMessage.value = ''
  registrationError.value = ''
  Object.keys(errors).forEach((key) => (errors[key] = ''))

  loading.value = true

  const result = await authStore.register(form)

  if (result.success) {
    registrationMessage.value = 'Registration successful! Redirecting to login...'
    // Clear form
    Object.keys(form).forEach((key) => (form[key] = ''))
    // Redirect to login after 2 sec
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    //Parse error message
    const errorText = result.error
    if (errorText.includes('username')) {
      errors.username = 'Username already exists or is invalid'
    } else if (errorText.includes('password')) {
      errors.password = 'Password does not meet requirements'
      errors.password2 = 'Password does not meet requirements'
    } else {
      registrationError.value = errorText || 'Registration failed. Please try again-'
    }
  }
  loading.value = false

}
</script>

<template>
  <form>
    <input type="text" placeholder="First name" v-model="form.first_name" />
    <input type="text" placeholder="Last Name" v-model="form.last_name" />
    <input type="email" placeholder="Email" v-model="form.email" />
    <input type="text" placeholder="Username" v-model="form.username" />
    <input type="password" placeholder="Password" v-model="form.password" />
    <input type="password" placeholder="retype Password" v-model="form.password2" />
    <button type='submit' @click.prevent="HandleRegister">Register</button>
    <p>{{ registrationMessage }}</p>
  </form>
</template>
