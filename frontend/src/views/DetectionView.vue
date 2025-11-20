<script setup>
import { ref, computed } from 'vue'
import { UploadFilled, VideoCamera } from '@element-plus/icons-vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const activeTab = ref('image')
const uploadUrl = '/api/detection/upload'
const imageUrl = ref('')
const resultData = ref(null)
const loading = ref(false)
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
</script>

<template>
  <div class="detection-container">
    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="图片检测" name="image">
        <div class="upload-area">
          <el-upload
            class="upload-demo"
            drag
            :action="uploadUrl"
            :headers="uploadHeaders" 
            :on-success="handleSuccess"
            :on-error="handleError"
            :before-upload="beforeUpload"
            :show-file-list="false"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
          </el-upload>
        </div>
        
        <div v-if="loading" class="loading-text">正在检测中...</div>
        
        <div v-if="imageUrl" class="result-area">
          <el-row :gutter="20">
            <el-col :span="16">
              <el-image :src="imageUrl" fit="contain" :preview-src-list="[imageUrl]" />
            </el-col>
            <el-col :span="8">
              <el-card header="检测结果">
                <div v-for="(count, label) in resultData" :key="label" class="result-item">
                  <span class="label">{{ label }}</span>
                  <el-tag>{{ count }}</el-tag>
                </div>
                <div v-if="!resultData || Object.keys(resultData).length === 0">
                  未检测到害虫
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="实时视频流检测" name="video">
        <div class="video-control">
           <el-button type="primary" @click="toggleVideo">
             {{ isVideoActive ? '停止摄像头' : '开启摄像头' }}
           </el-button>
        </div>
        <div class="video-container" v-if="isVideoActive">
          <img :src="videoUrl" class="video-feed" />
        </div>
        <div v-else class="video-placeholder">
          <el-icon :size="50"><VideoCamera /></el-icon>
          <p>点击按钮开启摄像头进行实时检测</p>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.upload-area {
  text-align: center;
  margin-bottom: 20px;
}
.result-area {
  margin-top: 20px;
}
.result-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 16px;
}
.video-container {
  text-align: center;
  margin-top: 20px;
}
.video-feed {
  max-width: 100%;
  border: 2px solid #ccc;
}
.video-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #eee;
  color: #999;
}
</style>

