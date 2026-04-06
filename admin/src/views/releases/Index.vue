<template>
  <div>
    <h2 style="margin-bottom:20px;">软件安装包</h2>
    <el-table :data="files" v-loading="loading" stripe>
      <el-table-column prop="key" label="文件路径" min-width="400" />
      <el-table-column label="大小" width="120">
        <template #default="{ row }">{{ formatSize(row.size) }}</template>
      </el-table-column>
      <el-table-column prop="last_modified" label="最后修改" width="200" />
      <el-table-column label="操作" width="140" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" text @click="copyCdnLink(row)">复制链接</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getReleases } from '@/api'

const CDN_DOMAIN = 'releases.linscio.com.cn'

const loading = ref(false)
const files = ref<any[]>([])

function formatSize(bytes: number) {
  if (!bytes) return '-'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

function copyCdnLink(row: any) {
  const path = row.key.startsWith('/') ? row.key : `/${row.key}`
  const url = `https://${CDN_DOMAIN}${path}`
  navigator.clipboard.writeText(url).then(() => {
    ElMessage.success('CDN 链接已复制')
  }).catch(() => {
    ElMessage.warning('复制失败，请手动复制：' + url)
  })
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
