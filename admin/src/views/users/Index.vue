<template>
  <div>
    <h2 style="margin-bottom:20px;">用户管理</h2>
    <el-input v-model="search" placeholder="搜索邮箱或手机号" style="width:300px;margin-bottom:16px;" clearable @change="fetchData" />

    <el-table :data="items" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="email" label="邮箱" min-width="200" />
      <el-table-column prop="phone" label="手机" width="140" />
      <el-table-column label="邮箱验证" width="90">
        <template #default="{ row }">
          <el-tag :type="row.email_verified ? 'success' : 'info'" size="small">
            {{ row.email_verified ? '已验证' : '未验证' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
            {{ row.is_active ? '正常' : '封禁' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="170" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.is_active" type="danger" size="small" text @click="handleBan(row)">封禁</el-button>
          <el-button v-else type="success" size="small" text @click="handleUnban(row)">解封</el-button>
          <el-button
            v-if="!row.is_admin"
            type="danger"
            size="small"
            text
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > pageSize"
      :current-page="page" :page-size="pageSize" :total="total"
      layout="prev, pager, next"
      style="margin-top:16px;justify-content:flex-end;"
      @current-change="(p: number) => { page = p; fetchData() }"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, banUser, unbanUser, deleteUser } from '@/api'

const loading = ref(false)
const search = ref('')
const page = ref(1)
const pageSize = 20
const total = ref(0)
const items = ref<any[]>([])

async function fetchData() {
  loading.value = true
  try {
    const { data } = await getUsers({ q: search.value, page: page.value, size: pageSize })
    items.value = data.items
    total.value = data.total
  } catch {}
  loading.value = false
}

async function handleBan(row: any) {
  try {
    await ElMessageBox.confirm(`确定封禁用户 ${row.email}？`, '封禁确认', { type: 'warning' })
    await banUser(row.id, { reason: '管理员操作' })
    ElMessage.success('已封禁')
    fetchData()
  } catch {}
}

async function handleUnban(row: any) {
  try {
    await unbanUser(row.id)
    ElMessage.success('已解封')
    fetchData()
  } catch {}
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(
      `将永久删除用户 ${row.email} 及其会话、授权、下载记录等关联数据，且不可恢复。确定继续？`,
      '删除用户',
      { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' },
    )
    await deleteUser(row.id, { reason: '管理员删除' })
    ElMessage.success('已删除')
    fetchData()
  } catch {}
}

onMounted(fetchData)
</script>
