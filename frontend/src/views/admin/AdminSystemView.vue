<script setup>
import { ref } from 'vue'
import { Setting, Bell, Lock, Database } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const systemInfo = ref({
  version: '1.0.0',
  database: 'MySQL',
  model: 'YOLOv8',
  lastBackup: '2024-01-15 10:30:00'
})

const handleBackup = () => {
  ElMessage.info('备份功能开发中...')
}

const handleClearCache = () => {
  ElMessage.info('清理缓存功能开发中...')
}

const handleUpdateModel = () => {
  ElMessage.info('模型更新功能开发中...')
}
</script>

<template>
  <div class="admin-system">
    <div class="system-info-card">
      <h3 class="card-title">系统信息</h3>
      <div class="info-list">
        <div class="info-item">
          <el-icon class="info-icon"><Setting /></el-icon>
          <div class="info-content">
            <div class="info-label">系统版本</div>
            <div class="info-value">{{ systemInfo.version }}</div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Database /></el-icon>
          <div class="info-content">
            <div class="info-label">数据库</div>
            <div class="info-value">{{ systemInfo.database }}</div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Setting /></el-icon>
          <div class="info-content">
            <div class="info-label">检测模型</div>
            <div class="info-value">{{ systemInfo.model }}</div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Bell /></el-icon>
          <div class="info-content">
            <div class="info-label">最后备份</div>
            <div class="info-value">{{ systemInfo.lastBackup }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="system-actions-card">
      <h3 class="card-title">系统操作</h3>
      <div class="actions-grid">
        <el-card class="action-card" shadow="hover">
          <div class="action-content">
            <el-icon class="action-icon"><Database /></el-icon>
            <div class="action-info">
              <div class="action-title">数据备份</div>
              <div class="action-desc">备份系统数据</div>
            </div>
            <el-button type="primary" @click="handleBackup">执行备份</el-button>
          </div>
        </el-card>

        <el-card class="action-card" shadow="hover">
          <div class="action-content">
            <el-icon class="action-icon"><Setting /></el-icon>
            <div class="action-info">
              <div class="action-title">清理缓存</div>
              <div class="action-desc">清理系统缓存数据</div>
            </div>
            <el-button type="warning" @click="handleClearCache">清理缓存</el-button>
          </div>
        </el-card>

        <el-card class="action-card" shadow="hover">
          <div class="action-content">
            <el-icon class="action-icon"><Lock /></el-icon>
            <div class="action-info">
              <div class="action-title">更新模型</div>
              <div class="action-desc">更新检测模型版本</div>
            </div>
            <el-button type="success" @click="handleUpdateModel">更新模型</el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-system {
  max-width: 1400px;
  margin: 0 auto;
}

.system-info-card,
.system-actions-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--ins-shadow);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 20px 0;
  color: var(--ins-text-primary);
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ins-border);
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

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.action-card {
  border-radius: var(--ins-radius);
}

.action-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-icon {
  font-size: 32px;
  color: var(--ins-accent);
}

.action-info {
  flex: 1;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--ins-text-primary);
  margin-bottom: 4px;
}

.action-desc {
  font-size: 13px;
  color: var(--ins-text-secondary);
}
</style>

