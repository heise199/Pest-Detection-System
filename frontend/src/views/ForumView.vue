<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { ChatDotSquare, Star, Plus } from '@element-plus/icons-vue'

const posts = ref([])
const dialogVisible = ref(false)
const newPost = ref({ title: '', content: '' })
const loading = ref(false)

const expandedPostId = ref(null)
const newComment = ref('')

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await api.get('/forum/posts')
    posts.value = res.data
  } catch (e) {
    // Handled
  } finally {
    loading.value = false
  }
}

const handleCreatePost = async () => {
  if (!newPost.value.title || !newPost.value.content) {
    ElMessage.warning('请填写完整')
    return
  }
  try {
    await api.post('/forum/posts', newPost.value)
    ElMessage.success('发布成功')
    dialogVisible.value = false
    newPost.value = { title: '', content: '' }
    fetchPosts()
  } catch (e) {
    // Handled
  }
}

const handleLike = async (post) => {
  try {
    const res = await api.post(`/forum/posts/${post.id}/like`)
    if (res.data.message === 'Liked') {
        post.likes_count++
    } else {
        post.likes_count--
    }
  } catch (e) {
    // Handled
  }
}

const toggleComments = (postId) => {
  if (expandedPostId.value === postId) {
    expandedPostId.value = null
  } else {
    expandedPostId.value = postId
  }
}

const handleAddComment = async (post) => {
  if (!newComment.value) return
  try {
    const res = await api.post(`/forum/posts/${post.id}/comments`, { content: newComment.value })
    post.comments.push(res.data)
    newComment.value = ''
    ElMessage.success('评论成功')
  } catch (e) {
    // Handled
  }
}

onMounted(fetchPosts)
</script>

<template>
  <div class="forum-container">
    <div class="forum-header">
      <h2 class="forum-title">社区论坛</h2>
      <el-button 
        type="primary" 
        :icon="Plus"
        @click="dialogVisible = true"
        class="create-btn"
      >
        发布新帖
      </el-button>
    </div>
    
    <div v-loading="loading" class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <div class="post-author-info">
            <el-avatar :size="40" class="author-avatar">
              {{ post.username?.[0]?.toUpperCase() || 'U' }}
            </el-avatar>
            <div class="author-details">
              <div class="author-name">{{ post.username }}</div>
              <div class="post-time">{{ formatTime(post.created_at) }}</div>
            </div>
          </div>
        </div>
        <h3 class="post-title">{{ post.title }}</h3>
        <div class="post-content">
          {{ post.content }}
        </div>
        <div class="post-actions">
          <button 
            :class="['action-btn', 'like-btn']"
            @click="handleLike(post)"
          >
            <el-icon><Star /></el-icon>
            <span>{{ post.likes_count }}</span>
          </button>
          <button 
            :class="['action-btn', 'comment-btn']"
            @click="toggleComments(post.id)"
          >
            <el-icon><ChatDotSquare /></el-icon>
            <span>{{ post.comments.length }}</span>
          </button>
        </div>
        
        <div v-if="expandedPostId === post.id" class="comments-section">
          <div class="comments-list">
            <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
              <el-avatar :size="32" class="comment-avatar">
                {{ comment.username?.[0]?.toUpperCase() || 'U' }}
              </el-avatar>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.username }}</span>
                  <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
              </div>
            </div>
          </div>
          <div class="add-comment">
            <el-input 
              v-model="newComment" 
              placeholder="写下你的评论..." 
              class="comment-input"
              @keyup.enter="handleAddComment(post)"
            >
              <template #append>
                <el-button @click="handleAddComment(post)" type="primary">发送</el-button>
              </template>
            </el-input>
          </div>
        </div>
      </div>
      
      <div v-if="posts.length === 0 && !loading" class="empty-state">
        <el-icon class="empty-icon"><ChatDotSquare /></el-icon>
        <p>还没有帖子，快来发布第一个吧！</p>
      </div>
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      title="发布新帖" 
      width="600px"
      class="post-dialog"
    >
      <el-form label-position="top">
        <el-form-item label="标题">
          <el-input v-model="newPost.title" placeholder="输入帖子标题" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input 
            v-model="newPost.content" 
            type="textarea" 
            :rows="6" 
            placeholder="分享你的想法..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreatePost">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  methods: {
    formatTime(timeString) {
      const date = new Date(timeString)
      const now = new Date()
      const diff = now - date
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)
      
      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      if (days < 7) return `${days}天前`
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.forum-container {
  max-width: 800px;
  margin: 0 auto;
}

.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.forum-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.create-btn {
  border-radius: var(--ins-radius-small);
  font-weight: 600;
  padding: 10px 20px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 20px;
  box-shadow: var(--ins-shadow);
  transition: all 0.3s ease;
}

.post-card:hover {
  box-shadow: var(--ins-shadow-hover);
}

.post-header {
  margin-bottom: 16px;
}

.post-author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.author-details {
  flex: 1;
}

.author-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--ins-text-primary);
  margin-bottom: 4px;
}

.post-time {
  font-size: 13px;
  color: var(--ins-text-secondary);
}

.post-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--ins-text-primary);
}

.post-content {
  font-size: 15px;
  line-height: 1.6;
  color: var(--ins-text-primary);
  margin-bottom: 16px;
  white-space: pre-wrap;
}

.post-actions {
  display: flex;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--ins-border);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--ins-text-secondary);
  font-size: 15px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: var(--ins-radius-small);
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--ins-bg);
  color: var(--ins-text-primary);
}

.action-btn .el-icon {
  font-size: 20px;
}

.like-btn.active {
  color: #ed4956;
}

.comments-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--ins-border);
}

.comments-list {
  margin-bottom: 16px;
  max-height: 300px;
  overflow-y: auto;
}

.comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-author {
  font-size: 14px;
  font-weight: 600;
  color: var(--ins-text-primary);
}

.comment-time {
  font-size: 12px;
  color: var(--ins-text-secondary);
}

.comment-text {
  font-size: 14px;
  color: var(--ins-text-primary);
  margin: 0;
  line-height: 1.5;
}

.add-comment {
  margin-top: 12px;
}

.comment-input :deep(.el-input__wrapper) {
  border-radius: var(--ins-radius-small);
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

.post-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.post-dialog :deep(.el-input__wrapper),
.post-dialog :deep(.el-textarea__inner) {
  border-radius: var(--ins-radius-small);
}
</style>
