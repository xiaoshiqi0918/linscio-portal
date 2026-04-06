<template>
  <div class="page-container">
    <h2>下载日志</h2>
    <el-table :data="logs" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="user_email" label="用户" min-width="160" />
      <el-table-column prop="download_type" label="类型" width="120">
        <template #default="{ row }">
          <el-tag size="small" :type="typeTag(row.download_type)">{{ row.download_type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="product_id" label="产品" width="120" />
      <el-table-column prop="filename" label="文件名" min-width="240" show-overflow-tooltip />
      <el-table-column prop="platform" label="平台" width="110" />
      <el-table-column prop="created_at" label="时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString('zh-CN') }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const logs = ref<any[]>([])

function typeTag(type: string) {
  const map: Record<string, string> = {
    software: '', bundle: 'success', specialty: 'warning', drawing_pack: 'info',
  }
  return map[type] || 'info'
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/download-logs')
    logs.value = res.data?.items || res.data || []
  } catch { /* empty */ }
  loading.value = false
})
</script>

<style scoped>
.page-container { padding: 20px; }
</style>
