<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()

const formRef = ref(null)
const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const loading = ref(false)

const handleLogin = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await userStore.login(form.username, form.password)
        ElMessage.success('登录成功')
        router.push('/')
      } catch (error) {
        // Error handled by axios interceptor
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <div class="login-container">
    <div class="login-wrapper">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-large">🐛</div>
          <h1 class="login-title">PestDetect</h1>
          <p class="login-subtitle">智能害虫检测平台</p>
        </div>
        <el-form ref="formRef" :model="form" :rules="rules" label-width="0" class="login-form">
          <el-form-item prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="用户名" 
              size="large"
              class="ins-input"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="密码" 
              size="large"
              show-password
              class="ins-input"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
              :loading="loading" 
              class="login-btn" 
              size="large"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
          <div class="login-footer">
            <span class="register-link">
              没有账号？
              <router-link to="/register" class="link">立即注册</router-link>
            </span>
            <router-link to="/forgot-password" class="forgot-link">忘记密码？</router-link>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: var(--ins-white);
  border-radius: var(--ins-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  padding: 48px 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-large {
  font-size: 64px;
  line-height: 1;
  margin-bottom: 16px;
}

.login-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--ins-text-primary);
  letter-spacing: -1px;
}

.login-subtitle {
  font-size: 15px;
  color: var(--ins-text-secondary);
  margin: 0;
}

.login-form {
  margin-top: 32px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: var(--ins-radius-small);
  box-shadow: 0 0 0 1px var(--ins-border);
  transition: all 0.2s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--ins-text-secondary);
}

.login-form :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 2px var(--ins-accent);
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: var(--ins-radius-small);
  font-weight: 600;
  font-size: 15px;
  background: var(--ins-accent);
  border: none;
  transition: all 0.2s ease;
}

.login-btn:hover {
  background: var(--ins-accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 149, 246, 0.3);
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--ins-border);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.register-link {
  font-size: 14px;
  color: var(--ins-text-secondary);
}

.link {
  color: var(--ins-accent);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.link:hover {
  color: var(--ins-accent-hover);
}

.forgot-link {
  font-size: 13px;
  color: var(--ins-text-secondary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: var(--ins-accent);
}
</style>

