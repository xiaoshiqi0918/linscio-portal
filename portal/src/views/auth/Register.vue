<template>
  <div class="auth-page">
    <div class="auth-card card">
      <template v-if="step === 'form'">
        <h1 class="auth-title">注册 LinScio</h1>
        <p class="auth-subtitle text-muted">创建您的账号</p>

        <div v-if="error" class="alert alert--error">{{ error }}</div>

        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="form.email" type="email" class="form-input" placeholder="name@example.com" required />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="form.password" type="password" class="form-input" placeholder="至少 8 位" required minlength="8" />
          </div>
          <div class="form-group">
            <label>确认密码</label>
            <input v-model="confirmPassword" type="password" class="form-input" placeholder="再次输入密码" required />
          </div>
          <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
            {{ loading ? '发送中...' : '发送验证码' }}
          </button>
        </form>
        <div class="auth-links mt-2">
          <router-link to="/login">已有账号？登录</router-link>
        </div>
      </template>

      <template v-else-if="step === 'verify'">
        <h1 class="auth-title">验证邮箱</h1>
        <p class="auth-subtitle text-muted">验证码已发送至 {{ form.email }}，请在 10 分钟内完成验证</p>

        <div v-if="error" class="alert alert--error">{{ error }}</div>
        <div v-if="success" class="alert alert--success">{{ success }}</div>

        <form @submit.prevent="handleVerify">
          <div class="form-group">
            <label>验证码</label>
            <input v-model="verifyCode" type="text" class="form-input" placeholder="6 位数字验证码" required maxlength="6" />
          </div>
          <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
            {{ loading ? '验证中...' : '完成注册' }}
          </button>
        </form>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authRegister, authVerify } from '@/api'

const router = useRouter()
const step = ref<'form' | 'verify'>('form')
const loading = ref(false)
const error = ref('')
const success = ref('')
const form = reactive({ email: '', password: '' })
const confirmPassword = ref('')
const verifyCode = ref('')

async function handleRegister() {
  error.value = ''
  if (form.password !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await authRegister(form)
    step.value = 'verify'
  } catch (e: any) {
    error.value = e.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}

async function handleVerify() {
  error.value = ''
  loading.value = true
  try {
    await authVerify({ email: form.email, code: verifyCode.value })
    success.value = '注册成功！即将跳转登录...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e: any) {
    error.value = e.response?.data?.detail || '验证失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.auth-card { width: 100%; max-width: 420px; }
.auth-title { font-size: 24px; font-weight: 600; margin-bottom: 4px; }
.auth-subtitle { margin-bottom: 24px; }
.auth-links { font-size: 13px; }
</style>
