<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <h1 class="page-title">联系我们</h1>

      <div class="contact-card">
        <h3>邮箱</h3>
        <p><a href="mailto:linscio@163.com">linscio@163.com</a></p>
        <p class="text-muted">工作日 9:00 - 18:00 回复</p>
      </div>

      <div class="contact-card">
        <h3>微信</h3>
        <p class="text-muted">扫描二维码添加微信</p>
        <div class="qr-placeholder">微信二维码（待上传）</div>
      </div>

      <div class="contact-card">
        <h3>其他链接</h3>
        <ul>
          <li><a href="https://www.linscio.com.cn" target="_blank">LinScio 主站</a></li>
          <li><a href="https://portal.linscio.com.cn" target="_blank">授权门户</a></li>
        </ul>
      </div>
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'
</script>

<style scoped lang="scss">
.page { padding: 48px 24px; max-width: 640px; }
.page-title { font-size: 28px; font-weight: 600; margin-bottom: 32px; }
.text-muted { color: var(--text-muted); font-size: 13px; }

.contact-card {
  background: #f9fafb; border: 1px solid var(--border); border-radius: 12px;
  padding: 24px; margin-bottom: 20px;
  h3 { font-size: 16px; margin-bottom: 8px; }
  ul { padding-left: 16px; font-size: 14px; line-height: 2; }
}
.qr-placeholder {
  width: 200px; height: 200px; margin-top: 12px;
  border: 2px dashed var(--border); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); font-size: 13px;
}
</style>
