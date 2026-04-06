<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-main">
        <div class="footer-brand">
          <span class="footer-logo">LinScio</span>
          <p class="footer-tagline">专注做好每一个工具</p>
        </div>
        <div class="footer-col">
          <h4>产品</h4>
          <a :href="medcommUrl" target="_blank">MedComm</a>
          <a href="#">Schola</a>
          <a href="#">QCC</a>
        </div>
        <div class="footer-col">
          <h4>公司</h4>
          <router-link to="/contact">联系我们</router-link>
          <router-link to="/legal/privacy">隐私政策</router-link>
          <router-link to="/legal/terms">服务条款</router-link>
        </div>
        <div class="footer-col">
          <h4>支持</h4>
          <a href="mailto:linscio@163.com">发送邮件</a>
          <a :href="`${portalUrl}/login`" target="_blank">用户登录</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; {{ year }} LinScio · 保留所有权利</span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
const medcommUrl = import.meta.env.VITE_URL_MEDCOMM
const portalUrl = import.meta.env.VITE_URL_PORTAL
</script>

<style scoped lang="scss">
.footer {
  background: var(--bg-dark);
  padding: 48px 0 0;
}
.footer-main {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  padding-bottom: 36px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.footer-brand {
  .footer-logo {
    font-size: 18px; font-weight: 700; color: #fff; letter-spacing: -0.5px;
  }
  .footer-tagline {
    margin-top: 8px; font-size: 13px; color: var(--text-on-dark-muted); line-height: 1.6;
  }
}
.footer-col {
  display: flex; flex-direction: column; gap: 10px;
  h4 {
    font-size: 13px; font-weight: 600; color: var(--text-on-dark);
    margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;
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
    grid-template-columns: 1fr 1fr;
    gap: 28px;
  }
  .footer-brand { grid-column: 1 / -1; }
  .footer-bottom { text-align: center; }
}
</style>
