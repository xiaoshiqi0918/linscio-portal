<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <p class="page-label">联系我们</p>
      <h1 class="page-title">有问题？直接联系</h1>
      <p class="page-sub">试用申请、授权咨询、使用问题，均可通过以下方式联系我们。</p>

      <div class="contact-grid">
        <div class="contact-card">
          <div class="card-header">
            <span class="card-icon">✉</span>
            <h3>邮件</h3>
          </div>
          <p class="card-desc">发送邮件至</p>
          <p class="card-value">linscio@163.com</p>
          <p class="card-note">通常在 1–2 个工作日内回复</p>
        </div>

        <div class="contact-card">
          <div class="card-header">
            <span class="card-icon">💬</span>
            <h3>微信</h3>
          </div>
          <p class="card-desc">扫码添加微信</p>
          <div class="qr-placeholder">二维码<br/>待上传</div>
          <p class="card-note">添加时请备注「linscio」</p>
        </div>
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
.page { padding: 60px 24px 80px; max-width: 900px; }

.page-label {
  font-size: 14px; color: var(--text-muted); margin-bottom: 12px;
}
.page-title {
  font-size: 32px; font-weight: 700; color: var(--text-primary); margin-bottom: 16px;
  letter-spacing: -0.5px;
}
.page-sub {
  font-size: 15px; color: var(--text-secondary); margin-bottom: 48px;
}

.contact-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
}

.contact-card {
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 16px; padding: 32px;
  color: var(--text-primary);
}

.card-header {
  display: flex; align-items: center; gap: 12px; margin-bottom: 24px;
}
.card-icon {
  width: 40px; height: 40px; background: var(--bg-surface); border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.card-header h3 {
  font-size: 16px; font-weight: 600; color: var(--text-primary);
}
.card-desc {
  font-size: 14px; color: var(--text-secondary); margin-bottom: 6px;
}
.card-value {
  font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px;
}
.card-note {
  font-size: 13px; color: var(--text-muted); margin-top: 8px;
}

.qr-placeholder {
  width: 120px; height: 120px; margin: 8px 0 12px;
  border: 2px dashed var(--border); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); font-size: 13px; text-align: center; line-height: 1.5;
}

@media (max-width: 640px) {
  .contact-grid { grid-template-columns: 1fr; }
  .page-title { font-size: 24px; }
}
</style>
