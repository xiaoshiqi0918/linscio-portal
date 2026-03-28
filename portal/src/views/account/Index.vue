<template>
  <div class="page">
    <h1 class="page__title">账号设置</h1>

    <!-- Change password -->
    <div class="card mb-3" style="max-width: 480px;">
      <h3 style="margin-bottom: 16px;">修改密码</h3>
      <div v-if="pwMsg" :class="['alert', pwSuccess ? 'alert--success' : 'alert--error']">{{ pwMsg }}</div>
      <form @submit.prevent="handleChangePassword">
        <div class="form-group">
          <label>当前密码</label>
          <input v-model="pw.old" type="password" class="form-input" required />
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input v-model="pw.new1" type="password" class="form-input" required minlength="8" />
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input v-model="pw.new2" type="password" class="form-input" required />
        </div>
        <button type="submit" class="btn btn--primary" :disabled="pwLoading">
          {{ pwLoading ? '提交中...' : '修改密码' }}
        </button>
      </form>
    </div>

    <!-- Change phone -->
    <div class="card mb-3" style="max-width: 480px;">
      <h3 style="margin-bottom: 16px;">联系方式</h3>
      <div v-if="phoneMsg" :class="['alert', phoneSuccess ? 'alert--success' : 'alert--error']">{{ phoneMsg }}</div>
      <form @submit.prevent="handleChangePhone">
        <div class="form-group">
          <label>手机号码</label>
          <input v-model="phone" type="tel" class="form-input" placeholder="13800138000" />
        </div>
        <button type="submit" class="btn btn--outline" :disabled="phoneLoading">
          {{ phoneLoading ? '保存中...' : '保存' }}
        </button>
      </form>
    </div>

    <!-- Delete account -->
    <div class="card" style="max-width: 480px; border-color: var(--danger);">
      <h3 style="margin-bottom: 8px; color: var(--danger);">注销账号</h3>
      <p class="text-muted" style="font-size: 13px; margin-bottom: 16px;">
        注销后所有授权将失效，软件需重新激活。此操作不可撤销。
      </p>
      <div v-if="delMsg" class="alert alert--error">{{ delMsg }}</div>
      <div v-if="!showDeleteConfirm">
        <button class="btn btn--danger" @click="showDeleteConfirm = true">注销账号</button>
      </div>
      <form v-else @submit.prevent="handleDelete">
        <div class="form-group">
          <label>输入当前密码确认注销</label>
          <input v-model="delPassword" type="password" class="form-input" required />
        </div>
        <div style="display: flex; gap: 8px;">
          <button type="submit" class="btn btn--danger" :disabled="delLoading">确认注销</button>
          <button type="button" class="btn btn--outline" @click="showDeleteConfirm = false">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { changePassword, changePhone, deleteAccount } from '@/api'

const router = useRouter()
const auth = useAuthStore()

// Password
const pw = reactive({ old: '', new1: '', new2: '' })
const pwLoading = ref(false)
const pwMsg = ref('')
const pwSuccess = ref(false)

async function handleChangePassword() {
  pwMsg.value = ''
  if (pw.new1 !== pw.new2) { pwMsg.value = '两次输入的密码不一致'; return }
  pwLoading.value = true
  try {
    await changePassword({ old_password: pw.old, new_password: pw.new1 })
    pwSuccess.value = true
    pwMsg.value = '密码已修改，请重新登录'
    setTimeout(() => { auth.clearSession(); router.push('/login') }, 2000)
  } catch (e: any) {
    pwSuccess.value = false
    pwMsg.value = e.response?.data?.detail || '修改失败'
  } finally {
    pwLoading.value = false
  }
}

// Phone
const phone = ref('')
const phoneLoading = ref(false)
const phoneMsg = ref('')
const phoneSuccess = ref(false)

async function handleChangePhone() {
  phoneMsg.value = ''
  phoneLoading.value = true
  try {
    await changePhone({ phone: phone.value })
    phoneSuccess.value = true
    phoneMsg.value = '手机号码已更新'
  } catch (e: any) {
    phoneSuccess.value = false
    phoneMsg.value = e.response?.data?.detail || '保存失败'
  } finally {
    phoneLoading.value = false
  }
}

// Delete
const showDeleteConfirm = ref(false)
const delPassword = ref('')
const delLoading = ref(false)
const delMsg = ref('')

async function handleDelete() {
  delMsg.value = ''
  delLoading.value = true
  try {
    await deleteAccount({ password: delPassword.value })
    auth.clearSession()
    router.push('/login')
  } catch (e: any) {
    delMsg.value = e.response?.data?.detail || '注销失败'
  } finally {
    delLoading.value = false
  }
}
</script>
