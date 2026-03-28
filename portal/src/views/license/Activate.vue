<template>
  <div class="page">
    <h1 class="page__title">激活授权码</h1>
    <p class="page__subtitle">输入授权码以激活或续费产品</p>

    <div class="card" style="max-width: 560px;">
      <div v-if="error" class="alert alert--error">{{ error }}</div>
      <div v-if="result" class="alert alert--success">
        <p v-if="result.token_unchanged">授权已更新，有效期延长至 {{ formatDate(result.new_expires_at!) }}</p>
        <p v-else-if="result.deep_link">授权激活成功！</p>
        <p v-if="result.deep_link" class="mt-1">
          <a :href="result.deep_link" class="btn btn--primary">打开软件完成绑定</a>
        </p>
        <p v-if="result.specialty_ids" class="mt-1">已激活学科包：{{ result.specialty_ids.join(', ') }}</p>
      </div>

      <form v-if="!result" @submit.prevent="handleActivate">
        <div class="form-group">
          <label>授权码</label>
          <input
            v-model="code"
            type="text"
            class="form-input"
            placeholder="LINSCIO-XXXX-XXXX-XXXX"
            required
            style="font-family: monospace; font-size: 16px; letter-spacing: 1px;"
          />
        </div>
        <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
          {{ loading ? '激活中...' : '激活' }}
        </button>
      </form>

      <router-link v-if="result" to="/license" class="btn btn--outline btn--block mt-2">返回我的授权</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { licenseActivate } from '@/api'

const code = ref('')
const loading = ref(false)
const error = ref('')
const result = ref<any>(null)

async function handleActivate() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await licenseActivate({ code: code.value })
    result.value = data
  } catch (e: any) {
    const detail = e.response?.data?.detail || ''
    const messages: Record<string, string> = {
      code_format_invalid: '授权码格式错误，请检查后重新输入',
      code_invalid_or_used: '授权码无效或已被使用',
      email_not_verified: '请先完成邮箱验证',
      rate_limit_exceeded: '操作过于频繁，请稍后再试',
      trial_cannot_activate_specialty: '试用用户无法激活学科包，请先激活正式授权',
      already_has_formal_license: '已拥有正式授权，无法再激活试用码',
    }
    error.value = messages[detail] || detail || '激活失败'
  } finally {
    loading.value = false
  }
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN')
}
</script>
