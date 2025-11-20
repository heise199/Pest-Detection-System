<script setup>
import { onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api/axios'

const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  // App startup check: Validate token if it exists
  if (userStore.token) {
    try {
      // Try to fetch user profile to validate token
      await api.get('/users/me')
    } catch (e) {
      // If 401 or other error, logout and redirect
      // Note: Axios interceptor handles 401, but we can be explicit here
      if (!userStore.token) { // If interceptor cleared it
         router.push('/login')
      }
    }
  }
})
</script>

<template>
  <RouterView />
</template>

<style>
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>
