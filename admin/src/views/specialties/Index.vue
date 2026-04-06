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
      <el-table-column label="强制最高版本" width="130">
        <template #default="{ row }">
          {{ row.version_policy?.force_max_version || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="170" />
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" text @click="openEdit(row)">策略</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="editVisible" title="编辑版本策略" width="460px">
      <el-form :model="editForm" label-width="110px">
        <el-form-item label="学科包">
          <span>{{ editForm.name }} ({{ editForm.id }})</span>
        </el-form-item>
        <el-form-item label="强制最低版本">
          <el-input v-model="editForm.force_min_version" placeholder="如 2.0.0，留空不限制" clearable />
        </el-form-item>
        <el-form-item label="强制最高版本">
          <el-input v-model="editForm.force_max_version" placeholder="如 3.0.0，留空不限制（紧急回退用）" clearable />
        </el-form-item>
        <el-form-item label="策略提示">
          <el-input v-model="editForm.policy_message" type="textarea" :rows="2" placeholder="提示信息（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="savePolicy">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSpecialties, updateSpecialtyPolicy } from '@/api'

const loading = ref(false)
const specialties = ref<any[]>([])

const editVisible = ref(false)
const saving = ref(false)
const editForm = ref({
  id: '',
  product_id: '',
  name: '',
  force_min_version: '',
  force_max_version: '',
  policy_message: '',
})

function openEdit(row: any) {
  editForm.value = {
    id: row.id,
    product_id: row.product_id,
    name: row.name || row.id,
    force_min_version: row.version_policy?.force_min_version || '',
    force_max_version: row.version_policy?.force_max_version || '',
    policy_message: row.version_policy?.policy_message || '',
  }
  editVisible.value = true
}

async function savePolicy() {
  saving.value = true
  try {
    await updateSpecialtyPolicy(editForm.value.id, editForm.value.product_id, {
      force_min_version: editForm.value.force_min_version || null,
      force_max_version: editForm.value.force_max_version || null,
      policy_message: editForm.value.policy_message || null,
    })
    ElMessage.success('策略已更新')
    editVisible.value = false
    fetchData()
  } catch {
    ElMessage.error('更新失败')
  }
  saving.value = false
}

async function fetchData() {
  loading.value = true
  try {
    const { data } = await getSpecialties()
    specialties.value = data.specialties || []
  } catch {}
  loading.value = false
}

onMounted(fetchData)
</script>
