<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { InfoFilled, Plus, Edit, Delete } from '@element-plus/icons-vue'
import { useDateFormat } from '@/composables/useDateFormat'

const { formatDate } = useDateFormat()

const pests = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const editingPest = ref(null)

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
  } catch (e) {
    ElMessage.error('获取害虫列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreatePest = async () => {
  try {
    if (editingPest.value) {
      await api.put(`/admin/pests/${editingPest.value.id}`, newPest.value)
      ElMessage.success('更新成功')
    } else {
      await api.post('/admin/pests', newPest.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    resetForm()
    fetchPests()
  } catch (e) {
    ElMessage.error(editingPest.value ? '更新失败' : '添加失败')
  }
}

const handleEdit = (pest) => {
  editingPest.value = pest
  newPest.value = {
    name: pest.name,
    description: pest.description || '',
    control_methods: pest.control_methods || '',
    image_url: pest.image_url || ''
  }
  dialogVisible.value = true
}

const handleDelete = async (id) => {
  try {
    await api.delete(`/admin/pests/${id}`)
    ElMessage.success('删除成功')
    fetchPests()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

const resetForm = () => {
  newPest.value = {
    name: '',
    description: '',
    control_methods: '',
    image_url: ''
  }
  editingPest.value = null
}

const handleDialogClose = () => {
  resetForm()
}

onMounted(fetchPests)
</script>

<template>
  <div class="admin-pests">
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
          <div class="pest-actions">
            <el-button 
              text 
              size="small"
              :icon="Edit"
              @click="handleEdit(pest)"
            >
              编辑
            </el-button>
            <el-button 
              text 
              size="small"
              type="danger"
              :icon="Delete"
              @click="handleDelete(pest.id)"
            >
              删除
            </el-button>
          </div>
        </div>
        <div class="pest-content">
          <p class="pest-description">{{ pest.description || '暂无描述' }}</p>
          <div class="pest-methods" v-if="pest.control_methods">
            <strong>防治方法：</strong>
            <p>{{ pest.control_methods }}</p>
          </div>
          <div class="pest-meta">
            <span class="meta-text">创建于 {{ formatDate(pest.created_at) }}</span>
          </div>
        </div>
      </div>
      <div v-if="pests.length === 0 && !loading" class="empty-state">
        <el-icon class="empty-icon"><InfoFilled /></el-icon>
        <p>还没有害虫信息</p>
      </div>
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      :title="editingPest ? '编辑害虫信息' : '添加害虫信息'" 
      width="600px"
      @close="handleDialogClose"
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

<style scoped>
.admin-pests {
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
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.add-btn {
  border-radius: var(--ins-radius-small);
  font-weight: 600;
}

.pest-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.pest-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 20px;
  transition: all 0.3s ease;
  box-shadow: var(--ins-shadow);
}

.pest-card:hover {
  box-shadow: var(--ins-shadow-hover);
  transform: translateY(-2px);
}

.pest-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.pest-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.pest-actions {
  display: flex;
  gap: 8px;
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

.pest-meta {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--ins-border);
}

.meta-text {
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
</style>

