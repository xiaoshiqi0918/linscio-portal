<template>
  <div>
    <h2 style="margin-bottom:20px;">设备管理</h2>
    <el-input v-model="search" placeholder="搜索邮箱或设备名" style="width:300px;margin-bottom:16px;" clearable @change="fetchData" />

    <el-table :data="items" v-loading="loading" stripe>
      <el-table-column prop="email" label="用户邮箱" min-width="180" />
      <el-table-column prop="product_id" label="产品" width="100" />
      <el-table-column prop="device_name" label="设备名称" min-width="180" />
      <el-table-column prop="rebind_count" label="已换绑" width="80" />
      <el-table-column prop="last_seen_at" label="最后活跃" width="170" />
      <el-table-column prop="expires_at" label="到期时间" width="170" />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="warning" size="small" text @click="handleReset(row)">强制换绑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-if="total > 20" :current-page="page" :page-size="20" :total="total"
      layout="prev, pager, next" style="margin-top:16px;justify-content:flex-end;"
      @current-change="(p: number) => { page = p; fetchData() }" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDevices, forceRebind } from '@/api'

const loading = ref(false)
const search = ref('')
const page = ref(1)
const total = ref(0)
const items = ref<any[]>([])

async function fetchData() {
  loading.value = true
  try {
    const { data } = await getDevices({ q: search.value, page: page.value })
    items.value = data.items
    total.value = data.total
  } catch {}
  loading.value = false
}

async function handleReset(row: any) {
  try {
    await ElMessageBox.confirm(`确定为 ${row.email} 的 ${row.product_id} 强制换绑？`, '确认')
    await forceRebind({ user_id: row.user_id, product_id: row.product_id })
    ElMessage.success('已重置')
    fetchData()
  } catch {}
}

onMounted(fetchData)
</script>
