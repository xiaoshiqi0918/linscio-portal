<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h1 class="auth-title">忘记密码</h1>
      <p class="auth-subtitle text-muted">输入您的注册邮箱，我们将发送重置链接</p>

      <div v-if="error" class="alert alert--error">{{ error }}</div>
      <div v-if="sent" class="alert alert--success">重置链接已发送到您的邮箱，请在 30 分钟内完成重置。如未收到，请检查垃圾邮件。</div>

      <form v-if="!sent" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" class="form-input" placeholder="name@example.com" required />
        </div>
        <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
          {{ loading ? '发送中...' : '发送重置链接' }}
        </button>
      </form>
      <div class="auth-links mt-2">
        <router-link to="/login">返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authForgotPassword } from '@/api'

const email = ref('')
const loading = ref(false)
const error = ref('')
const sent = ref(false)

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    await authForgotPassword({ email: email.value })
    sent.value = true
  } catch (e: any) {
    error.value = e.response?.data?.detail || '请求失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; }
.auth-card { width: 100%; max-width: 420px; }
.auth-title { font-size: 24px; font-weight: 600; margin-bottom: 4px; }
.auth-subtitle { margin-bottom: 24px; }
.auth-links { font-size: 13px; }
</style>
