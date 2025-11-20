<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'

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
    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="害虫百科管理" name="pests">
        <div class="mb-20">
          <el-button type="primary" @click="dialogVisible = true">添加害虫信息</el-button>
        </div>
        <el-table :data="pests" style="width: 100%" v-loading="loading">
          <el-table-column prop="name" label="名称" width="150" />
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
          <el-table-column prop="control_methods" label="防治方法" show-overflow-tooltip />
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="用户管理" name="users">
        <el-table :data="users" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" width="150" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="is_admin" label="管理员" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_admin ? 'danger' : 'info'">
                {{ scope.row.is_admin ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="注册时间">
             <template #default="scope">
                {{ new Date(scope.row.created_at).toLocaleString() }}
             </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- Add Pest Dialog -->
    <el-dialog v-model="dialogVisible" title="添加害虫信息" width="50%">
      <el-form :model="newPest" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="newPest.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="newPest.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="防治方法">
          <el-input v-model="newPest.control_methods" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="图片URL">
           <el-input v-model="newPest.image_url" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreatePest">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.mb-20 {
  margin-bottom: 20px;
}
</style>

