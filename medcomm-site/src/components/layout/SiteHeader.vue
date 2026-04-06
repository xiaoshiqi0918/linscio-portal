<template>
  <header class="header">
    <div class="container header-inner">
      <div class="header-left">
        <router-link to="/" class="logo">
          <span class="logo-brand">LinScio</span>
          <span class="logo-sep">/</span>
          <span class="logo-product">MedComm</span>
        </router-link>
      </div>
      <nav class="nav">
        <router-link to="/">首页</router-link>
        <router-link to="/features">功能介绍</router-link>
        <router-link to="/download">下载</router-link>
        <router-link to="/help">帮助中心</router-link>
        <router-link to="/contact">联系我们</router-link>
      </nav>
      <a :href="`${portalUrl}/login`" target="_blank" class="header-login">登录</a>
    </div>
  </header>
</template>

<script setup lang="ts">
const portalUrl = import.meta.env.VITE_URL_PORTAL
</script>

<style scoped lang="scss">
.header {
  position: sticky; top: 0; z-index: 100;
  background: var(--bg-dark);
}
.header-inner { display: flex; justify-content: space-between; align-items: center; height: 56px; }
.logo {
  text-decoration: none; display: flex; align-items: baseline; gap: 8px;
}
.logo-brand { font-size: 16px; font-weight: 700; color: #fff; }
.logo-sep { font-size: 16px; color: rgba(255,255,255,0.3); }
.logo-product { font-size: 16px; font-weight: 500; color: var(--text-on-dark-muted); }
.nav {
  display: flex; gap: 24px; font-size: 14px;
  a {
    color: var(--text-on-dark-muted); text-decoration: none; padding: 4px 0;
    transition: color 0.15s;
    &:hover, &.router-link-active { color: #fff; }
  }
}
.header-login {
  padding: 6px 18px; border: 1px solid rgba(255,255,255,0.2); border-radius: 6px;
  font-size: 13px; color: #5ED1A5; text-decoration: none;
  transition: all 0.15s; flex-shrink: 0;
  &:hover { border-color: #5ED1A5; color: #7EEABC; }
}
</style>
