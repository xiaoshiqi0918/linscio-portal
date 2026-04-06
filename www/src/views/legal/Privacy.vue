<template>
  <div class="legal-wrapper">
    <header class="legal-header">
      <div class="container lh-inner">
        <div class="lh-left">
          <span class="lh-brand">LinScio</span>
          <span class="lh-title">法律文件</span>
        </div>
        <router-link to="/" class="lh-back">返回</router-link>
      </div>
    </header>

    <div class="container legal-body">
      <div class="legal-tabs">
        <router-link to="/legal/privacy" class="tab active">隐私政策</router-link>
        <router-link to="/legal/terms" class="tab">服务条款</router-link>
      </div>

      <h1>隐私政策</h1>
      <p class="meta">
        生效日期：2026 年 03 月 27 日 · 适用范围：在 LinScio 下相关平台与相关的产品 ·
        服务处理：LinScio（个人开发者，后期将更新为法律主体名称） · 联系方式：linscio@163.com
      </p>

      <section>
        <h2>一、我们收集的信息</h2>
        <p>在您注册帐号、激活授权码、使用软件与服务过程中，我们可能收集以下信息：</p>
        <ul>
          <li><strong>注册邮箱：</strong>用于账号识别、登录验证，及发送必要的验证邮件/通知邮件，以确保安全通信。</li>
          <li><strong>手机号（选填）：</strong>仅作备用联系方式，不参与自动验证流程，可以为空。</li>
          <li><strong>验证信息：</strong>首次登录验证或重置密码时会临时生成短时验证码，不记录已使用的验证码内容。</li>
          <li><strong>授权数据：</strong>授权码激活记录、有效期信息、绑定的设备唯一指纹（不含硬件序列号）、可用学科包列表等。</li>
          <li><strong>设备信息：</strong>操作系统类型及版本、芯片架构（用于区分版本发放），用于在用户中心展示当前绑定设备。不主动采集硬件序列号。</li>
          <li><strong>登录日志：</strong>IP 地址（仅用于安全防护和限速控制）、登录时间。日志不用于用户画像。</li>
          <li><strong>最后活跃 IP：</strong>用于安全审计与已知 IP 黑名单检查，大约三至五次登录后自动覆盖。</li>
          <li><strong>学科包本地缓存数据：</strong>在本地自动缓存，用于在用户中心展示本地版本及是否可更新。不包含创作内容。</li>
        </ul>
        <div class="notice">
          我们不额外收集任何与写作工作流相关的数据。软件内的创作内容和引用资料，由数据及内容保持在你的本地设备上，不会上传至我们的服务器上。
        </div>
      </section>

      <section>
        <h2>二、信息的使用方式</h2>
        <p>我们收集的信息仅供以下目的：</p>
        <ul>
          <li><strong>提供核心功能：</strong>登录验证、授权码验证、设备绑定与换机验证等</li>
          <li><strong>安全与合规保障：</strong>设备及安全检测、限制来自同一 IP 的恶意攻击或暴力破解</li>
          <li><strong>维护知识库完整：</strong>统计频率与资源分布策略</li>
          <li><strong>服务状态告知：</strong>授权将到期提醒、系统升级通知等功能性通知</li>
        </ul>
        <p>我们不将用户的个人信息对外打包供给第三方广告服务，也不将产品使用习惯进行数据化分析营销。</p>
      </section>

      <section>
        <h2>三、信息共享与披露</h2>
        <p>
          我们的个人信息存储在平台内部的加密字段中，运行时采用数据库保护加密。除非经过授权，我们不会主动对外传输。
          会话令牌（Token）采用加密机制进行校验，确保运行机构产品安全。
        </p>
        <p>双方不得擅自向第三方公布。也不应超出双方商定以外的个人信息。以下情况除外：</p>
        <ul>
          <li>经用户知情同意</li>
          <li>依据公共利益或法律法规要求</li>
          <li>为避免用户及认证的技术可能影响安全的需要</li>
        </ul>
      </section>

      <section>
        <h2>四、信息的安全</h2>
        <p>所属（含个人信息及产品运行）的数据，你享有：</p>
        <ul>
          <li>查阅、复制你的个人信息</li>
          <li>更正不准确的个人信息</li>
          <li>删除你的个人信息（注册期间）</li>
          <li>撤回对个人信息处理的授权同意</li>
        </ul>
        <p>如需行使以上权利，请发送邮件至 <a href="mailto:linscio@163.com">linscio@163.com</a>，我们将在 10 个工作日内回复。</p>
      </section>

      <section>
        <h2>五、Cookie 及追踪技术</h2>
        <p>
          门户网站仅使用必要 Cookie。LinScio 门户网站使用 Keychain 存储登录凭证，不会侵入用户隐私。
          我们不使用第三方追踪 Cookie 或分析工具。
        </p>
      </section>

      <section>
        <h2>六、第三方链入</h2>
        <p>
          我们的服务可能包含第三方链接。我们对第三方网站的隐私政策和内容不承担责任。
          建议您在访问第三方网站时查阅其隐私政策。
        </p>
      </section>

      <section>
        <h2>七、未成年人</h2>
        <p>
          本产品面向成年用户。我们不会有意收集未成年人的个人信息。
          如发现误收集，请联系：<a href="mailto:linscio@163.com">linscio@163.com</a>。
        </p>
      </section>

      <section>
        <h2>八、变更与通知</h2>
        <p>
          如对本隐私政策有任何疑问，请发送邮件至 <a href="mailto:linscio@163.com">linscio@163.com</a>，我们将在 5 个工作日内回复。
        </p>
      </section>
    </div>

    <footer class="legal-footer">
      <div class="container lf-inner">
        <span>&copy; 2026 LinScio · 保留所有权利</span>
        <span class="lf-links">
          <router-link to="/legal/privacy">隐私政策</router-link>
          <router-link to="/legal/terms">服务条款</router-link>
        </span>
      </div>
    </footer>
  </div>
