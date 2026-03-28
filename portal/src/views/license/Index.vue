<template>
  <div class="page">
    <h1 class="page__title">我的授权</h1>
    <p class="page__subtitle">查看您的产品授权状态</p>

    <div v-if="loading" class="text-center text-muted mt-3">加载中...</div>

    <div v-else class="license-grid">
      <div v-for="lic in licenses" :key="lic.product_id" class="card license-card">
        <div class="license-card__header">
          <h3>{{ lic.product_name }}</h3>
          <span class="badge" :class="statusClass(lic.status)">{{ statusText(lic.status) }}</span>
        </div>

        <div v-if="lic.status !== 'not_activated'" class="license-card__body">
          <div class="info-row">
            <span class="info-label">到期时间</span>
            <span>{{ lic.expires_at ? formatDate(lic.expires_at) : '-' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">剩余天数</span>
            <span>{{ lic.days_remaining ?? '-' }} 天</span>
          </div>
          <div class="info-row">
            <span class="info-label">绑定设备</span>
            <span>{{ lic.device_name || '未绑定' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">剩余换绑</span>
            <span>{{ lic.rebind_remaining ?? '-' }} 次</span>
          </div>
        </div>

        <div v-else class="license-card__body">
          <p class="text-muted">尚未激活此产品，请使用授权码激活。</p>
        </div>

        <div class="license-card__footer">
          <router-link to="/license/activate" class="btn btn--primary">
            {{ lic.status === 'not_activated' ? '激活授权码' : '续费 / 激活' }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { licenseStatusAll } from '@/api'

interface LicenseInfo {
  product_id: string
  product_name: string
  status: string
  is_trial: boolean
  expires_at: string | null
  days_remaining: number | null
  device_name: string | null
  rebind_remaining: number | null
}

const loading = ref(true)
const licenses = ref<LicenseInfo[]>([])

onMounted(async () => {
  try {
    const { data } = await licenseStatusAll()
    licenses.value = data.licenses
  } catch { /* handled by interceptor */ }
  loading.value = false
})

function statusClass(s: string) {
  const map: Record<string, string> = {
    valid: 'badge--valid', expired: 'badge--expired',
    trial: 'badge--trial', not_activated: 'badge--inactive',
  }
  return map[s] || ''
}

function statusText(s: string) {
  const map: Record<string, string> = {
    valid: '有效', expired: '已到期', trial: '试用中', not_activated: '未激活',
  }
  return map[s] || s
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN')
}
</script>

<style scoped lang="scss">
.license-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

.license-card {
  display: flex;
  flex-direction: column;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h3 { font-size: 18px; font-weight: 600; }
  }

  &__body {
    flex: 1;
    margin-bottom: 16px;
  }

  &__footer {
    display: flex;
    gap: 8px;
  }
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 13px;
  border-bottom: 1px solid var(--border);

  &:last-child { border-bottom: none; }
}

.info-label { color: var(--text-secondary); }
</style>
