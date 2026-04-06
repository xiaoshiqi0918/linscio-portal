<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-brand">LinScio</span>
        <span class="logo-badge">Admin</span>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-group">
          <p class="nav-group__label">概览</p>
          <router-link to="/dashboard" class="nav-item" exact-active-class="active">
            <span class="nav-dot"></span>数据概览
          </router-link>
        </div>

        <div class="nav-group">
          <p class="nav-group__label">用户与授权</p>
          <router-link to="/users" class="nav-item" active-class="active">
            <span class="nav-dot"></span>用户管理
          </router-link>
          <router-link to="/licenses" class="nav-item" active-class="active">
            <span class="nav-dot"></span>授权码管理
          </router-link>
          <router-link to="/devices" class="nav-item" active-class="active">
            <span class="nav-dot"></span>设备管理
          </router-link>
          <router-link to="/migrations" class="nav-item" active-class="active">
            <span class="nav-dot"></span>账号迁移审批
          </router-link>
        </div>

        <div class="nav-group">
          <p class="nav-group__label">内容发布</p>
          <router-link to="/specialties" class="nav-item" active-class="active">
            <span class="nav-dot"></span>学科包管理
          </router-link>
          <router-link to="/bundles" class="nav-item" active-class="active">
            <span class="nav-dot"></span>组件包管理
          </router-link>
          <router-link to="/releases" class="nav-item" active-class="active">
            <span class="nav-dot"></span>软件安装包
          </router-link>
        </div>

        <div class="nav-group">
          <p class="nav-group__label">系统</p>
          <router-link to="/logs/downloads" class="nav-item" active-class="active">
            <span class="nav-dot"></span>下载日志
          </router-link>
          <router-link to="/security" class="nav-item" active-class="active">
            <span class="nav-dot"></span>系统安全
          </router-link>
        </div>
      </nav>
    </aside>

    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.admin-layout {
  display: flex; min-height: 100vh;
}

.sidebar {
  width: 200px; flex-shrink: 0;
  background: var(--bg-dark); border-right: 1px solid var(--bg-dark-secondary);
  display: flex; flex-direction: column;
  overflow-y: auto;
}

.sidebar-logo {
  height: 52px; display: flex; align-items: center;
  padding: 0 20px; gap: 8px;
  border-bottom: 1px solid var(--bg-dark-secondary);
}
.logo-brand {
  font-size: 17px; font-weight: 700; color: #5ED1A5;
  font-style: italic; letter-spacing: -0.5px;
}
.logo-badge {
  font-size: 11px; font-weight: 500; color: var(--text-on-dark-muted);
  border: 1px solid rgba(255,255,255,0.15); padding: 1px 8px; border-radius: 4px;
}

.sidebar-nav { padding: 16px 0; flex: 1; }

.nav-group { margin-bottom: 20px; }
.nav-group__label {
  padding: 0 20px; font-size: 11px; color: var(--text-on-dark-muted);
  text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 6px;
}

.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 20px; font-size: 14px;
  color: var(--text-on-dark-muted); text-decoration: none;
  transition: all 0.15s; border-left: 3px solid transparent;
}
.nav-item:hover { color: var(--text-on-dark); }
.nav-item.active {
  color: #fff; background: var(--bg-dark-secondary);
  border-left-color: #5ED1A5;
}
.nav-dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: rgba(255,255,255,0.2); flex-shrink: 0;
}
.nav-item.active .nav-dot { background: #5ED1A5; }

.admin-main {
  flex: 1; background: var(--bg-alt);
  overflow-y: auto; padding: 32px 40px;
  color: var(--text-primary);
}
</style>
