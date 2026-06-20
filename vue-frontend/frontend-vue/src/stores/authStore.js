import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function setAuth(data) {
    token.value = data.access
    refreshToken.value = data.refreshToken
    user.value = data.user || null
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    if (data.user) {
      localStorage.setItem('user', JSON.stringify(data.user))
    }
  }

  function clearAuth() {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  function getAuthHeader() {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  async function login(username, password) {
    try {
      const response = await fetch('http://localhost:8000/api/v1/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Login failed')
      }

      const data = await response.json()
      setAuth(data)
      return { success: true, data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  async function register(userData) {
    try {
      const response = await fetch('http://localhost:8000/api/v1/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })

      const data = await response.json()

      if (!response.ok) {
        // format error message for display
        const errorMessages = Object.values(data).flat().join(' ')
        throw new Error(errorMessages || 'Registration failed')
      }
      return { success: true, data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  async function logout() {
    clearAuth()
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    getAuthHeader,
    setAuth,
    clearAuth,
  }
})
