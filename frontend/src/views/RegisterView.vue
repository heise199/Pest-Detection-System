<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Message, Lock } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()

const formRef = ref(null)
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }]
}

const loading = ref(false)

const handleRegister = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await userStore.register(form.username, form.email, form.password)
        ElMessage.success('注册成功，请登录')
        router.push('/login')
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
  <div class="register-container">
    <div class="register-wrapper">
      <div class="register-card">
        <div class="register-header">
          <div class="logo-large">🐛</div>
          <h1 class="register-title">加入 PestDetect</h1>
          <p class="register-subtitle">创建账号开始使用</p>
        </div>
        <el-form ref="formRef" :model="form" :rules="rules" label-width="0" class="register-form">
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
          <el-form-item prop="email">
            <el-input 
              v-model="form.email" 
              placeholder="邮箱 (可选)" 
              size="large"
              class="ins-input"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
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
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="confirmPassword">
            <el-input 
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="确认密码" 
              size="large"
              show-password
              class="ins-input"
              @keyup.enter="handleRegister"
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
              class="register-btn" 
              size="large"
              @click="handleRegister"
            >
              {{ loading ? '注册中...' : '注册' }}
            </el-button>
          </el-form-item>
          <div class="register-footer">
            <span class="login-link">
              已有账号？
              <router-link to="/login" class="link">立即登录</router-link>
            </span>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-wrapper {
  width: 100%;
  max-width: 420px;
}

.register-card {
  background: var(--ins-white);
  border-radius: var(--ins-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  padding: 48px 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-large {
  font-size: 64px;
  line-height: 1;
  margin-bottom: 16px;
}

.register-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--ins-text-primary);
  letter-spacing: -1px;
}

.register-subtitle {
  font-size: 15px;
  color: var(--ins-text-secondary);
  margin: 0;
}

.register-form {
  margin-top: 32px;
}

.register-form :deep(.el-input__wrapper) {
  border-radius: var(--ins-radius-small);
  box-shadow: 0 0 0 1px var(--ins-border);
  transition: all 0.2s ease;
}

.register-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--ins-text-secondary);
}

.register-form :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 2px var(--ins-accent);
}

.register-btn {
  width: 100%;
  height: 44px;
  border-radius: var(--ins-radius-small);
  font-weight: 600;
  font-size: 15px;
  background: var(--ins-accent);
  border: none;
  transition: all 0.2s ease;
}

.register-btn:hover {
  background: var(--ins-accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 149, 246, 0.3);
}

.register-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--ins-border);
}

.login-link {
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
</style>

