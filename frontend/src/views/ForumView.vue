<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { ElMessage } from 'element-plus'
import { ChatDotSquare, Star } from '@element-plus/icons-vue'

const posts = ref([])
const dialogVisible = ref(false)
const newPost = ref({ title: '', content: '' })
const loading = ref(false)

// Comment logic
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
    <div class="header-actions">
      <h2>社区论坛</h2>
      <el-button type="primary" @click="dialogVisible = true">发布新帖</el-button>
    </div>
    
    <div v-loading="loading" class="post-list">
      <el-card v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <span class="post-title">{{ post.title }}</span>
          <span class="post-author">By {{ post.username }} at {{ new Date(post.created_at).toLocaleString() }}</span>
        </div>
        <div class="post-content">
          {{ post.content }}
        </div>
        <div class="post-actions">
          <el-button text @click="handleLike(post)">
             <el-icon><Star /></el-icon> {{ post.likes_count }} 点赞
          </el-button>
          <el-button text @click="toggleComments(post.id)">
             <el-icon><ChatDotSquare /></el-icon> {{ post.comments.length }} 评论
          </el-button>
        </div>
        
        <!-- Comments Section -->
        <div v-if="expandedPostId === post.id" class="comments-section">
          <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
            <strong>{{ comment.username }}:</strong> {{ comment.content }}
          </div>
          <div class="add-comment">
            <el-input v-model="newComment" placeholder="写下你的评论..." class="comment-input">
              <template #append>
                <el-button @click="handleAddComment(post)">发送</el-button>
              </template>
            </el-input>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Create Post Dialog -->
    <el-dialog v-model="dialogVisible" title="发布新帖" width="50%">
      <el-form label-position="top">
        <el-form-item label="标题">
          <el-input v-model="newPost.title" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="newPost.content" type="textarea" :rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreatePost">发布</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.post-card {
  margin-bottom: 20px;
}
.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.post-title {
  font-size: 18px;
  font-weight: bold;
}
.post-author {
  color: #999;
  font-size: 12px;
}
.post-content {
  margin-bottom: 15px;
  line-height: 1.5;
}
.comments-section {
  margin-top: 15px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
}
.comment-item {
  margin-bottom: 5px;
  font-size: 14px;
}
.add-comment {
  margin-top: 10px;
}
</style>

