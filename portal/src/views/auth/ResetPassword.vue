<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h1 class="auth-title">重置密码</h1>
      <p class="auth-subtitle text-muted">请输入新密码</p>

      <div v-if="error" class="alert alert--error">{{ error }}</div>
      <div v-if="success" class="alert alert--success">密码已重置，即将跳转登录...</div>

      <form v-if="!success" @submit.prevent="handleReset">
        <div class="form-group">
          <label>新密码</label>
          <input v-model="password" type="password" class="form-input" placeholder="至少 8 位" required minlength="8" />
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input v-model="confirm" type="password" class="form-input" placeholder="再次输入新密码" required />
        </div>
        <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
          {{ loading ? '提交中...' : '重置密码' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authResetPassword } from '@/api'

const route = useRoute()
const router = useRouter()
const password = ref('')
const confirm = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)
const token = route.query.token as string | undefined

if (!token) {
  error.value = '重置链接无效或已过期，请重新申请'
}

async function handleReset() {
  error.value = ''
  if (!token) {
    error.value = '重置链接无效或已过期，请重新申请'
    return
  }
  if (password.value !== confirm.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await authResetPassword({ token, new_password: password.value })
    success.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (e: any) {
    error.value = e.response?.data?.detail || '重置失败'
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
</style>
