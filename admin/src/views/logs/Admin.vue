<template>
  <div class="page-container">
    <h2>管理员操作日志</h2>
    <el-table :data="logs" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="admin_email" label="操作人" min-width="160" />
      <el-table-column prop="action" label="操作" width="160" />
      <el-table-column prop="target_type" label="对象类型" width="120" />
      <el-table-column prop="target_id" label="对象 ID" width="120" />
      <el-table-column prop="detail" label="详情" min-width="240" show-overflow-tooltip />
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

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/admin-logs')
    logs.value = res.data?.items || res.data || []
  } catch { /* empty */ }
  loading.value = false
})
</script>

<style scoped>
.page-container { padding: 20px; }
</style>
