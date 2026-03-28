<template>
  <div class="page">
    <h1 class="page__title">我的设备</h1>
    <p class="page__subtitle">管理已绑定设备，或使用换机码换绑新设备</p>

    <div v-if="loading" class="text-center text-muted mt-3">加载中...</div>

    <div v-else>
      <div v-for="lic in licenses" :key="lic.product_id" class="card mb-2">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
          <h3>{{ lic.product_name }}</h3>
          <span class="badge" :class="lic.device_name ? 'badge--valid' : 'badge--inactive'">
            {{ lic.device_name ? '已绑定' : '未绑定' }}
          </span>
        </div>
        <div v-if="lic.device_name" class="info-row"><span>设备名称</span><span>{{ lic.device_name }}</span></div>
        <div class="info-row"><span>剩余换绑次数</span><span>{{ lic.rebind_remaining ?? '-' }} 次</span></div>
      </div>

      <div class="card mt-3" style="max-width: 480px;">
        <h3 style="margin-bottom: 12px;">换机码验证</h3>
        <p class="text-muted" style="font-size:13px;margin-bottom:16px;">
          在新设备上打开软件获取换机码，然后在此验证以完成换绑。
        </p>

        <div v-if="verifyError" class="alert alert--error">{{ verifyError }}</div>
        <div v-if="verifyResult" class="alert alert--success">
          <p>换绑成功！新设备：{{ verifyResult.new_device_name }}</p>
          <a v-if="verifyResult.deep_link" :href="verifyResult.deep_link" class="btn btn--primary mt-1">打开软件完成激活</a>
        </div>

        <form v-if="!verifyResult" @submit.prevent="handleVerify">
          <div class="form-group">
            <label>产品</label>
            <select v-model="verifyForm.product_id" class="form-input" required>
              <option value="" disabled>选择产品</option>
              <option v-for="lic in licenses" :key="lic.product_id" :value="lic.product_id">{{ lic.product_name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>换机码（6 位数字）</label>
            <input v-model="verifyForm.code" type="text" class="form-input" placeholder="如 483921" required maxlength="6" />
          </div>
          <button type="submit" class="btn btn--primary" :disabled="verifyLoading">
            {{ verifyLoading ? '验证中...' : '验证换绑' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { licenseStatusAll, deviceVerify } from '@/api'

const loading = ref(true)
const licenses = ref<any[]>([])
const verifyForm = reactive({ product_id: '', code: '' })
const verifyLoading = ref(false)
const verifyError = ref('')
const verifyResult = ref<any>(null)

onMounted(async () => {
  try {
    const { data } = await licenseStatusAll()
    licenses.value = data.licenses.filter((l: any) => l.status !== 'not_activated')
  } catch {}
  loading.value = false
})

async function handleVerify() {
  verifyLoading.value = true
  verifyError.value = ''
  try {
    const { data } = await deviceVerify(verifyForm)
    verifyResult.value = data
  } catch (e: any) {
    verifyError.value = e.response?.data?.detail || '验证失败'
  } finally {
    verifyLoading.value = false
  }
}
</script>

<style scoped lang="scss">
.info-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
  &:last-child { border-bottom: none; }
}
</style>
