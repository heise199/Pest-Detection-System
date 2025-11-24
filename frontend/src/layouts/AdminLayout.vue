<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Setting, InfoFilled, User as UserIcon, DataLine, View } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

// 管理员菜单项
const menuItems = [
  { path: '/admin', label: '管理首页', icon: 'DataLine' },
  { path: '/admin/pests', label: '害虫管理', icon: 'InfoFilled' },
  { path: '/admin/users', label: '用户管理', icon: 'UserIcon' },
  { path: '/admin/system', label: '系统设置', icon: 'Setting' }
]

const pageTitles = {
  '/admin': '管理首页',
  '/admin/pests': '害虫管理',
  '/admin/users': '用户管理',
  '/admin/system': '系统设置'
}

const currentPageTitle = computed(() => pageTitles[route.path] || '管理后台')
const activeMenu = computed(() => route.path)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const handleMenuSelect = (path) => {
  router.push(path)
}

const goToUserView = () => {
  router.push('/')
}
</script>

<template>
  <div class="admin-layout-wrapper">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">⚙️</div>
          <span class="logo-text">管理后台</span>
        </div>
      </div>
      <nav class="sidebar-nav">
        <div 
          v-for="item in menuItems" 
          :key="item.path"
          :class="['nav-item', { active: activeMenu === item.path || activeMenu.startsWith(item.path) }]"
          @click.stop="handleMenuSelect(item.path)"
        >
          <el-icon class="nav-icon">
            <DataLine v-if="item.icon === 'DataLine'" />
            <InfoFilled v-else-if="item.icon === 'InfoFilled'" />
            <UserIcon v-else-if="item.icon === 'UserIcon'" />
            <Setting v-else-if="item.icon === 'Setting'" />
          </el-icon>
          <span class="nav-text">{{ item.label }}</span>
        </div>
      </nav>
      <div class="sidebar-footer">
        <el-button 
          text 
          class="switch-view-btn"
          @click="goToUserView"
        >
          <el-icon><View /></el-icon>
          <span>切换到用户视图</span>
        </el-button>
      </div>
    </aside>
    
    <div class="main-content">
      <header class="top-header">
        <div class="header-left">
          <h2 class="page-title">{{ currentPageTitle }}</h2>
        </div>
        <div class="header-right">
          <div class="user-info">
            <el-avatar :size="32" class="user-avatar">
              {{ userStore.user.username?.[0]?.toUpperCase() || 'A' }}
            </el-avatar>
            <div class="user-details">
              <span class="username">{{ userStore.user.username }}</span>
              <span class="user-role">管理员</span>
            </div>
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
.admin-layout-wrapper {
  display: flex;
  height: 100vh;
  background: var(--ins-bg);
}

.admin-sidebar {
  width: 280px;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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
  color: #ffffff;
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
  padding: 14px 16px;
  margin-bottom: 4px;
  border-radius: var(--ins-radius-small);
  cursor: pointer;
  transition: all 0.2s ease;
  color: rgba(255, 255, 255, 0.7);
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.nav-item.active {
  background: rgba(0, 149, 246, 0.3);
  color: #ffffff;
  font-weight: 600;
  border-left: 3px solid var(--ins-accent);
}

.nav-icon {
  font-size: 20px;
}

.nav-text {
  font-size: 15px;
}

.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.switch-view-btn {
  width: 100%;
  color: rgba(255, 255, 255, 0.7);
  padding: 12px;
  border-radius: var(--ins-radius-small);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.switch-view-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.main-content {
  flex: 1;
  margin-left: 280px;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  font-weight: 600;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.username {
  font-size: 15px;
  font-weight: 500;
  color: var(--ins-text-primary);
}

.user-role {
  font-size: 12px;
  color: var(--ins-text-secondary);
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

/* 滚动条样式 */
.sidebar-nav::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>

