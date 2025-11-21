<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, Lock } from '@element-plus/icons-vue'
import api from '@/api/axios'

const router = useRouter()

const step = ref(1) // 1: 输入邮箱, 2: 输入验证码, 3: 重置密码
const email = ref('')
const code = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const countdown = ref(0)
const sending = ref(false)

const formRef = ref(null)

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== newPassword.value) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const sendCode = async () => {
  if (!formRef.value) return
  
  await formRef.value.validateField('email', async (valid) => {
    if (valid) {
      sending.value = true
      try {
        await api.post('/password/send-code', {
          email: email.value
        })
        ElMessage.success('验证码已发送到邮箱')
        step.value = 2
        startCountdown()
      } catch (e) {
        // Error handled
      } finally {
        sending.value = false
      }
    }
  })
}

const verifyCode = async () => {
  if (!formRef.value) return
  
  await formRef.value.validateField('code', async (valid) => {
    if (valid) {
      try {
        await api.post('/password/verify-code', {
          email: email.value,
          code: code.value
        })
        ElMessage.success('验证码验证成功')
        step.value = 3
      } catch (e) {
        // Error handled
      }
    }
  })
}

const resetPassword = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await api.post('/password/reset', {
          email: email.value,
          code: code.value,
          new_password: newPassword.value
        })
        ElMessage.success('密码重置成功，请登录')
        router.push('/login')
      } catch (e) {
        // Error handled
      }
    }
  })
}

const startCountdown = () => {
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}
</script>

<template>
  <div class="forgot-password-container">
    <div class="forgot-password-wrapper">
      <div class="forgot-password-card">
        <div class="card-header">
          <div class="logo-large">🔐</div>
          <h1 class="card-title">找回密码</h1>
          <div class="step-indicator">
            <div :class="['step', { active: step >= 1 }]">1</div>
            <div class="step-line"></div>
            <div :class="['step', { active: step >= 2 }]">2</div>
            <div class="step-line"></div>
            <div :class="['step', { active: step >= 3 }]">3</div>
          </div>
        </div>

        <!-- Step 1: 输入邮箱 -->
        <div v-if="step === 1" class="step-content">
          <el-form ref="formRef" :model="{ email }" :rules="{ email: rules.email }" label-width="0">
            <el-form-item prop="email">
              <el-input 
                v-model="email" 
                placeholder="请输入注册邮箱" 
                size="large"
                class="ins-input"
              >
                <template #prefix>
                  <el-icon><Message /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                :loading="sending"
                class="action-btn" 
                size="large"
                @click="sendCode"
              >
                {{ sending ? '发送中...' : '发送验证码' }}
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- Step 2: 输入验证码 -->
        <div v-if="step === 2" class="step-content">
          <el-form ref="formRef" :model="{ code }" :rules="{ code: rules.code }" label-width="0">
            <el-form-item prop="code">
              <el-input 
                v-model="code" 
                placeholder="请输入6位验证码" 
                size="large"
                maxlength="6"
                class="ins-input"
              >
                <template #prefix>
                  <el-icon><Message /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                class="action-btn" 
                size="large"
                @click="verifyCode"
              >
                验证
              </el-button>
              <el-button 
                text
                class="resend-btn"
                :disabled="countdown > 0"
                @click="sendCode"
              >
                {{ countdown > 0 ? `${countdown}秒后重发` : '重新发送' }}
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- Step 3: 重置密码 -->
        <div v-if="step === 3" class="step-content">
          <el-form 
            ref="formRef" 
            :model="{ newPassword, confirmPassword }" 
            :rules="{ newPassword: rules.newPassword, confirmPassword: rules.confirmPassword }" 
            label-width="0"
          >
            <el-form-item prop="newPassword">
              <el-input 
                v-model="newPassword" 
                type="password" 
                placeholder="请输入新密码" 
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
                v-model="confirmPassword" 
                type="password" 
                placeholder="请确认新密码" 
                size="large"
                show-password
                class="ins-input"
                @keyup.enter="resetPassword"
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                class="action-btn" 
                size="large"
                @click="resetPassword"
              >
                重置密码
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <div class="card-footer">
          <router-link to="/login" class="back-link">返回登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.forgot-password-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.forgot-password-wrapper {
  width: 100%;
  max-width: 480px;
}

.forgot-password-card {
  background: var(--ins-white);
  border-radius: var(--ins-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  padding: 48px 40px;
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-large {
  font-size: 64px;
  line-height: 1;
  margin-bottom: 16px;
}

.card-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 24px 0;
  color: var(--ins-text-primary);
}

.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.step {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--ins-bg);
  border: 2px solid var(--ins-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--ins-text-secondary);
  transition: all 0.3s ease;
}

.step.active {
  background: var(--ins-accent);
  border-color: var(--ins-accent);
  color: white;
}

.step-line {
  width: 40px;
  height: 2px;
  background: var(--ins-border);
}

.step-content {
  margin-bottom: 24px;
}

.action-btn {
  width: 100%;
  height: 44px;
  border-radius: var(--ins-radius-small);
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 12px;
}

.resend-btn {
  width: 100%;
  color: var(--ins-text-secondary);
  font-size: 14px;
}

.card-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid var(--ins-border);
}

.back-link {
  color: var(--ins-accent);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: var(--ins-accent-hover);
}

.forgot-password-card :deep(.el-input__wrapper) {
  border-radius: var(--ins-radius-small);
  box-shadow: 0 0 0 1px var(--ins-border);
}

.forgot-password-card :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 2px var(--ins-accent);
}
</style>

