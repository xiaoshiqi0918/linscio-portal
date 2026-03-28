<template>
  <div>
    <h2 style="margin-bottom:20px;">系统安全</h2>
    <el-table :data="items" v-loading="loading" stripe>
      <el-table-column prop="limit_type" label="限制类型" width="180" />
      <el-table-column prop="identifier" label="标识符" min-width="200" />
      <el-table-column prop="fail_count" label="失败次数" width="90" />
      <el-table-column prop="locked_until" label="锁定至" width="170" />
      <el-table-column prop="updated_at" label="更新时间" width="170" />
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button type="warning" size="small" text @click="handleUnlock(row)">解锁</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSecurityLimits, unlockSecurity } from '@/api'

const loading = ref(false)
const items = ref<any[]>([])

async function fetchData() {
  loading.value = true
  try {
    const { data } = await getSecurityLimits({})
    items.value = data.items
  } catch {}
  loading.value = false
}

async function handleUnlock(row: any) {
  try {
    await unlockSecurity({ limit_type: row.limit_type, identifier: row.identifier })
    ElMessage.success('已解锁')
    fetchData()
  } catch {}
}

onMounted(fetchData)
</script>
