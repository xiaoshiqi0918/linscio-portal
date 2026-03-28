<template>
  <header class="header">
    <div class="container header-inner">
      <router-link to="/" class="logo">LinScio</router-link>
      <nav class="nav">
        <router-link to="/">首页</router-link>
        <router-link to="/contact">联系我们</router-link>
        <router-link to="/legal/privacy">法律信息</router-link>
        <a href="https://portal.linscio.com.cn" target="_blank" class="nav-login">用户登录</a>
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
.header-inner {
  display: flex; justify-content: space-between; align-items: center; height: 64px;
}
.logo {
  font-size: 20px; font-weight: 700; color: var(--primary);
  text-decoration: none; letter-spacing: -0.5px;
}
.nav {
  display: flex; gap: 24px; align-items: center; font-size: 14px;
  a {
    color: var(--text-secondary); text-decoration: none;
    padding: 4px 0;
    &:hover, &.router-link-active { color: var(--primary); text-decoration: none; }
  }
}
.nav-login {
  padding: 6px 16px; border: 1px solid var(--primary); border-radius: 6px;
  color: var(--primary) !important; font-weight: 500;
  &:hover { background: var(--primary-light); }
}
</style>
