<template>
  <div class="login-page">
    <el-card class="login-card" shadow="always">
      <h1 style="text-align:center;margin-bottom:24px;font-size:20px;">LinScio 管理后台</h1>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input v-model="form.email" placeholder="管理员邮箱" size="large" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" show-password />
        </el-form-item>
        <el-button type="primary" size="large" style="width:100%" :loading="loading" @click="handleLogin">
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAdminAuth } from '@/stores/auth'
import { adminLogin } from '@/api'

const router = useRouter()
const auth = useAdminAuth()
const loading = ref(false)
const form = reactive({ email: '', password: '' })

async function handleLogin() {
  loading.value = true
  try {
    const { data } = await adminLogin(form)
    if (!data.is_admin) {
      ElMessage.error('该账号没有管理员权限')
      return
    }
    auth.setToken(data.session_token)
    router.push('/')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
}
.login-card { width: 400px; }
</style>
