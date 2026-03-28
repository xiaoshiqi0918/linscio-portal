<template>
  <el-container style="height: 100vh;">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-text">LinScio</span>
        <span class="logo-badge">Admin</span>
      </div>
      <el-menu
        :default-active="route.path"
        background-color="#001529"
        text-color="#ffffffb3"
        active-text-color="#fff"
        router
      >
        <el-menu-item index="/dashboard">
          <span class="menu-icon">📊</span>
          <span>数据概览</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <span class="menu-icon">👥</span>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/licenses">
          <span class="menu-icon">🔑</span>
          <span>授权码管理</span>
        </el-menu-item>
        <el-menu-item index="/devices">
          <span class="menu-icon">💻</span>
          <span>设备管理</span>
        </el-menu-item>
        <el-menu-item index="/migrations">
          <span class="menu-icon">🔄</span>
          <span>账号迁移</span>
        </el-menu-item>
        <el-menu-item index="/specialties">
          <span class="menu-icon">📚</span>
          <span>学科包管理</span>
        </el-menu-item>
        <el-menu-item index="/releases">
          <span class="menu-icon">📦</span>
          <span>软件安装包</span>
        </el-menu-item>
        <el-menu-item index="/products">
          <span class="menu-icon">🏷</span>
          <span>产品管理</span>
        </el-menu-item>
        <el-sub-menu index="logs">
          <template #title>
            <span class="menu-icon">📝</span>
            <span>日志</span>
          </template>
          <el-menu-item index="/logs/downloads">下载日志</el-menu-item>
          <el-menu-item index="/logs/admin">操作日志</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/security">
          <span class="menu-icon">🛡</span>
          <span>系统安全</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="topbar">
        <span class="topbar-title">{{ pageTitle }}</span>
        <el-button text @click="handleLogout">退出登录</el-button>
      </el-header>
      <el-main style="background:#f5f5f5; overflow-y: auto;">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminAuth } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAdminAuth()

const titleMap: Record<string, string> = {
  '/dashboard': '数据概览',
  '/users': '用户管理',
  '/licenses': '授权码管理',
  '/devices': '设备管理',
  '/migrations': '账号迁移审批',
  '/specialties': '学科包管理',
  '/releases': '软件安装包',
  '/products': '产品管理',
  '/logs/downloads': '下载日志',
  '/logs/admin': '操作日志',
  '/security': '系统安全',
}

const pageTitle = computed(() => titleMap[route.path] || 'LinScio Admin')

function handleLogout() {
  auth.clear()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  background: #001529;
  overflow-y: auto;
}
.sidebar-logo {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.logo-text {
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.5px;
}
.logo-badge {
  font-size: 11px;
  font-weight: 600;
  color: #1a56db;
  background: rgba(26,86,219,0.15);
  padding: 1px 6px;
  border-radius: 4px;
}
.menu-icon {
  margin-right: 8px;
  font-size: 14px;
}
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
  background: #fff;
}
.topbar-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}
</style>
