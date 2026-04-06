<template>
  <div>
    <h2 style="margin-bottom:20px;">产品管理</h2>
    <el-table :data="products" v-loading="loading" stripe>
      <el-table-column prop="product_id" label="产品ID" width="120" />
      <el-table-column prop="name" label="名称" width="150" />
      <el-table-column prop="description" label="描述" min-width="200" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sort_order" label="排序" width="70" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" text @click="openEdit(row)">编辑</el-button>
          <el-button :type="row.is_active ? 'warning' : 'success'" size="small" text @click="handleToggle(row)">
            {{ row.is_active ? '下架' : '上架' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="editVisible" title="编辑产品" width="460px">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="产品ID">
          <span>{{ editForm.product_id }}</span>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="editForm.sort_order" :min="0" :max="99" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveProduct">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProducts, updateProduct } from '@/api'

const loading = ref(false)
const products = ref<any[]>([])

const editVisible = ref(false)
const saving = ref(false)
const editForm = ref({
  product_id: '',
  name: '',
  description: '',
  sort_order: 0,
})

function openEdit(row: any) {
  editForm.value = {
    product_id: row.product_id,
    name: row.name || '',
    description: row.description || '',
    sort_order: row.sort_order || 0,
  }
  editVisible.value = true
}

async function saveProduct() {
  saving.value = true
  try {
    await updateProduct(editForm.value.product_id, {
      name: editForm.value.name,
      description: editForm.value.description,
      sort_order: editForm.value.sort_order,
    })
    ElMessage.success('已更新')
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
    const { data } = await getProducts()
    products.value = data.products || []
  } catch {}
  loading.value = false
}

async function handleToggle(row: any) {
  try {
    await updateProduct(row.product_id, { is_active: row.is_active ? 0 : 1 })
    ElMessage.success('已更新')
    fetchData()
  } catch {}
}

onMounted(fetchData)
</script>
