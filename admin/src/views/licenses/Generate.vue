<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">生成授权码</h1>
      <router-link to="/licenses" class="back-link">← 返回授权码列表</router-link>
    </div>

    <div class="gen-layout">
      <!-- Left: Form -->
      <div class="gen-form">
        <!-- License type -->
        <div class="form-section">
          <p class="form-label">授权类型</p>
          <div class="type-cards">
            <div
              v-for="t in licenseTypes" :key="t.value"
              :class="['type-card', { active: form.license_type === t.value }]"
              @click="form.license_type = t.value"
            >
              <h4>{{ t.label }}</h4>
              <p>{{ t.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Product -->
        <div class="form-section">
          <p class="form-label">适用产品</p>
          <select v-model="form.product_id" class="form-select">
            <option v-for="p in products" :key="p.product_id" :value="p.product_id">{{ p.name }}</option>
          </select>
        </div>

        <!-- Duration: months for basic -->
        <div v-if="form.license_type === 'basic'" class="form-section">
          <p class="form-label">授权周期</p>
          <div class="duration-options">
            <div
              v-for="d in durations" :key="d"
              :class="['duration-opt', { active: form.duration_months === d }]"
              @click="form.duration_months = d"
            >
              {{ d }}<br/>个月
            </div>
          </div>
        </div>

        <!-- Duration: fixed 1 day for trial -->
        <div v-if="form.license_type === 'trial'" class="form-section">
          <p class="form-label">试用天数</p>
          <div class="duration-options">
            <div class="duration-opt active">1<br/>天</div>
          </div>
        </div>

        <!-- Count -->
        <div class="form-section">
          <p class="form-label">生成数量</p>
          <div class="count-row">
            <div class="stepper">
              <button class="stepper-btn" @click="form.count = Math.max(1, form.count - 1)">−</button>
              <span class="stepper-val">{{ form.count }}</span>
              <button class="stepper-btn" @click="form.count = Math.min(100, form.count + 1)">+</button>
            </div>
            <span class="count-hint">批量生成时每张码独立，备注相同</span>
          </div>
        </div>

        <!-- Note -->
        <div class="form-section">
          <p class="form-label">备注</p>
          <textarea v-model="form.recipient_note" class="form-textarea" placeholder="如：张医生-仁济医院" rows="3"></textarea>
          <p class="form-hint">备注仅管理员可见，帮助追踪授权用途</p>
        </div>
      </div>

      <!-- Right: Preview -->
      <div class="gen-preview">
        <p class="preview-label">预览</p>
        <div class="preview-card">
          <div class="preview-code">LINSCIO-XXXX-XXXX-XXXX</div>
          <div class="preview-rows">
            <div class="preview-row"><span>产品</span><span>{{ selectedProductName }}</span></div>
            <div class="preview-row"><span>类型</span><span class="type-tag">{{ typeLabel }} · {{ typeSubLabel }}</span></div>
            <div v-if="form.license_type === 'basic'" class="preview-row"><span>周期</span><span>{{ form.duration_months }} 个月</span></div>
            <div v-if="form.license_type === 'trial'" class="preview-row"><span>试用</span><span>{{ form.duration_days }} 天</span></div>
            <div class="preview-row"><span>数量</span><span>{{ form.count }} 张</span></div>
            <div class="preview-row"><span>备注</span><span>{{ form.recipient_note || '未填写' }}</span></div>
          </div>
          <button class="gen-btn" :disabled="loading" @click="handleGenerate">
            {{ loading ? '生成中...' : '生成授权码' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Generated codes result -->
    <el-dialog v-model="showCodes" title="已生成的授权码" width="500px">
      <div v-for="c in generatedCodes" :key="c" style="padding:4px 0;font-family:monospace;">{{ c }}</div>
      <template #footer>
        <el-button type="primary" @click="handleCopyCodes">复制全部</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { generateLicenses, getProducts } from '@/api'

const licenseTypes = [
  { value: 'basic', label: '基础版', desc: '正式授权，按月计' },
  { value: 'trial', label: '试用码', desc: '1 天限时体验' },
  { value: 'specialty', label: '学科包', desc: '永久有效' },
]

const durations = [1, 3, 6, 12]
const trialDays = [1]

const products = ref<any[]>([])
const loading = ref(false)
const showCodes = ref(false)
const generatedCodes = ref<string[]>([])

const form = reactive({
  product_id: '',
  license_type: 'basic',
  duration_months: 1,
  duration_days: 1,
  count: 1,
  recipient_note: '',
})

const selectedProductName = computed(() => {
  const p = products.value.find(x => x.product_id === form.product_id)
  return p?.name || form.product_id || '--'
})

const typeLabel = computed(() => {
  return { basic: '基础版', trial: '试用码', specialty: '学科包' }[form.license_type] || ''
})
const typeSubLabel = computed(() => {
  return { basic: '正式', trial: '试用', specialty: '永久' }[form.license_type] || ''
})

onMounted(async () => {
  try {
    const { data } = await getProducts()
    products.value = data.products || []
    if (products.value.length && !form.product_id) {
      form.product_id = products.value[0].product_id
    }
  } catch {}
})

async function handleGenerate() {
  loading.value = true
  try {
    const payload: any = {
      product_id: form.product_id,
      license_type: form.license_type === 'trial' ? 'basic' : form.license_type,
      count: form.count,
      recipient_note: form.recipient_note,
      is_trial: form.license_type === 'trial',
    }
    if (form.license_type === 'trial') {
      payload.duration_days = form.duration_days
    } else if (form.license_type === 'basic') {
      payload.duration_months = form.duration_months
    }
    const { data } = await generateLicenses(payload)
    generatedCodes.value = data.codes
    showCodes.value = true
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '生成失败')
  } finally {
    loading.value = false
  }
}

function handleCopyCodes() {
  navigator.clipboard.writeText(generatedCodes.value.join('\n'))
  ElMessage.success('已复制到剪贴板')
}
</script>

<style scoped>
.page-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 28px;
}
.page-title { font-size: 20px; font-weight: 600; color: var(--text-primary); }
.back-link { font-size: 13px; color: var(--text-muted); text-decoration: none; }
.back-link:hover { color: var(--text-primary); }

.gen-layout {
  display: grid; grid-template-columns: 1fr 320px; gap: 32px; align-items: start;
}

/* ── Form ── */
.gen-form {
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px;
  padding: 28px;
}
.form-section { margin-bottom: 28px; }
.form-section:last-child { margin-bottom: 0; }
.form-label { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }
.form-hint { font-size: 12px; color: var(--text-muted); margin-top: 6px; }

.type-cards { display: flex; gap: 10px; }
.type-card {
  flex: 1; padding: 16px; border: 2px solid var(--border-card); border-radius: 10px;
  cursor: pointer; transition: all 0.15s; text-align: center;
  h4 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
  p { font-size: 11px; color: var(--text-muted); }
}
.type-card.active { border-color: var(--primary); }
.type-card:hover { border-color: var(--text-muted); }

.form-select {
  width: 100%; max-width: 240px; padding: 10px 14px;
  border: 1px solid var(--border-card); border-radius: 8px; font-size: 14px;
  background: var(--bg-card); color: var(--text-primary); outline: none;
  appearance: auto;
}

.duration-options { display: flex; gap: 10px; }
.duration-opt {
  width: 60px; padding: 10px; border: 2px solid var(--border-card); border-radius: 8px;
  text-align: center; cursor: pointer; font-size: 15px; font-weight: 600;
  color: var(--text-secondary); line-height: 1.3; transition: all 0.15s;
}
.duration-opt.active { border-color: var(--primary); color: var(--primary); }

.count-row { display: flex; align-items: center; gap: 16px; }
.stepper { display: flex; align-items: center; gap: 0; }
.stepper-btn {
  width: 40px; height: 40px; border: 1px solid var(--border-card); background: var(--bg-card);
  font-size: 18px; cursor: pointer; color: var(--text-primary);
  display: flex; align-items: center; justify-content: center;
}
.stepper-btn:first-child { border-radius: 8px 0 0 8px; }
.stepper-btn:last-child { border-radius: 0 8px 8px 0; }
.stepper-val {
  width: 48px; height: 40px; border-top: 1px solid var(--border-card); border-bottom: 1px solid var(--border-card);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 600; color: var(--text-primary);
}
.count-hint { font-size: 12px; color: var(--text-muted); }

.form-textarea {
  width: 100%; max-width: 300px; padding: 10px 14px;
  border: 1px solid var(--border-card); border-radius: 8px; font-size: 14px;
  font-family: inherit; color: var(--text-primary); outline: none; resize: vertical;
}

/* ── Preview ── */
.preview-label { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }
.preview-card {
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px;
  padding: 24px;
}
.preview-code {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 16px; font-weight: 600; color: var(--text-primary);
  text-align: center; padding: 16px; margin-bottom: 16px;
  background: var(--bg-surface); border-radius: 8px;
}
.preview-rows { margin-bottom: 20px; }
.preview-row {
  display: flex; justify-content: space-between; padding: 8px 0;
  font-size: 13px; border-bottom: 1px solid var(--border);
  span:first-child { color: var(--text-muted); }
  span:last-child { color: var(--text-primary); font-weight: 500; }
}
.type-tag { color: var(--primary) !important; }

.gen-btn {
  width: 100%; padding: 14px; border: 1px solid var(--border-card);
  border-radius: 8px; font-size: 15px; font-weight: 600;
  background: var(--bg-card); color: var(--text-primary); cursor: pointer;
  transition: all 0.15s;
}
.gen-btn:hover { border-color: var(--primary); color: var(--primary); }
.gen-btn:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 768px) {
  .gen-layout { grid-template-columns: 1fr; }
}
</style>
