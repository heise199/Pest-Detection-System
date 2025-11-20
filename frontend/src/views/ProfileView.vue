<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import api from '@/api/axios'

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
  // Direct download link
  window.open(`http://127.0.0.1:8000/detection/report/${id}`, '_blank')
}

onMounted(fetchHistory)
</script>

<template>
  <div class="profile-container">
    <el-card class="info-card">
      <template #header>个人信息</template>
      <p><strong>用户名:</strong> {{ userStore.user.username }}</p>
      <p><strong>邮箱:</strong> {{ userStore.user.email || '未设置' }}</p>
      <p><strong>角色:</strong> {{ userStore.isAdmin ? '管理员' : '普通用户' }}</p>
      <p><strong>注册时间:</strong> {{ new Date(userStore.user.created_at).toLocaleDateString() }}</p>
    </el-card>

    <el-card class="history-card">
      <template #header>检测历史记录</template>
      <el-table :data="history" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="scope">
            {{ new Date(scope.row.created_at).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="detection_type" label="类型" width="100" />
        <el-table-column label="结果概要">
            <template #default="scope">
                <span v-if="scope.row.result_json">
                    {{ Object.keys(scope.row.result_json).join(', ') }}
                </span>
                <span v-else>无</span>
            </template>
        </el-table-column>
        <el-table-column label="图片预览" width="120">
             <template #default="scope">
                 <el-image 
                    v-if="scope.row.image_path"
                    style="width: 50px; height: 50px"
                    :src="`http://127.0.0.1:8000/${scope.row.image_path}`"
                    :preview-src-list="[`http://127.0.0.1:8000/${scope.row.image_path}`]"
                 />
             </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" type="primary" @click="downloadReport(scope.row.id)">
              下载报告
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.info-card {
  margin-bottom: 20px;
}
.history-card {
  
}
</style>

