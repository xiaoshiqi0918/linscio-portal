<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <h1 class="page-title">联系我们</h1>
      <p class="page-sub">如有产品咨询、授权购买或技术支持需求，请通过以下方式联系</p>

      <div class="contact-grid">
        <div class="contact-card">
          <div class="contact-icon">✉</div>
          <h3>邮箱</h3>
          <p><a href="mailto:linscio@163.com">linscio@163.com</a></p>
          <p class="note">工作日 9:00 - 18:00 回复</p>
        </div>

        <div class="contact-card">
          <div class="contact-icon">💬</div>
          <h3>微信</h3>
          <p class="note">扫描二维码添加微信咨询</p>
          <div class="qr-placeholder">请添加微信号：<strong>LinScio</strong></div>
        </div>

        <div class="contact-card">
          <div class="contact-icon">🔗</div>
          <h3>相关链接</h3>
          <ul>
            <li><a :href="portalUrl" target="_blank">授权门户</a> — 登录、注册、管理授权</li>
            <li><a :href="medcommUrl" target="_blank">MedComm 产品页</a> — 了解与下载</li>
          </ul>
        </div>
      </div>
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const portalUrl = import.meta.env.VITE_URL_PORTAL
const medcommUrl = import.meta.env.VITE_URL_MEDCOMM
</script>

<style scoped lang="scss">
.page { padding: 60px 24px; max-width: 900px; }
.page-title { font-size: 28px; font-weight: 600; margin-bottom: 8px; color: var(--text-primary); }
.page-sub { color: var(--text-secondary); margin-bottom: 36px; }

.contact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
.contact-card {
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; padding: 28px;
  h3 { font-size: 16px; margin: 12px 0 8px; color: var(--text-primary); }
  p { font-size: 14px; color: var(--text-secondary); }
  a { color: var(--primary); }
  ul { padding-left: 16px; font-size: 14px; line-height: 2; color: var(--text-secondary); }
  .note { color: var(--text-muted); font-size: 13px; }
}
.contact-icon { font-size: 28px; }

.qr-placeholder {
  width: 160px; height: 160px; margin-top: 12px;
  border: 2px dashed var(--border); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); font-size: 13px; text-align: center; line-height: 1.6;
}
</style>