</template>

<style scoped lang="scss">
.legal-wrapper {
  min-height: 100vh; display: flex; flex-direction: column;
  background: var(--bg-page); color: var(--text-primary);
}

.legal-header { background: var(--bg-dark); }
.lh-inner {
  display: flex; justify-content: space-between; align-items: center;
  height: 52px;
}
.lh-left { display: flex; align-items: baseline; gap: 10px; }
.lh-brand { font-size: 17px; font-weight: 700; color: #fff; font-style: italic; }
.lh-title { font-size: 14px; color: var(--text-on-dark-muted); }
.lh-back { font-size: 13px; color: var(--text-on-dark-muted); text-decoration: none; &:hover { color: #fff; } }

.legal-body {
  flex: 1; max-width: 800px; padding: 32px 24px 60px;
}

.legal-tabs {
  display: flex; gap: 16px; margin-bottom: 28px;
}
.tab {
  padding: 6px 16px; border-radius: 6px; font-size: 13px;
  color: var(--text-muted); text-decoration: none;
  &.active { background: var(--bg-surface); color: var(--text-primary); font-weight: 500; }
  &:not(.active):hover { color: var(--text-secondary); }
}

h1 {
  font-size: 24px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px;
}
.meta {
  font-size: 12px; color: var(--text-muted); line-height: 1.8; margin-bottom: 32px;
}
section { margin-bottom: 28px; }
h2 {
  font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 10px;
}
p {
  font-size: 13px; color: var(--text-secondary); line-height: 1.9; margin-bottom: 8px;
  a { color: var(--text-secondary); text-decoration: underline; text-underline-offset: 3px; }
}
ul {
  padding-left: 18px; font-size: 13px; color: var(--text-secondary); line-height: 2;
  li { margin-bottom: 2px; }
  strong { color: var(--text-primary); font-weight: 500; }
}
.notice {
  margin-top: 12px; padding: 14px 18px; border: 1px solid var(--border);
  border-radius: 8px; font-size: 13px; color: var(--text-secondary); line-height: 1.8;
  background: var(--bg-surface);
}

.legal-footer { background: var(--bg-dark); padding: 20px 0; }
.lf-inner {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 12px; color: var(--text-on-dark-muted);
}
.lf-links {
  display: flex; gap: 20px;
  a { color: var(--text-on-dark-muted); text-decoration: none; &:hover { color: #fff; } }
}
</style>
