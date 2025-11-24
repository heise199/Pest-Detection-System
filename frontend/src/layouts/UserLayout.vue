<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { DataLine, Camera, ChatDotRound, User, InfoFilled } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

// 普通用户菜单项
const menuItems = [
  { path: '/', label: '数据概览', icon: 'DataLine' },
  { path: '/detection', label: '检测中心', icon: 'Camera' },
  { path: '/pests', label: '害虫百科', icon: 'InfoFilled' },
  { path: '/forum', label: '交流论坛', icon: 'ChatDotRound' },
  { path: '/profile', label: '个人中心', icon: 'User' }
]

const pageTitles = {
  '/': '数据概览',
  '/detection': '检测中心',
  '/pests': '害虫百科',
  '/forum': '交流论坛',
  '/profile': '个人中心'
}

const currentPageTitle = computed(() => {
  const path = route.path
  return pageTitles[path] || pageTitles[path.replace(/\/$/, '')] || '首页'
})

const activeMenu = computed(() => {
  const path = route.path
  // 确保路径匹配正确，包括根路径
  if (path === '/' || path === '') return '/'
  return path
})

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const handleMenuSelect = (path) => {
  console.log('菜单点击:', path, '当前路径:', route.path)
  if (route.path !== path) {
    router.push(path).catch(err => {
      console.error('路由跳转失败:', err)
    })
  }
}
</script>

<template>
  <div class="layout-wrapper">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">🐛</div>
          <span class="logo-text">PestDetect</span>
        </div>
      </div>
      <nav class="sidebar-nav">
        <div 
          v-for="item in menuItems" 
          :key="item.path"
          :class="['nav-item', { active: activeMenu === item.path || (item.path === '/' && activeMenu === '/') }]"
          @click="handleMenuSelect(item.path)"
        >
          <el-icon class="nav-icon">
            <DataLine v-if="item.icon === 'DataLine'" />
            <Camera v-else-if="item.icon === 'Camera'" />
            <InfoFilled v-else-if="item.icon === 'InfoFilled'" />
            <ChatDotRound v-else-if="item.icon === 'ChatDotRound'" />
            <User v-else-if="item.icon === 'User'" />
          </el-icon>
          <span class="nav-text">{{ item.label }}</span>
        </div>
      </nav>
    </aside>
    
    <div class="main-content">
      <header class="top-header">
        <div class="header-left">
          <h2 class="page-title">{{ currentPageTitle }}</h2>
        </div>
        <div class="header-right">
          <div class="user-info">
            <el-avatar :size="32" class="user-avatar">
              {{ userStore.user.username?.[0]?.toUpperCase() || 'U' }}
            </el-avatar>
            <span class="username">{{ userStore.user.username }}</span>
          </div>
          <el-button 
            text 
            class="logout-btn" 
            @click="handleLogout"
          >
            退出
          </el-button>
        </div>
      </header>
      <main class="content-area">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.layout-wrapper {
  display: flex;
  height: 100vh;
  background: var(--ins-bg);
}

.sidebar {
  width: 260px;
  background: var(--ins-white);
  border-right: 1px solid var(--ins-border);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid var(--ins-border);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 28px;
  line-height: 1;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  color: var(--ins-text-primary);
  letter-spacing: -0.5px;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: var(--ins-radius-small);
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--ins-text-primary);
  user-select: none;
  -webkit-user-select: none;
  pointer-events: auto;
}

.nav-item:hover {
  background: var(--ins-bg);
}

.nav-item.active {
  background: rgba(0, 149, 246, 0.1);
  color: var(--ins-accent);
  font-weight: 600;
}

.nav-icon {
  font-size: 20px;
}

.nav-text {
  font-size: 15px;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-header {
  background: var(--ins-white);
  border-bottom: 1px solid var(--ins-border);
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.username {
  font-size: 15px;
  font-weight: 500;
  color: var(--ins-text-primary);
}

.logout-btn {
  color: var(--ins-text-secondary);
  font-size: 14px;
  padding: 8px 16px;
  border-radius: var(--ins-radius-small);
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: var(--ins-bg);
  color: var(--ins-text-primary);
}

.content-area {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}
</style>

