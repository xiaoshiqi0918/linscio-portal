<template>
  <div class="page">
    <h1 class="page__title">我的学科包</h1>
    <p class="page__subtitle">查看已购学科包及安装状态</p>

    <div v-if="loading" class="text-center text-muted mt-3">加载中...</div>
    <div v-else-if="!specialties.length" class="card text-center">
      <p class="text-muted">暂无已购学科包</p>
      <router-link to="/license/activate" class="btn btn--primary mt-2">激活学科包授权码</router-link>
    </div>

    <div v-else class="spec-grid">
      <div v-for="s in specialties" :key="s.id" class="card spec-card">
        <h3>{{ s.name || s.id }}</h3>
        <div class="info-row"><span>远程版本</span><span>{{ s.remote_version || '-' }}</span></div>
        <div class="info-row"><span>本地版本</span><span>{{ s.local_version || '未安装或软件未启动' }}</span></div>
        <div class="info-row">
          <span>状态</span>
          <span v-if="!s.local_version" class="text-muted">未安装</span>
          <span v-else-if="s.local_version === s.remote_version" style="color: var(--success)">已是最新</span>
          <span v-else style="color: var(--warning)">有更新</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { licenseStatusAll } from '@/api'

const loading = ref(true)
const specialties = ref<any[]>([])

onMounted(async () => {
  try {
    const { data } = await licenseStatusAll()
    // Flatten specialties from all products — would need specialties data from status
    // For now, show placeholder
  } catch {}
  loading.value = false
})
</script>

<style scoped lang="scss">
.spec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
.spec-card h3 { font-size: 16px; margin-bottom: 12px; }
.info-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  font-size: 13px;
}
</style>
