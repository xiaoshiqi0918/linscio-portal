<template>
  <div>
    <SiteHeader />
    <main class="container legal-page">
      <h1>服务条款</h1>
      <p class="meta">最后更新日期：2026 年 3 月</p>

      <section>
        <h2>1. 服务说明</h2>
        <p>
          LinScio 提供一系列面向专业场景的桌面应用软件（包括但不限于 MedComm、Schola 等），
          以及配套的授权门户、管理后台和在线服务。使用本服务即表示您同意遵守以下条款。
        </p>
      </section>

      <section>
        <h2>2. 账号管理</h2>
        <ul>
          <li>您应提供真实有效的注册信息</li>
          <li>您有责任妥善保管账号密码，因密码泄露造成的损失由您自行承担</li>
          <li>每个邮箱只能注册一个账号</li>
          <li>禁止将账号转让、出租给他人使用</li>
        </ul>
      </section>

      <section>
        <h2>3. 授权许可</h2>
        <ul>
          <li>LinScio 软件授权为<strong>订阅制</strong>，授权码激活后在有效期内可正常使用</li>
          <li>每个授权限绑定一台设备，授权期内最多可换绑 2 次</li>
          <li>授权到期后软件不会被禁用，但更新和学科包下载功能将受限</li>
          <li>试用授权具有独立的时间限制和功能范围</li>
          <li>禁止破解、反编译或绕过授权验证机制</li>
        </ul>
      </section>

      <section>
        <h2>4. 内容责任</h2>
        <p>
          LinScio 软件包含 AI 辅助生成功能。AI 生成的内容仅供参考，不构成专业建议。
          用户应对发布的内容自行负责，确保内容的准确性和合规性。
          LinScio 不对 AI 生成内容的准确性、完整性或适用性做出任何保证。
        </p>
      </section>

      <section>
        <h2>5. 知识产权</h2>
        <ul>
          <li>LinScio 软件、品牌、界面设计的知识产权归 LinScio 所有</li>
          <li>您使用本软件创作的原创内容，知识产权归您所有</li>
          <li>学科包中的术语库、案例和参考资料受知识产权保护，仅限授权用户使用</li>
        </ul>
      </section>

      <section>
        <h2>6. 服务变更与终止</h2>
        <p>
          LinScio 有权在提前通知的情况下修改、暂停或终止部分服务。
          如因违反本条款，我们有权暂停或终止您的服务并不予退款。
        </p>
      </section>

      <section>
        <h2>7. 免责声明</h2>
        <p>
          LinScio 按「现状」提供服务，不对服务的不间断性、安全性或无错误做出明示或暗示的保证。
          在法律允许的最大范围内，LinScio 不对任何间接、偶然或后果性损害承担责任。
        </p>
      </section>

      <section>
        <h2>8. 联系方式</h2>
        <p>如对本服务条款有任何疑问，请联系：<a href="mailto:linscio@163.com">linscio@163.com</a></p>
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
