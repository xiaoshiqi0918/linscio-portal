<template>
  <div class="auth-page">
    <p class="muted">正在退出…</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { authLogout } from '@/api'

const auth = useAuthStore()
const wwwUrl = import.meta.env.VITE_URL_WWW || '/'

onMounted(async () => {
  try {
    await authLogout()
  } catch {
    /* 会话已失效时仍清理本地状态 */
  }
  auth.clearSession()
  window.location.replace(wwwUrl)
})
</script>

<style scoped lang="scss">
.auth-page {
  min-height: 40vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.muted {
  color: var(--text-muted, #888);
  font-size: 14px;
}
</style>
