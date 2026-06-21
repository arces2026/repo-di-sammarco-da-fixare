<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import Button from './ui/Button.vue'
import HeartIcon from './ui/HeartIcon.vue'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.login(username.value, password.value)

  if (result.success) {
    router.push('/')
  } else {
    error.value = 'Invalid username or password'
  }
  loading.value = false
}

</script>

<template>
  <form>
    <input type="text" placeholder="Username" v-model="username" />
    <input type="password" placeholder="Password" v-model="password" />
    <Button type="submit" @click.prevent="handleLogin"> <span>Login</span><HeartIcon /> </Button>
  </form>
</template>

<style scoped>
input {
  padding: 5px;
}
</style>
