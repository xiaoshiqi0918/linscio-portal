<template>
  <header class="header">
    <div class="container header-inner">
      <div class="header-left">
        <router-link to="/" class="logo">
          <span class="logo-brand">LinScio</span>
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
    </div>
  </header>
</template>

<style scoped lang="scss">
.header {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,0.95); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.header-inner { display: flex; justify-content: space-between; align-items: center; height: 64px; }
.logo { text-decoration: none; display: flex; align-items: baseline; gap: 6px; }
.logo-brand { font-size: 18px; font-weight: 700; color: var(--primary); }
.logo-product { font-size: 16px; font-weight: 500; color: var(--text-secondary); }
.nav {
  display: flex; gap: 24px; font-size: 14px;
  a {
    color: var(--text-secondary); text-decoration: none; padding: 4px 0;
    &:hover, &.router-link-active { color: var(--primary); }
  }
}
</style>
