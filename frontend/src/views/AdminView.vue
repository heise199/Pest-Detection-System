<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { Bug, User, Plus } from '@element-plus/icons-vue'

const activeTab = ref('pests')
const pests = ref([])
const users = ref([])
const loading = ref(false)

const dialogVisible = ref(false)
const newPest = ref({
  name: '',
  description: '',
  control_methods: '',
  image_url: ''
})

const fetchPests = async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/pests')
    pests.value = res.data
  } finally {
    loading.value = false
  }
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/users')
    users.value = res.data
  } finally {
    loading.value = false
  }
}

const handleCreatePest = async () => {
  try {
    await api.post('/admin/pests', newPest.value)
    ElMessage.success('添加成功')
    dialogVisible.value = false
    newPest.value = { name: '', description: '', control_methods: '', image_url: '' }
    fetchPests()
  } catch (e) {
    // Handled
  }
}

const handleTabClick = (tab) => {
  if (tab.paneName === 'pests') fetchPests()
  if (tab.paneName === 'users') fetchUsers()
}

onMounted(fetchPests)
</script>

<template>
  <div class="admin-container">
    <div class="admin-tabs">
      <div class="tab-header">
        <div 
          :class="['tab-item', { active: activeTab === 'pests' }]"
          @click="activeTab = 'pests'; handleTabClick({ paneName: 'pests' })"
        >
          <el-icon><Bug /></el-icon>
          <span>害虫百科</span>
        </div>
        <div 
          :class="['tab-item', { active: activeTab === 'users' }]"
          @click="activeTab = 'users'; handleTabClick({ paneName: 'users' })"
        >
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </div>
      </div>

      <div class="tab-content">
        <!-- 害虫百科管理 -->
        <div v-show="activeTab === 'pests'" class="tab-pane">
          <div class="section-header">
            <h3 class="section-title">害虫百科管理</h3>
            <el-button 
              type="primary" 
              :icon="Plus"
              @click="dialogVisible = true"
              class="add-btn"
            >
              添加害虫
            </el-button>
          </div>
          <div class="pest-grid" v-loading="loading">
            <div v-for="pest in pests" :key="pest.id" class="pest-card">
              <div class="pest-header">
                <h4 class="pest-name">{{ pest.name }}</h4>
              </div>
              <div class="pest-content">
                <p class="pest-description">{{ pest.description || '暂无描述' }}</p>
                <div class="pest-methods" v-if="pest.control_methods">
                  <strong>防治方法：</strong>
                  <p>{{ pest.control_methods }}</p>
                </div>
              </div>
            </div>
            <div v-if="pests.length === 0 && !loading" class="empty-state">
              <el-icon class="empty-icon"><Bug /></el-icon>
              <p>还没有害虫信息</p>
            </div>
          </div>
        </div>

        <!-- 用户管理 -->
        <div v-show="activeTab === 'users'" class="tab-pane">
          <div class="section-header">
            <h3 class="section-title">用户管理</h3>
            <span class="user-count">共 {{ users.length }} 位用户</span>
          </div>
          <div class="user-list" v-loading="loading">
            <div v-for="user in users" :key="user.id" class="user-card">
              <el-avatar :size="48" class="user-avatar">
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
            </div>
            <div v-if="users.length === 0 && !loading" class="empty-state">
              <el-icon class="empty-icon"><User /></el-icon>
              <p>还没有用户</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      title="添加害虫信息" 
      width="600px"
      class="pest-dialog"
    >
      <el-form :model="newPest" label-position="top">
        <el-form-item label="名称">
          <el-input v-model="newPest.name" placeholder="输入害虫名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="newPest.description" 
            type="textarea" 
            :rows="3" 
            placeholder="输入害虫描述"
          />
        </el-form-item>
        <el-form-item label="防治方法">
          <el-input 
            v-model="newPest.control_methods" 
            type="textarea" 
            :rows="3" 
            placeholder="输入防治方法"
          />
        </el-form-item>
        <el-form-item label="图片URL">
          <el-input v-model="newPest.image_url" placeholder="输入图片链接（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreatePest">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  methods: {
    formatDate(dateString) {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
}

.admin-tabs {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  overflow: hidden;
  box-shadow: var(--ins-shadow);
}

.tab-header {
  display: flex;
  border-bottom: 1px solid var(--ins-border);
  background: var(--ins-bg);
}

.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--ins-text-secondary);
  font-weight: 500;
  border-bottom: 2px solid transparent;
}

.tab-item:hover {
  background: rgba(0, 149, 246, 0.05);
  color: var(--ins-text-primary);
}

.tab-item.active {
  color: var(--ins-accent);
  border-bottom-color: var(--ins-accent);
  background: var(--ins-white);
}

.tab-content {
  padding: 32px;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ins-border);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.user-count {
  font-size: 14px;
  color: var(--ins-text-secondary);
}

.add-btn {
  border-radius: var(--ins-radius-small);
  font-weight: 600;
}

.pest-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.pest-card {
  background: var(--ins-bg);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 20px;
  transition: all 0.3s ease;
}

.pest-card:hover {
  background: var(--ins-white);
  box-shadow: var(--ins-shadow);
  transform: translateY(-2px);
}

.pest-header {
  margin-bottom: 12px;
}

.pest-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.pest-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--ins-text-primary);
}

.pest-description {
  margin: 0 0 12px 0;
  color: var(--ins-text-secondary);
}

.pest-methods {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--ins-border);
}

.pest-methods strong {
  color: var(--ins-text-primary);
  font-size: 13px;
}

.pest-methods p {
  margin: 4px 0 0 0;
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
  gap: 16px;
  padding: 20px;
  background: var(--ins-bg);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  transition: all 0.2s ease;
}

.user-card:hover {
  background: var(--ins-white);
  box-shadow: var(--ins-shadow);
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
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
  margin-bottom: 6px;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--ins-text-primary);
}

.role-badge {
  display: inline-block;
  padding: 2px 10px;
  background: var(--ins-white);
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

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--ins-text-secondary);
  grid-column: 1 / -1;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.pest-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.pest-dialog :deep(.el-input__wrapper),
.pest-dialog :deep(.el-textarea__inner) {
  border-radius: var(--ins-radius-small);
}
</style>

