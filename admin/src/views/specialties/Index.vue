<template>
  <div>
    <h2 style="margin-bottom:20px;">学科包管理</h2>
    <el-table :data="specialties" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="140" />
      <el-table-column prop="product_id" label="产品" width="100" />
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column prop="version" label="最新版本" width="100" />
      <el-table-column label="强制最低版本" width="130">
        <template #default="{ row }">
          {{ row.version_policy?.force_min_version || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="170" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSpecialties } from '@/api'

const loading = ref(false)
const specialties = ref<any[]>([])

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await getSpecialties()
    specialties.value = data.specialties || []
  } catch {}
  loading.value = false
})
</script>
