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
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" text @click="handleToggle(row)">
            {{ row.is_active ? '下架' : '上架' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProducts, updateProduct } from '@/api'

const loading = ref(false)
const products = ref<any[]>([])

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
