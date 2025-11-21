<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { Bug } from '@element-plus/icons-vue'

const pests = ref([])
const loading = ref(false)
const selectedPest = ref(null)
const dialogVisible = ref(false)

const fetchPests = async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/pests')
    pests.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const showPestDetail = (pest) => {
  selectedPest.value = pest
  dialogVisible.value = true
}

onMounted(fetchPests)
</script>

<template>
  <div class="pest-info-container">
    <div class="page-header">
      <h2 class="page-title">害虫百科</h2>
      <p class="page-subtitle">了解常见害虫的特征与防治方法</p>
    </div>

    <div v-loading="loading" class="pest-grid">
      <div 
        v-for="pest in pests" 
        :key="pest.id" 
        class="pest-card"
        @click="showPestDetail(pest)"
      >
        <div class="pest-image" v-if="pest.image_url">
          <el-image :src="pest.image_url" fit="cover" />
        </div>
        <div v-else class="pest-icon">🐛</div>
        <div class="pest-content">
          <h3 class="pest-name">{{ pest.name }}</h3>
          <p class="pest-description">{{ pest.description || '暂无描述' }}</p>
          <div class="pest-footer">
            <span class="view-detail">查看详情 →</span>
          </div>
        </div>
      </div>
      
      <div v-if="pests.length === 0 && !loading" class="empty-state">
        <el-icon class="empty-icon"><Bug /></el-icon>
        <p>暂无害虫信息</p>
      </div>
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      :title="selectedPest?.name || '害虫详情'"
      width="600px"
      class="pest-detail-dialog"
    >
      <div v-if="selectedPest" class="pest-detail">
        <div class="detail-image" v-if="selectedPest.image_url">
          <el-image :src="selectedPest.image_url" fit="contain" />
        </div>
        <div class="detail-content">
          <div class="detail-section">
            <h4>害虫描述</h4>
            <p>{{ selectedPest.description || '暂无描述' }}</p>
          </div>
          <div class="detail-section" v-if="selectedPest.control_methods">
            <h4>防治方法</h4>
            <p>{{ selectedPest.control_methods }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.pest-info-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--ins-text-primary);
}

.page-subtitle {
  font-size: 15px;
  color: var(--ins-text-secondary);
  margin: 0;
}

.pest-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.pest-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--ins-shadow);
}

.pest-card:hover {
  box-shadow: var(--ins-shadow-hover);
  transform: translateY(-4px);
}

.pest-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--ins-bg);
}

.pest-image :deep(.el-image) {
  width: 100%;
  height: 100%;
}

.pest-icon {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  opacity: 0.8;
}

.pest-content {
  padding: 20px;
}

.pest-name {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--ins-text-primary);
}

.pest-description {
  font-size: 14px;
  color: var(--ins-text-secondary);
  line-height: 1.6;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pest-footer {
  display: flex;
  justify-content: flex-end;
}

.view-detail {
  font-size: 14px;
  color: var(--ins-accent);
  font-weight: 500;
  transition: all 0.2s ease;
}

.pest-card:hover .view-detail {
  color: var(--ins-accent-hover);
  transform: translateX(4px);
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 80px 20px;
  color: var(--ins-text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.pest-detail-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.pest-detail {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-image {
  width: 100%;
  max-height: 300px;
  border-radius: var(--ins-radius-small);
  overflow: hidden;
  background: var(--ins-bg);
}

.detail-image :deep(.el-image) {
  width: 100%;
  height: 100%;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--ins-text-primary);
}

.detail-section p {
  font-size: 15px;
  line-height: 1.8;
  color: var(--ins-text-primary);
  margin: 0;
  white-space: pre-wrap;
}
</style>

