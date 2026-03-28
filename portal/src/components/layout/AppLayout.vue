<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="container header-inner">
        <router-link to="/" class="logo">LinScio</router-link>
        <nav class="nav">
          <router-link to="/license" class="nav-link">我的授权</router-link>
          <router-link to="/device" class="nav-link">我的设备</router-link>
          <router-link to="/account" class="nav-link">账号设置</router-link>
          <button class="nav-link nav-link--logout" @click="handleLogout">退出</button>
        </nav>
      </div>
    </header>
    <main class="app-main container">
      <router-view />
    </main>
    <footer class="app-footer">
      <div class="container footer-inner">
        <span>&copy; {{ year }} LinScio. All rights reserved.</span>
        <a href="https://www.linscio.com.cn" target="_blank">linscio.com.cn</a>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authLogout } from '@/api'

const router = useRouter()
const auth = useAuthStore()
const year = new Date().getFullYear()

async function handleLogout() {
  try { await authLogout() } catch {}
  auth.clearSession()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: #fff;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
  letter-spacing: -0.5px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  padding: 6px 14px;
  border-radius: var(--radius);
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition);
  background: none;
  border: none;
  font-family: inherit;

  &:hover {
    color: var(--primary);
    background: var(--primary-light);
    text-decoration: none;
  }

  &.router-link-active {
    color: var(--primary);
    font-weight: 500;
  }

  &--logout {
    color: var(--text-muted);
    cursor: pointer;
  }
}

.app-main {
  flex: 1;
  padding-top: 32px;
  padding-bottom: 48px;
}

.app-footer {
  border-top: 1px solid var(--border);
  padding: 16px 0;
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
}
</style>
