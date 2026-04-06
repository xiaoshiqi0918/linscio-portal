<template>
  <header class="header">
    <div class="container header-inner">
      <router-link to="/" class="logo">LinScio</router-link>
      <nav class="nav">
        <a href="#products" @click.prevent="scrollTo('products')">产品</a>
        <a href="#vision" @click.prevent="scrollTo('vision')">关于</a>
        <router-link to="/contact">联系我们</router-link>
        <template v-if="portalEmail">
          <span class="nav-email">{{ portalEmail }}</span>
          <a :href="`${portalUrl}/`" class="nav-portal">用户中心</a>
          <a :href="`${portalUrl}/logout`" class="nav-logout">退出</a>
        </template>
        <a v-else :href="`${portalUrl}/login`" target="_blank" class="nav-login">登录</a>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getPortalEmailFromCookie } from '@/utils/portalCookie'

const portalUrl = import.meta.env.VITE_URL_PORTAL
const portalEmail = ref('')

function syncPortalEmail() {
  portalEmail.value = getPortalEmailFromCookie()
}

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  syncPortalEmail()
  window.addEventListener('focus', syncPortalEmail)
})
onUnmounted(() => window.removeEventListener('focus', syncPortalEmail))
</script>

<style scoped lang="scss">
.header {
  position: sticky; top: 0; z-index: 100;
  background: var(--bg-dark);
}
.header-inner {
  display: flex; justify-content: space-between; align-items: center; height: 56px;
}
.logo {
  font-size: 18px; font-weight: 700; color: #fff;
  text-decoration: none; letter-spacing: -0.5px;
}
.nav {
  display: flex; gap: 28px; align-items: center; font-size: 14px;
  a {
    color: var(--text-on-dark-muted); text-decoration: none;
    transition: color 0.15s;
    &:hover { color: #fff; }
  }
}
.nav-login {
  color: #5ED1A5 !important; font-weight: 500;
  &:hover { color: #7EEABC !important; }
}
.nav-email {
  font-size: 13px; color: rgba(255, 255, 255, 0.55); max-width: 200px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.nav-portal {
  color: #5ED1A5 !important; font-weight: 500;
  &:hover { color: #7EEABC !important; }
}
.nav-logout {
  opacity: 0.85;
  &:hover { opacity: 1; color: #fff !important; }
}
</style>
