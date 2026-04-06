<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-main">
        <div class="footer-brand">
          <span class="footer-logo">LinScio / MedComm</span>
          <p class="footer-tagline">结构化内容创作，专注表达本身</p>
        </div>
        <div class="footer-col">
          <h4>产品</h4>
          <router-link to="/features">功能介绍</router-link>
          <router-link to="/download">下载</router-link>
          <router-link to="/help">帮助中心</router-link>
        </div>
        <div class="footer-col">
          <h4>LinScio</h4>
          <a :href="wwwUrl" target="_blank">LinScio 主站</a>
          <a :href="`${portalUrl}/login`" target="_blank">用户登录</a>
          <router-link to="/contact">联系我们</router-link>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; {{ year }} LinScio · MedComm</span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
const wwwUrl = import.meta.env.VITE_URL_WWW
const portalUrl = import.meta.env.VITE_URL_PORTAL
</script>

<style scoped lang="scss">
.footer {
  background: var(--bg-dark);
  padding: 48px 0 0;
}
.footer-main {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 40px;
  padding-bottom: 36px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.footer-brand {
  .footer-logo {
    font-size: 16px; font-weight: 700; color: #fff; letter-spacing: -0.5px;
  }
  .footer-tagline {
    margin-top: 8px; font-size: 13px; color: var(--text-on-dark-muted); line-height: 1.6;
  }
}
.footer-col {
  display: flex; flex-direction: column; gap: 10px;
  h4 {
    font-size: 13px; font-weight: 600; color: var(--text-on-dark);
    margin-bottom: 4px; letter-spacing: 0.5px;
  }
  a {
    font-size: 13px; color: var(--text-on-dark-muted); text-decoration: none;
    transition: color 0.15s;
    &:hover { color: #fff; }
  }
}
.footer-bottom {
  padding: 20px 0;
  font-size: 12px; color: var(--text-on-dark-muted);
}

@media (max-width: 640px) {
  .footer-main {
    grid-template-columns: 1fr;
    gap: 28px;
  }
  .footer-bottom { text-align: center; }
}
</style>
