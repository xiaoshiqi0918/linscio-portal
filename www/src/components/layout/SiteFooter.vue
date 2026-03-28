<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-left">
        <span>&copy; {{ year }} LinScio. All rights reserved.</span>
        <span class="footer-links">
          <router-link to="/legal/privacy">隐私政策</router-link>
          <span class="sep">|</span>
          <router-link to="/legal/terms">服务条款</router-link>
        </span>
      </div>
      <div class="footer-right">
        <a href="mailto:linscio@163.com">linscio@163.com</a>
        <span class="sep">|</span>
        <a href="https://portal.linscio.com.cn" target="_blank">用户登录</a>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped lang="scss">
.footer { padding: 24px 0; border-top: 1px solid var(--border); margin-top: 60px; }
.footer-inner {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 13px; color: var(--text-muted);
  a { color: var(--text-muted); text-decoration: none; &:hover { color: var(--primary); } }
}
.footer-links { margin-left: 16px; }
.sep { margin: 0 8px; color: #ddd; }

@media (max-width: 640px) {
  .footer-inner { flex-direction: column; gap: 8px; text-align: center; }
  .footer-links { margin-left: 0; display: block; margin-top: 4px; }
}
</style>
