<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <h2 style="font-size: 18px; font-weight: 600;">组件包管理</h2>
      <el-button type="primary" size="small" @click="refresh">刷新 Manifest</el-button>
    </div>

    <el-card shadow="hover" style="margin-bottom: 20px;">
      <template #header>
        <span style="font-weight: 600;">Manifest 基础信息</span>
      </template>
      <el-descriptions :column="3" size="small" border>
        <el-descriptions-item label="Schema 版本">{{ manifest.schema_version || '-' }}</el-descriptions-item>
        <el-descriptions-item label="最低客户端版本">{{ manifest.min_client_version || '-' }}</el-descriptions-item>
        <el-descriptions-item label="产品数量">{{ (manifest.products || []).length }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card shadow="hover" style="margin-bottom: 20px;">
      <template #header>
        <span style="font-weight: 600;">扩展组件包</span>
      </template>
      <el-table :data="bundles" size="small" stripe>
        <el-table-column prop="id" label="ID" width="160" />
        <el-table-column prop="name" label="名称" min-width="200" />
        <el-table-column prop="type" label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.type === 'basic' ? 'success' : 'warning'" size="small">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column label="平台" width="200">
          <template #default="{ row }">
            <div v-for="(info, plat) in (row.platforms || {})" :key="plat" style="font-size: 12px; line-height: 1.8;">
              {{ plat }}: {{ info.filename || '-' }}
              <span v-if="info.size_bytes" style="color: #9ca3af;"> ({{ formatBytes(info.size_bytes) }})</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="min_client_version" label="最低客户端" width="100" />
      </el-table>
      <div v-if="!bundles.length" style="text-align:center;padding:24px;color:#9ca3af;font-size:13px;">暂无 Bundle 数据</div>
    </el-card>

    <el-row :gutter="16">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span style="font-weight: 600;">学科包</span>
          </template>
          <el-table :data="specialties" size="small" stripe>
            <el-table-column prop="id" label="ID" width="120" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="version" label="版本" width="80" />
            <el-table-column label="大小" width="80">
              <template #default="{ row }">{{ row.full_package?.size_mb ? row.full_package.size_mb + ' MB' : '-' }}</template>
            </el-table-column>
          </el-table>
          <div v-if="!specialties.length" style="text-align:center;padding:20px;color:#9ca3af;font-size:13px;">暂无数据</div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span style="font-weight: 600;">绘图包</span>
          </template>
          <el-table :data="drawingPacks" size="small" stripe>
            <el-table-column prop="id" label="ID" width="140" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="version" label="版本" width="80" />
            <el-table-column label="大小" width="80">
              <template #default="{ row }">{{ row.full_package?.size_mb ? row.full_package.size_mb + ' MB' : '-' }}</template>
            </el-table-column>
          </el-table>
          <div v-if="!drawingPacks.length" style="text-align:center;padding:20px;color:#9ca3af;font-size:13px;">暂无数据</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const manifest = ref<any>({})
const bundles = ref<any[]>([])
const specialties = ref<any[]>([])
const drawingPacks = ref<any[]>([])

function formatBytes(bytes: number): string {
  if (!bytes) return '-'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(0) + ' KB'
  if (bytes < 1024 * 1024 * 1024) return (bytes / 1024 / 1024).toFixed(1) + ' MB'
  return (bytes / 1024 / 1024 / 1024).toFixed(2) + ' GB'
}

async function refresh() {
  try {
    const { data } = await api.get('/api/download/product-info')
    manifest.value = data
    bundles.value = data.bundles || []
    specialties.value = data.specialties || []
    drawingPacks.value = data.drawing_packs || []
    ElMessage.success('Manifest 已刷新')
  } catch {
    ElMessage.error('获取 Manifest 失败')
  }
}

onMounted(refresh)
</script>
