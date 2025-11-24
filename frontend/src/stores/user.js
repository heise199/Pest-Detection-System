import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

// Safe localStorage access
const getStorageItem = (key, defaultValue = '') => {
  if (typeof window !== 'undefined' && window.localStorage) {
    return localStorage.getItem(key) || defaultValue
  }
  return defaultValue
}

const setStorageItem = (key, value) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem(key, value)
  }
}

const removeStorageItem = (key) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.removeItem(key)
  }
}

export const useUserStore = defineStore('user', () => {
  const token = ref(getStorageItem('token', ''))
  const user = ref(JSON.parse(getStorageItem('user', '{}')))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value.is_admin)

  function setToken(newToken) {
    token.value = newToken
    setStorageItem('token', newToken)
  }

  function setUser(newUser) {
    user.value = newUser
    setStorageItem('user', JSON.stringify(newUser))
  }

  function logout() {
    token.value = ''
    user.value = {}
    removeStorageItem('token')
    removeStorageItem('user')
  }

  async function login(username, password) {
    // OAuth2PasswordRequestForm requires application/x-www-form-urlencoded
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
    
    const res = await api.post('/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    setToken(res.data.access_token)
    
    const userRes = await api.get('/users/me')
    setUser(userRes.data)
  }

  async function register(username, email, password) {
    await api.post('/register', { username, email, password })
  }

  async function updateProfile(updates) {
    const res = await api.put('/users/me', updates)
    setUser(res.data)
    return res.data
  }

  return { token, user, isLoggedIn, isAdmin, login, logout, register, updateProfile, setUser }
})

