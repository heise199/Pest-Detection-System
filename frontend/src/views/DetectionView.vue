<script setup>
import { ref, computed } from 'vue'
import { UploadFilled, VideoCamera, Loading, CircleCheck, VideoPause, VideoPlay } from '@element-plus/icons-vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const activeTab = ref('image')
const uploadUrl = '/api/detection/upload'
const videoUploadUrl = '/api/detection/upload_video'
const imageUrl = ref('')
const videoResultUrl = ref('')
const resultData = ref(null)
const loading = ref(false)
const videoLoading = ref(false)
const videoUrl = ref('http://127.0.0.1:8000/detection/video_feed')
const isVideoActive = ref(false)

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token || ''}`
}))

const handleSuccess = (response) => {
  loading.value = false
  // response is the detection object
  imageUrl.value = `http://127.0.0.1:8000/${response.image_path}`
  resultData.value = response.result_json
  ElMessage.success('检测完成')
}

const handleError = () => {
  loading.value = false
  ElMessage.error('检测失败')
}

const beforeUpload = () => {
  loading.value = true
  imageUrl.value = ''
  resultData.value = null
  return true
}

const toggleVideo = () => {
  isVideoActive.value = !isVideoActive.value
}

const handleVideoUpload = async (file) => {
  videoLoading.value = true
  videoResultUrl.value = ''
  resultData.value = null
  
  const formData = new FormData()
  formData.append('file', file.raw || file)
  
  try {
    const res = await api.post('/detection/upload_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    if (res.data.video_path) {
      videoResultUrl.value = `http://127.0.0.1:8000/${res.data.video_path}`
    }
    resultData.value = res.data.result_json
    ElMessage.success('视频检测完成')
  } catch (e) {
    ElMessage.error('视频检测失败')
  } finally {
    videoLoading.value = false
  }
  return false // Prevent default upload
}
</script>

<template>
  <div class="detection-container">
    <div class="detection-tabs">
      <div class="tab-header">
        <div 
          :class="['tab-item', { active: activeTab === 'image' }]"
          @click="activeTab = 'image'"
        >
          <el-icon><UploadFilled /></el-icon>
          <span>图片检测</span>
        </div>
        <div 
          :class="['tab-item', { active: activeTab === 'video' }]"
          @click="activeTab = 'video'"
        >
          <el-icon><VideoCamera /></el-icon>
          <span>视频检测</span>
        </div>
        <div 
          :class="['tab-item', { active: activeTab === 'stream' }]"
          @click="activeTab = 'stream'"
        >
          <el-icon><VideoPlay /></el-icon>
          <span>实时检测</span>
        </div>
      </div>

      <div class="tab-content">
        <!-- 图片检测 -->
        <div v-show="activeTab === 'image'" class="tab-pane">
          <div class="upload-card">
            <el-upload
              class="upload-area"
              drag
              :action="uploadUrl"
              :headers="uploadHeaders" 
              :on-success="handleSuccess"
              :on-error="handleError"
              :before-upload="beforeUpload"
              :show-file-list="false"
            >
              <div class="upload-content">
                <el-icon class="upload-icon"><UploadFilled /></el-icon>
                <p class="upload-text">拖拽图片到此处或 <em>点击上传</em></p>
                <p class="upload-hint">支持 JPG、PNG 格式</p>
              </div>
            </el-upload>
          </div>
          
          <div v-if="loading" class="loading-card">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <p>正在检测中...</p>
          </div>
          
          <div v-if="imageUrl" class="result-card">
            <div class="result-image">
              <el-image :src="imageUrl" fit="contain" :preview-src-list="[imageUrl]" />
            </div>
            <div class="result-info">
              <h3 class="result-title">检测结果</h3>
              <div v-if="resultData && Object.keys(resultData).length > 0" class="result-list">
                <div v-for="(count, label) in resultData" :key="label" class="result-item">
                  <span class="pest-label">{{ label }}</span>
                  <span class="pest-count">{{ count }} 只</span>
                </div>
              </div>
              <div v-else class="no-result">
                <el-icon><CircleCheck /></el-icon>
                <p>未检测到害虫</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 视频上传检测 -->
        <div v-show="activeTab === 'video'" class="tab-pane">
          <div class="video-upload-card">
            <el-upload
              class="video-upload-area"
              drag
              :before-upload="handleVideoUpload"
              :show-file-list="false"
              accept="video/*"
            >
              <div class="upload-content">
                <el-icon class="upload-icon"><VideoCamera /></el-icon>
                <p class="upload-text">拖拽视频到此处或 <em>点击上传</em></p>
                <p class="upload-hint">支持 MP4、AVI、MOV 格式</p>
              </div>
            </el-upload>
          </div>
          
          <div v-if="videoLoading" class="loading-card">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <p>正在处理视频，请稍候...</p>
          </div>
          
          <div v-if="videoResultUrl" class="result-card">
            <div class="result-video">
              <video :src="videoResultUrl" controls class="video-player"></video>
            </div>
            <div class="result-info">
              <h3 class="result-title">检测结果</h3>
              <div v-if="resultData && Object.keys(resultData).length > 0" class="result-list">
                <div v-for="(count, label) in resultData" :key="label" class="result-item">
                  <span class="pest-label">{{ label }}</span>
                  <span class="pest-count">{{ count }} 只</span>
                </div>
              </div>
              <div v-else class="no-result">
                <el-icon><CircleCheck /></el-icon>
                <p>未检测到害虫</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 实时视频流检测 -->
        <div v-show="activeTab === 'stream'" class="tab-pane">
          <div class="video-card">
            <div class="video-control">
              <el-button 
                type="primary" 
                size="large"
                @click="toggleVideo"
                class="video-btn"
              >
                <el-icon v-if="!isVideoActive"><VideoPlay /></el-icon>
                <el-icon v-else><VideoPause /></el-icon>
                {{ isVideoActive ? '停止检测' : '开启摄像头' }}
              </el-button>
            </div>
            <div v-if="isVideoActive" class="video-container">
              <img :src="videoUrl" class="video-feed" />
            </div>
            <div v-else class="video-placeholder">
              <el-icon class="placeholder-icon"><VideoCamera /></el-icon>
              <p class="placeholder-text">点击按钮开启摄像头进行实时检测</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detection-container {
  max-width: 1200px;
  margin: 0 auto;
}

