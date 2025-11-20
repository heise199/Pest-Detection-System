<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const handleMenuSelect = (index) => {
  router.push(index)
}

const activeMenu = computed(() => route.path)
</script>

<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <div class="logo">害虫检测系统</div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        @select="handleMenuSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="/">
          <el-icon><DataLine /></el-icon>
          <span>数据概览</span>
        </el-menu-item>
        <el-menu-item index="/detection">
          <el-icon><Camera /></el-icon>
          <span>检测中心</span>
        </el-menu-item>
        <el-menu-item index="/forum">
          <el-icon><ChatDotRound /></el-icon>
          <span>交流论坛</span>
        </el-menu-item>
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
        <el-menu-item v-if="userStore.isAdmin" index="/admin">
          <el-icon><Setting /></el-icon>
          <span>后台管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-content">
          <span>欢迎回来, {{ userStore.user.username }}</span>
          <el-button type="text" @click="handleLogout" style="color: #fff;">退出登录</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background-color: #434a50;
}
.el-menu-vertical {
  height: calc(100% - 60px);
  border-right: none;
}
.el-header {
  background-color: #545c64;
  color: #fff;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.header-content {
  display: flex;
  gap: 20px;
  align-items: center;
}
.el-main {
  background-color: #f0f2f5;
}
</style>

