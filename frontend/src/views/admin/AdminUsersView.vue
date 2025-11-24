<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { User, Search } from '@element-plus/icons-vue'
import { useDateFormat } from '@/composables/useDateFormat'

const { formatDate } = useDateFormat()

const users = ref([])
const loading = ref(false)
const searchQuery = ref('')

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/users')
    users.value = res.data
  } catch (e) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) ||
    (user.email && user.email.toLowerCase().includes(query))
  )
})

const handleToggleAdmin = async (user) => {
  try {
    await api.put(`/admin/users/${user.id}`, {
      is_admin: !user.is_admin
    })
    ElMessage.success(user.is_admin ? '已取消管理员权限' : '已授予管理员权限')
    fetchUsers()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

onMounted(fetchUsers)
</script>

<template>
  <div class="admin-users">
    <div class="section-header">
      <h3 class="section-title">用户管理</h3>
      <div class="header-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户..."
          :prefix-icon="Search"
          class="search-input"
          clearable
        />
        <span class="user-count">共 {{ users.length }} 位用户</span>
      </div>
    </div>

    <div class="user-list" v-loading="loading">
      <div v-for="user in filteredUsers" :key="user.id" class="user-card">
        <el-avatar :size="56" class="user-avatar">
          {{ user.username?.[0]?.toUpperCase() || 'U' }}
        </el-avatar>
        <div class="user-info">
          <div class="user-name-row">
            <span class="user-name">{{ user.username }}</span>
            <span :class="['role-badge', { admin: user.is_admin }]">
              {{ user.is_admin ? '管理员' : '普通用户' }}
            </span>
          </div>
          <div class="user-email">{{ user.email || '未设置邮箱' }}</div>
          <div class="user-time">注册于 {{ formatDate(user.created_at) }}</div>
        </div>
        <div class="user-actions">
          <el-button 
            :type="user.is_admin ? 'warning' : 'primary'"
            size="small"
            @click="handleToggleAdmin(user)"
          >
            {{ user.is_admin ? '取消管理员' : '设为管理员' }}
          </el-button>
        </div>
      </div>
      <div v-if="filteredUsers.length === 0 && !loading" class="empty-state">
        <el-icon class="empty-icon"><User /></el-icon>
        <p>{{ searchQuery ? '未找到匹配的用户' : '还没有用户' }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-users {
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ins-border);
  flex-wrap: wrap;
  gap: 16px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.user-count {
  font-size: 14px;
  color: var(--ins-text-secondary);
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  transition: all 0.2s ease;
  box-shadow: var(--ins-shadow);
}

.user-card:hover {
  box-shadow: var(--ins-shadow-hover);
  transform: translateY(-1px);
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  font-size: 24px;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--ins-text-primary);
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  background: var(--ins-bg);
  border: 1px solid var(--ins-border);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--ins-text-secondary);
}

.role-badge.admin {
  background: rgba(0, 149, 246, 0.1);
  border-color: var(--ins-accent);
  color: var(--ins-accent);
}

.user-email {
  font-size: 14px;
  color: var(--ins-text-secondary);
  margin-bottom: 4px;
}

.user-time {
  font-size: 12px;
  color: var(--ins-text-secondary);
}

.user-actions {
  flex-shrink: 0;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--ins-text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}
</style>

