<template>
  <div class="page">
    <h1 class="page__title">下载</h1>

    <div v-if="loading" class="text-center text-muted mt-3">处理中...</div>

    <div v-else-if="error" class="card">
      <div class="alert alert--error">{{ error }}</div>
      <p v-if="needLogin" class="mt-2">
        <router-link to="/login" class="btn btn--primary">登录后继续</router-link>
      </p>
      <p v-else class="mt-2 text-muted">
        如需获取授权，请联系我们：<a href="mailto:linscio@163.com">linscio@163.com</a>
      </p>
    </div>

    <div v-else-if="downloadUrl" class="card text-center">
      <div class="alert alert--success">正在为您下载...</div>
      <p class="mt-2 text-muted">如果下载没有自动开始，请
        <a :href="downloadUrl" target="_blank">点击此处</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { downloadSoftware } from '@/api'

const route = useRoute()
const auth = useAuthStore()
const loading = ref(true)
const error = ref('')
const needLogin = ref(false)
const downloadUrl = ref('')

onMounted(async () => {
  const product = (route.query.product as string) || 'MedComm'
  const platform = (route.query.platform as string) || detectPlatform()

  if (!auth.isLoggedIn) {
    error.value = '请先登录后再下载'
    needLogin.value = true
    loading.value = false
    return
  }

  try {
    const { data } = await downloadSoftware({ product_id: product, platform })
    downloadUrl.value = data.download_url
    window.location.href = data.download_url
  } catch (e: any) {
    const detail = e.response?.data?.detail || ''
    if (detail === 'no_valid_license') {
      error.value = '您尚未激活此产品授权，请联系我们获取授权码'
    } else {
      error.value = detail || '下载失败'
    }
  }
  loading.value = false
})

function detectPlatform(): string {
  const ua = navigator.userAgent.toLowerCase()
  if (ua.includes('mac')) return navigator.userAgent.includes('ARM') ? 'mac-arm64' : 'mac-x64'
  return 'win-x64'
}
</script>
