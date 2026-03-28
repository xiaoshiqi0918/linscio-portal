<template>
  <div>
    <h2 style="margin-bottom:20px;">软件安装包</h2>
    <el-table :data="files" v-loading="loading" stripe>
      <el-table-column prop="key" label="文件路径" min-width="400" />
      <el-table-column label="大小" width="120">
        <template #default="{ row }">{{ formatSize(row.size) }}</template>
      </el-table-column>
      <el-table-column prop="last_modified" label="最后修改" width="200" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getReleases } from '@/api'

const loading = ref(false)
const files = ref<any[]>([])

function formatSize(bytes: number) {
  if (!bytes) return '-'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await getReleases()
    files.value = data.files || []
  } catch {}
  loading.value = false
})
</script>
