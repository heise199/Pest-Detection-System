<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import api from '@/api/axios'
import { Download, User, Message, Calendar, Shield } from '@element-plus/icons-vue'

const userStore = useUserStore()
const history = ref([])
const loading = ref(false)

const fetchHistory = async () => {
  loading.value = true
  try {
    const res = await api.get('/detection/history')
    history.value = res.data
  } catch (e) {
    // Handled
  } finally {
    loading.value = false
  }
}

const downloadReport = (id) => {
  window.open(`http://127.0.0.1:8000/detection/report/${id}`, '_blank')
}

onMounted(fetchHistory)
</script>

<template>
  <div class="profile-container">
    <div class="profile-header">
      <el-avatar :size="80" class="profile-avatar">
        {{ userStore.user.username?.[0]?.toUpperCase() || 'U' }}
      </el-avatar>
      <div class="profile-info">
        <h2 class="profile-name">{{ userStore.user.username }}</h2>
        <div class="profile-meta">
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            注册于 {{ formatDate(userStore.user.created_at) }}
          </span>
        </div>
      </div>
    </div>

    <div class="info-card">
      <h3 class="card-title">个人信息</h3>
      <div class="info-list">
        <div class="info-item">
          <el-icon class="info-icon"><User /></el-icon>
          <div class="info-content">
            <div class="info-label">用户名</div>
            <div class="info-value">{{ userStore.user.username }}</div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Message /></el-icon>
          <div class="info-content">
            <div class="info-label">邮箱</div>
            <div class="info-value">{{ userStore.user.email || '未设置' }}</div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Shield /></el-icon>
          <div class="info-content">
            <div class="info-label">角色</div>
            <div class="info-value">
              <span :class="['role-badge', { admin: userStore.isAdmin }]">
                {{ userStore.isAdmin ? '管理员' : '普通用户' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="history-card">
      <div class="card-header">
        <h3 class="card-title">检测历史</h3>
        <span class="history-count">共 {{ history.length }} 条记录</span>
      </div>
      <div v-loading="loading" class="history-list">
        <div 
          v-for="item in history" 
          :key="item.id" 
          class="history-item"
        >
          <div class="history-image" v-if="item.image_path">
            <el-image 
              :src="`http://127.0.0.1:8000/${item.image_path}`"
              :preview-src-list="[`http://127.0.0.1:8000/${item.image_path}`]"
              fit="cover"
            />
          </div>
          <div class="history-content">
            <div class="history-meta">
              <span class="history-type">{{ item.detection_type === 'image' ? '图片检测' : '视频检测' }}</span>
              <span class="history-time">{{ formatTime(item.created_at) }}</span>
            </div>
            <div class="history-result" v-if="item.result_json">
              <span 
                v-for="(count, pest) in item.result_json" 
                :key="pest"
                class="result-tag"
              >
                {{ pest }} × {{ count }}
              </span>
            </div>
            <div v-else class="no-result">未检测到害虫</div>
          </div>
          <div class="history-actions">
            <el-button 
              size="small" 
              type="primary"
              :icon="Download"
              @click="downloadReport(item.id)"
              class="download-btn"
            >
              报告
            </el-button>
          </div>
        </div>
        <div v-if="history.length === 0 && !loading" class="empty-history">
          <el-icon class="empty-icon"><Calendar /></el-icon>
          <p>还没有检测记录</p>
        </div>
      </div>
    </div>
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
    },
    formatTime(timeString) {
      const date = new Date(timeString)
      return date.toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
}

.profile-header {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 32px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  box-shadow: var(--ins-shadow);
}

.profile-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  font-size: 32px;
  flex-shrink: 0;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--ins-text-primary);
}

.profile-meta {
  display: flex;
  gap: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--ins-text-secondary);
}

.info-card,
.history-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--ins-shadow);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ins-border);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.history-count {
  font-size: 14px;
  color: var(--ins-text-secondary);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--ins-bg);
  border-radius: var(--ins-radius-small);
}

.info-icon {
  font-size: 24px;
  color: var(--ins-accent);
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 13px;
  color: var(--ins-text-secondary);
  margin-bottom: 4px;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: var(--ins-text-primary);
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  background: var(--ins-bg);
  border: 1px solid var(--ins-border);
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

.role-badge.admin {
  background: rgba(0, 149, 246, 0.1);
  border-color: var(--ins-accent);
  color: var(--ins-accent);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--ins-bg);
  border-radius: var(--ins-radius);
  border: 1px solid var(--ins-border);
  transition: all 0.2s ease;
}

.history-item:hover {
  background: var(--ins-white);
  box-shadow: var(--ins-shadow);
}

.history-image {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  border-radius: var(--ins-radius-small);
  overflow: hidden;
  border: 1px solid var(--ins-border);
}

.history-image :deep(.el-image) {
  width: 100%;
  height: 100%;
}

.history-content {
  flex: 1;
  min-width: 0;
}

.history-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.history-type {
  font-size: 13px;
  padding: 4px 10px;
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: 12px;
  color: var(--ins-text-primary);
  font-weight: 500;
}

.history-time {
  font-size: 13px;
  color: var(--ins-text-secondary);
}

.history-result {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.result-tag {
  font-size: 12px;
  padding: 4px 10px;
  background: rgba(0, 149, 246, 0.1);
  color: var(--ins-accent);
  border-radius: 12px;
  font-weight: 500;
}

.no-result {
  font-size: 14px;
  color: var(--ins-text-secondary);
  font-style: italic;
}

.history-actions {
  display: flex;
  align-items: center;
}

.download-btn {
  border-radius: var(--ins-radius-small);
  font-weight: 500;
}

.empty-history {
  text-align: center;
  padding: 60px 20px;
  color: var(--ins-text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}
</style>