.detection-tabs {
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

.upload-card {
  border: 2px dashed var(--ins-border);
  border-radius: var(--ins-radius);
  background: var(--ins-bg);
  transition: all 0.3s ease;
}

.upload-card:hover {
  border-color: var(--ins-accent);
  background: rgba(0, 149, 246, 0.02);
}

.upload-area :deep(.el-upload) {
  width: 100%;
}

.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  border: none;
  background: transparent;
  padding: 60px 20px;
}

.upload-content {
  text-align: center;
}

.upload-icon {
  font-size: 64px;
  color: var(--ins-accent);
  margin-bottom: 16px;
}

.upload-text {
  font-size: 16px;
  color: var(--ins-text-primary);
  margin: 0 0 8px 0;
}

.upload-text em {
  color: var(--ins-accent);
  font-style: normal;
  font-weight: 600;
}

.upload-hint {
  font-size: 14px;
  color: var(--ins-text-secondary);
  margin: 0;
}

.loading-card {
  text-align: center;
  padding: 60px 20px;
  background: var(--ins-bg);
  border-radius: var(--ins-radius);
  margin-top: 24px;
}

.loading-icon {
  font-size: 48px;
  color: var(--ins-accent);
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.result-card {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-top: 24px;
}

.result-image {
  background: var(--ins-bg);
  border-radius: var(--ins-radius);
  padding: 16px;
  border: 1px solid var(--ins-border);
}

.result-image :deep(.el-image) {
  width: 100%;
  border-radius: var(--ins-radius-small);
}

.result-info {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 24px;
}

.result-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 20px 0;
  color: var(--ins-text-primary);
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ins-border);
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--ins-bg);
  border-radius: var(--ins-radius-small);
  transition: all 0.2s ease;
}

.result-item:hover {
  background: rgba(0, 149, 246, 0.05);
}

.pest-label {
  font-size: 15px;
  color: var(--ins-text-primary);
  font-weight: 500;
}

.pest-count {
  font-size: 16px;
  font-weight: 600;
  color: var(--ins-accent);
}

.no-result {
  text-align: center;
  padding: 40px 20px;
  color: var(--ins-text-secondary);
}

.no-result .el-icon {
  font-size: 48px;
  color: #52c41a;
  margin-bottom: 12px;
}

.video-card {
  background: var(--ins-bg);
  border-radius: var(--ins-radius);
  padding: 32px;
  border: 1px solid var(--ins-border);
}

.video-control {
  text-align: center;
  margin-bottom: 24px;
}

.video-btn {
  border-radius: var(--ins-radius-small);
  font-weight: 600;
  padding: 12px 32px;
}

.video-container {
  text-align: center;
  background: var(--ins-white);
  border-radius: var(--ins-radius);
  padding: 16px;
  border: 1px solid var(--ins-border);
}

.video-feed {
  max-width: 100%;
  border-radius: var(--ins-radius-small);
  box-shadow: var(--ins-shadow);
}

.video-upload-card {
  border: 2px dashed var(--ins-border);
  border-radius: var(--ins-radius);
  background: var(--ins-bg);
  transition: all 0.3s ease;
}

.video-upload-card:hover {
  border-color: var(--ins-accent);
  background: rgba(0, 149, 246, 0.02);
}

.video-upload-area :deep(.el-upload) {
  width: 100%;
}

.video-upload-area :deep(.el-upload-dragger) {
  width: 100%;
  border: none;
  background: transparent;
  padding: 60px 20px;
}

.video-player {
  width: 100%;
  border-radius: var(--ins-radius-small);
  background: #000;
}

.result-video {
  background: var(--ins-bg);
  border-radius: var(--ins-radius);
  padding: 16px;
  border: 1px solid var(--ins-border);
}

.video-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--ins-white);
  border-radius: var(--ins-radius);
  border: 1px solid var(--ins-border);
}

.placeholder-icon {
  font-size: 64px;
  color: var(--ins-text-secondary);
  margin-bottom: 16px;
}

.placeholder-text {
  font-size: 15px;
  color: var(--ins-text-secondary);
  margin: 0;
}
</style>

