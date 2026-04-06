<template>
  <div class="page">
    <h1 class="page__title">下载</h1>

    <div v-if="loading" class="text-center text-muted mt-3">处理中...</div>

    <!-- 登录提示 -->
    <div v-else-if="needLogin" class="card">
      <div class="alert alert--error">请先登录后再下载</div>
      <p class="mt-2">
        <router-link :to="loginLink" class="btn btn--primary">登录后继续</router-link>
      </p>
    </div>

    <!-- 下载成功 -->
    <div v-else-if="downloadUrl" class="card text-center">
      <div class="alert alert--success">正在为您下载 v{{ productVersion }}...</div>
      <p class="mt-2 text-muted">如果下载没有自动开始，请
        <a :href="downloadUrl" target="_blank">点击此处</a>
      </p>
      <p v-if="redirectUrl" class="mt-2">
        <a :href="redirectUrl" class="btn btn--outline">返回产品页</a>
      </p>
    </div>

    <!-- 错误 -->
    <div v-else-if="error" class="card">
      <div class="alert alert--error">{{ error }}</div>
      <p class="mt-2 text-muted">
        如需获取授权，请联系我们：<a href="mailto:linscio@163.com">linscio@163.com</a>
      </p>
    </div>

    <!-- 产品信息一览（登录后，非自动下载模式） -->
    <template v-if="!loading && !downloadUrl && !error && auth.isLoggedIn">
      <!-- 客户端下载 -->
      <section v-if="productInfo" class="section">
        <h2 class="section__title">MedComm 客户端 <span class="version-tag">v{{ productInfo.latest_version }}</span></h2>
        <div class="download-grid">
          <div v-for="p in clientPlatforms" :key="p.id" class="download-item" :class="{ 'download-item--disabled': p.status === 'suspended' }">
            <div class="download-item__name">{{ p.name }}</div>
            <div class="download-item__meta">{{ p.filename || '暂无' }}</div>
            <button v-if="p.status !== 'suspended'" class="btn btn--primary btn--sm" @click="startDownload('software', p.id)">下载</button>
            <span v-else class="text-muted" style="font-size: 13px;">暂未开放</span>
          </div>
        </div>
      </section>

      <!-- 学科包 -->
      <section v-if="specialtyList.length" class="section">
        <h2 class="section__title">学科包</h2>
        <div class="download-grid">
          <div v-for="s in specialtyList" :key="s.id" class="download-item">
            <div class="download-item__name">{{ s.name }}</div>
            <div class="download-item__meta">v{{ s.version }} · {{ s.size_mb ? s.size_mb + ' MB' : '' }}</div>
            <div class="download-item__desc">{{ s.description }}</div>
          </div>
        </div>
      </section>

      <!-- 绘图包 -->
      <section v-if="drawingPackList.length" class="section">
        <h2 class="section__title">MedPic 绘图包</h2>
        <div class="download-grid">
          <div v-for="d in drawingPackList" :key="d.id" class="download-item">
            <div class="download-item__name">{{ d.name }}</div>
            <div class="download-item__meta">v{{ d.version }} · {{ d.size_mb ? d.size_mb + ' MB' : '' }}</div>
            <div class="download-item__desc">{{ d.description }}</div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { downloadSoftware } from '@/api'
import api from '@/api'

const route = useRoute()
const auth = useAuthStore()
const loading = ref(true)
const error = ref('')
const needLogin = ref(false)
const downloadUrl = ref('')
const productVersion = ref('')

const productInfo = ref<any>(null)

interface ClientPlatform { id: string; name: string; filename: string; status: string }
const clientPlatforms = ref<ClientPlatform[]>([])

const specialtyList = ref<any[]>([])
const drawingPackList = ref<any[]>([])

const redirectUrl = computed(() => (route.query.redirect as string) || '')

const loginLink = computed(() => {
  const currentPath = route.fullPath
  return `/login?redirect=${encodeURIComponent(currentPath)}`
})

const platformLabels: Record<string, string> = {
  'mac-arm64': 'macOS（Apple Silicon）',
  'mac-x64': 'macOS（Intel）',
  'win-x64': 'Windows（x64）',
}

onMounted(async () => {
  const product = ((route.query.product as string) || 'medcomm').toLowerCase()
  const platform = (route.query.platform as string) || ''
  const autoDownload = !!platform

  try {
    const infoRes = await api.get('/api/download/product-info')
    const data = infoRes.data || {}
    const products = data.products || {}
    const matched = products[product] || products.MedComm || products.medcomm
    if (matched) {
      productVersion.value = matched.latest_version || ''
      productInfo.value = matched

      const files = matched.download_files || {}
      const statusMap = matched.platform_status || {}
      const platIds = matched.platforms || Object.keys(files)
      const allPlats = new Set([...platIds, ...Object.keys(statusMap)])
      clientPlatforms.value = [...allPlats].map(pid => ({
        id: pid,
        name: platformLabels[pid] || pid,
        filename: files[pid] || '',
        status: statusMap[pid] || 'available',
      }))
    }

    specialtyList.value = (data.specialties || []).filter((s: any) => s.product_id?.toLowerCase() === product)
    drawingPackList.value = (data.drawing_packs || []).filter((d: any) => d.product_id?.toLowerCase() === product)
  } catch { /* fallback */ }

  if (!auth.isLoggedIn) {
    if (autoDownload) {
      needLogin.value = true
    }
    loading.value = false
    return
  }

  if (autoDownload) {
    await startDownload('software', platform)
  }
  loading.value = false
})

async function startDownload(type: string, platform: string) {
  const product = ((route.query.product as string) || 'medcomm').toLowerCase()
  loading.value = true
  error.value = ''
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
}

function detectPlatform(): string {
  const ua = navigator.userAgent.toLowerCase()
  if (ua.includes('mac')) return navigator.userAgent.includes('ARM') ? 'mac-arm64' : 'mac-x64'
  return 'win-x64'
}
</script>

<style scoped>
.section { margin-top: 28px; }
.section__title { font-size: 16px; font-weight: 600; margin-bottom: 14px; }
.version-tag {
  font-size: 12px; font-weight: 400; color: #6b7280;
  background: #f3f4f6; padding: 2px 8px; border-radius: 4px; margin-left: 8px;
}
.download-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.download-item {
  border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px;
  &--disabled { opacity: 0.5; }
}
.download-item__name { font-size: 14px; font-weight: 500; margin-bottom: 4px; }
.download-item__meta { font-size: 12px; color: #9ca3af; margin-bottom: 8px; }
.download-item__desc { font-size: 12px; color: #6b7280; line-height: 1.6; }
.btn--sm { padding: 6px 18px; font-size: 13px; }
</style>
