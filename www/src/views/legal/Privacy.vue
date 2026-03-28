<template>
  <div>
    <SiteHeader />
    <main class="container legal-page">
      <h1>隐私政策</h1>
      <p class="meta">最后更新日期：2026 年 3 月</p>

      <section>
        <h2>1. 信息收集</h2>
        <p>我们在您使用 LinScio 产品和服务时可能收集以下信息：</p>
        <ul>
          <li><strong>账号信息：</strong>注册邮箱、手机号码（选填）、加密存储的密码</li>
          <li><strong>授权信息：</strong>授权码激活记录、设备标识符（设备名称和匿名指纹）</li>
          <li><strong>使用数据：</strong>软件版本、操作系统信息、下载记录</li>
          <li><strong>日志数据：</strong>访问 IP 地址、请求时间（用于安全防护）</li>
        </ul>
      </section>

      <section>
        <h2>2. 信息使用</h2>
        <p>收集的信息仅用于以下目的：</p>
        <ul>
          <li>提供和维护产品服务（账号管理、授权验证、软件更新）</li>
          <li>安全防护（防止恶意访问、账号盗用）</li>
          <li>发送服务通知（授权到期提醒、安全警告等必要通知）</li>
          <li>产品改进（匿名使用统计）</li>
        </ul>
      </section>

      <section>
        <h2>3. 数据安全</h2>
        <p>
          LinScio 桌面应用采用本地优先架构，您的创作内容（文章、草稿、自定义知识库等）存储在本地设备，
          不会上传至我们的服务器。密码通过 bcrypt 单向加密存储，传输层使用 HTTPS/TLS 加密。
        </p>
      </section>

      <section>
        <h2>4. 信息共享</h2>
        <p>
          我们不会将您的个人信息出售、出租或与第三方共享，以下情形除外：
        </p>
        <ul>
          <li>法律法规要求或政府主管部门依法要求</li>
          <li>为保护 LinScio、用户或公众的权利和安全所必需</li>
        </ul>
      </section>

      <section>
        <h2>5. 数据存储</h2>
        <p>
          账号数据存储于中国境内服务器。软件安装包和学科包通过腾讯云 CDN 分发。
          您可以随时通过「账号设置」页面删除账号，我们将在 30 天内删除您的所有个人数据。
        </p>
      </section>

      <section>
        <h2>6. Cookie</h2>
        <p>
          LinScio 门户网站使用必要的会话 Cookie 维持登录状态，不使用第三方追踪 Cookie。
        </p>
      </section>

      <section>
        <h2>7. 联系方式</h2>
        <p>如对本隐私政策有任何疑问，请联系：<a href="mailto:linscio@163.com">linscio@163.com</a></p>
      </section>
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'
</script>

<style scoped lang="scss">
.legal-page {
  max-width: 720px; padding: 48px 24px;
  h1 { font-size: 28px; font-weight: 600; margin-bottom: 4px; }
  .meta { color: var(--text-muted); font-size: 13px; margin-bottom: 36px; }
  section { margin-bottom: 32px; }
  h2 { font-size: 18px; font-weight: 600; margin-bottom: 12px; }
  p { font-size: 14px; color: var(--text-secondary); line-height: 1.8; margin-bottom: 8px; }
  ul { padding-left: 20px; font-size: 14px; color: var(--text-secondary); line-height: 2; }
}
</style>
