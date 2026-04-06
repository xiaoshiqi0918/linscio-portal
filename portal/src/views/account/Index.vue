<template>
  <div class="page">
    <h1 class="page__title">账号设置</h1>

    <!-- 基本信息 -->
    <p class="section-label">基本信息</p>
    <div class="setting-card card">
      <div class="setting-row">
        <div class="setting-info">
          <p class="setting-key">注册邮箱</p>
          <p class="setting-val">{{ userEmail }}</p>
          <p class="setting-hint">邮箱为账号唯一标识，不可修改</p>
        </div>
      </div>
      <div class="setting-divider"></div>
      <div class="setting-row">
        <div class="setting-info">
          <p class="setting-key">手机号 <span class="optional">选填</span></p>
          <template v-if="!editingPhone">
            <p class="setting-val">{{ phone || '未填写' }}</p>
          </template>
          <template v-else>
            <input v-model="phoneInput" type="tel" class="inline-input" placeholder="13800138000" />
            <div v-if="phoneMsg" :class="['inline-msg', phoneSuccess ? 'inline-msg--ok' : 'inline-msg--err']">{{ phoneMsg }}</div>
          </template>
        </div>
        <div class="setting-action">
          <template v-if="!editingPhone">
            <button class="btn btn--ghost" @click="editingPhone = true; phoneInput = phone">编辑</button>
          </template>
          <template v-else>
            <button class="btn btn--ghost" :disabled="phoneLoading" @click="handleSavePhone">{{ phoneLoading ? '保存中...' : '保存' }}</button>
            <button class="btn btn--ghost" @click="editingPhone = false; phoneMsg = ''">取消</button>
          </template>
        </div>
      </div>
    </div>

    <!-- 修改密码 -->
    <p class="section-label">修改密码</p>
    <div class="setting-card card">
      <template v-if="!editingPw">
        <div class="setting-row">
          <div class="setting-info">
            <p class="setting-key">登录密码</p>
            <p class="setting-val">••••••••</p>
            <p class="setting-hint">修改密码后需要重新登录，软件端也将要求重新激活</p>
          </div>
          <div class="setting-action">
            <button class="btn btn--ghost" @click="editingPw = true">修改</button>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="pw-form">
          <div v-if="pwMsg" :class="['alert', pwSuccess ? 'alert--success' : 'alert--error']">{{ pwMsg }}</div>
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
          <div class="pw-actions">
            <button class="btn btn--ghost" :disabled="pwLoading" @click="handleChangePassword">{{ pwLoading ? '提交中...' : '确认修改' }}</button>
            <button class="btn btn--ghost" @click="editingPw = false; pwMsg = ''">取消</button>
          </div>
        </div>
      </template>
    </div>

    <!-- 危险操作 -->
    <p class="section-label">危险操作</p>
    <div class="setting-card card danger-card">
      <template v-if="!showDeleteConfirm">
        <div class="setting-row">
          <div class="setting-info">
            <p class="setting-key danger-text">注销账号</p>
            <p class="setting-hint">注销后账号、授权记录及学科包授权将永久删除，无法恢复。</p>
          </div>
          <div class="setting-action">
            <button class="btn btn--ghost" @click="showDeleteConfirm = true">注销账号</button>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="pw-form">
          <p class="danger-text" style="font-weight:600;margin-bottom:12px;">确认注销账号</p>
          <div v-if="delMsg" class="alert alert--error">{{ delMsg }}</div>
          <div class="form-group">
            <label>输入当前密码确认</label>
            <input v-model="delPassword" type="password" class="form-input" required />
          </div>
          <div class="pw-actions">
            <button class="btn btn--ghost" style="border-color:#dc2626;color:#dc2626;" :disabled="delLoading" @click="handleDelete">{{ delLoading ? '处理中...' : '确认注销' }}</button>
            <button class="btn btn--ghost" @click="showDeleteConfirm = false; delMsg = ''">取消</button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { changePassword, changePhone, deleteAccount } from '@/api'

const router = useRouter()
const auth = useAuthStore()

const userEmail = computed(() => auth.userEmail || '—')

// Phone
const phone = ref('')
const phoneInput = ref('')
const editingPhone = ref(false)
const phoneLoading = ref(false)
const phoneMsg = ref('')
const phoneSuccess = ref(false)

async function handleSavePhone() {
  phoneMsg.value = ''
  phoneLoading.value = true
  try {
    await changePhone({ phone: phoneInput.value })
    phoneSuccess.value = true
    phoneMsg.value = '已保存'
    phone.value = phoneInput.value
    setTimeout(() => { editingPhone.value = false; phoneMsg.value = '' }, 1500)
  } catch (e: any) {
    phoneSuccess.value = false
    phoneMsg.value = e.response?.data?.detail || '保存失败'
  } finally {
    phoneLoading.value = false
  }
}

// Password
const editingPw = ref(false)
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
    pwMsg.value = '密码已修改，即将重新登录...'
    setTimeout(() => { auth.clearSession(); router.push('/login') }, 2000)
  } catch (e: any) {
    pwSuccess.value = false
    pwMsg.value = e.response?.data?.detail || '修改失败'
  } finally {
    pwLoading.value = false
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

<style scoped lang="scss">
.section-label {
  font-size: 13px; color: var(--text-muted); margin-bottom: 12px; margin-top: 28px;
  &:first-of-type { margin-top: 0; }
}

.setting-card { padding: 24px 28px; }

.setting-row {
  display: flex; justify-content: space-between; align-items: center; gap: 24px;
}
.setting-info { flex: 1; }
.setting-key {
  font-size: 13px; color: var(--text-muted); margin-bottom: 4px;
}
.optional {
  font-size: 11px; color: var(--text-muted); margin-left: 4px;
}
.setting-val {
  font-size: 15px; color: var(--text-secondary); margin-bottom: 4px;
}
.setting-hint {
  font-size: 12px; color: var(--text-muted); line-height: 1.6;
}
.setting-action {
  display: flex; gap: 8px; flex-shrink: 0;
}
.setting-divider {
  height: 1px; background: var(--border); margin: 18px 0;
}

.inline-input {
  padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--bg-surface); color: var(--text-primary);
  font-size: 14px; width: 220px; outline: none; margin-top: 4px;
  &:focus { border-color: var(--primary); }
}
.inline-msg {
  font-size: 12px; margin-top: 4px;
  &--ok { color: var(--success); }
  &--err { color: var(--danger); }
}

.danger-card { border-color: var(--danger); }
.danger-text { color: var(--danger); }

.pw-form {
  max-width: 380px; padding: 4px 0;
}
.pw-actions {
  display: flex; gap: 8px; margin-top: 8px;
}
</style>
