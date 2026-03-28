<template>
  <div>
    <h2 style="margin-bottom:20px;">账号迁移审批</h2>
    <el-table :data="items" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="from_user_id" label="申请用户ID" width="110" />
      <el-table-column prop="to_credential" label="目标账号" min-width="200" />
      <el-table-column prop="reason" label="原因" min-width="200" />
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 'pending' ? 'warning' : row.status === 'approved' ? 'success' : 'danger'" size="small">
            {{ { pending: '待审批', approved: '已通过', rejected: '已拒绝' }[row.status as string] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="170" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button type="success" size="small" text @click="handle(row, 'approve')">通过</el-button>
            <el-button type="danger" size="small" text @click="handle(row, 'reject')">拒绝</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getMigrations, handleMigration } from '@/api'

const loading = ref(false)
const items = ref<any[]>([])

async function fetchData() {
  loading.value = true
  try {
    const { data } = await getMigrations({ status: '' })
    items.value = data.items
  } catch {}
  loading.value = false
}

async function handle(row: any, action: string) {
  try {
    await handleMigration(row.id, { action })
    ElMessage.success(action === 'approve' ? '已通过' : '已拒绝')
    fetchData()
  } catch {}
}

onMounted(fetchData)
</script>
