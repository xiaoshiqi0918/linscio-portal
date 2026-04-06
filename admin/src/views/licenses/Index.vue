<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
      <h2>授权码管理</h2>
      <el-button type="primary" @click="$router.push('/licenses/generate')">生成授权码</el-button>
    </div>

    <el-table :data="items" v-loading="loading" stripe>
      <el-table-column prop="code" label="授权码" width="260">
        <template #default="{ row }">
          <code style="font-size: 12px;">{{ row.code }}</code>
        </template>
      </el-table-column>
      <el-table-column prop="product_id" label="产品" width="100" />
      <el-table-column prop="license_type" label="类型" width="90" />
      <el-table-column label="时长" width="100">
        <template #default="{ row }">
          <span v-if="row.is_trial && row.duration_days">{{ row.duration_days }} 天</span>
          <span v-else-if="row.duration_months">{{ row.duration_months }} 个月</span>
          <span v-else>--</span>
        </template>
      </el-table-column>
      <el-table-column label="试用" width="70">
        <template #default="{ row }">{{ row.is_trial ? '是' : '否' }}</template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_activated ? 'success' : 'info'" size="small">
            {{ row.is_activated ? '已激活' : '未激活' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="recipient_note" label="备注" min-width="150" />
      <el-table-column prop="created_at" label="创建时间" width="170" />
      <el-table-column label="操作" width="80" fixed="right">
        <template #default="{ row }">
          <el-button v-if="!row.is_activated" type="danger" size="small" text @click="handleVoid(row)">作废</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > pageSize" :current-page="page" :page-size="pageSize" :total="total"
      layout="prev, pager, next" style="margin-top:16px;justify-content:flex-end;"
      @current-change="(p: number) => { page = p; fetchData() }"
    />

    <!-- Generate dialog -->
    <el-dialog v-model="showGenerate" title="生成授权码" width="480px">
      <el-form :model="genForm" label-width="100px">
        <el-form-item label="产品">
          <el-select v-model="genForm.product_id" placeholder="选择产品">
            <el-option v-for="p in products" :key="p.product_id" :label="p.name" :value="p.product_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="genForm.license_type">
            <el-option label="基础版" value="basic" />
            <el-option label="学科包" value="specialty" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="genForm.license_type === 'basic'" label="时长(月)">
          <el-input-number v-model="genForm.duration_months" :min="1" :max="120" />
        </el-form-item>
        <el-form-item v-if="genForm.license_type === 'basic'" label="试用码">
          <el-switch v-model="genForm.is_trial" />
        </el-form-item>
        <el-form-item v-if="genForm.license_type === 'basic' && genForm.is_trial" label="试用天数">
          <span>1 天（固定）</span>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="genForm.count" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="genForm.recipient_note" placeholder="发给谁（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showGenerate = false">取消</el-button>
        <el-button type="primary" :loading="genLoading" @click="handleGenerate">生成</el-button>
      </template>
    </el-dialog>

    <!-- Generated codes dialog -->
    <el-dialog v-model="showCodes" title="已生成的授权码" width="500px">
      <div v-for="c in generatedCodes" :key="c" style="padding:4px 0;font-family:monospace;">{{ c }}</div>
      <template #footer>
        <el-button type="primary" @click="handleCopyCodes">复制全部</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getLicenses, generateLicenses, voidLicenseCode, getProducts } from '@/api'

const loading = ref(false)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const items = ref<any[]>([])
const products = ref<any[]>([])

const showGenerate = ref(false)
const genLoading = ref(false)
const genForm = reactive({
  product_id: '', license_type: 'basic',
  count: 1, duration_months: 12, duration_days: 1, is_trial: false,
  recipient_note: '',
})
const showCodes = ref(false)
const generatedCodes = ref<string[]>([])

async function fetchData() {
  loading.value = true
  try {
    const { data } = await getLicenses({ page: page.value, size: pageSize })
    items.value = data.items
    total.value = data.total
  } catch {}
  loading.value = false
}

async function handleGenerate() {
  genLoading.value = true
  try {
    const payload: any = { ...genForm }
    if (payload.is_trial) {
      delete payload.duration_months
    } else {
      delete payload.duration_days
    }
    const { data } = await generateLicenses(payload)
    generatedCodes.value = data.codes
    showGenerate.value = false
    showCodes.value = true
    fetchData()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '生成失败')
  } finally {
    genLoading.value = false
  }
}

function handleCopyCodes() {
  navigator.clipboard.writeText(generatedCodes.value.join('\n'))
  ElMessage.success('已复制到剪贴板')
}

async function handleVoid(row: any) {
  try {
    await ElMessageBox.confirm(`确定作废授权码 ${row.code}？`, '确认', { type: 'warning' })
    await voidLicenseCode(row.id)
    ElMessage.success('已作废')
    fetchData()
  } catch {}
}

onMounted(async () => {
  fetchData()
  try {
    const { data } = await getProducts()
    products.value = data.products || []
    if (products.value.length && !genForm.product_id) {
      genForm.product_id = products.value[0].product_id
    }
  } catch {}
})
</script>
