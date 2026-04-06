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
        <router-link to="/legal/privacy" class="tab">隐私政策</router-link>
        <router-link to="/legal/terms" class="tab active">服务条款</router-link>
      </div>

      <h1>服务条款</h1>
      <p class="meta">
        生效日期：2026 年 03 月 27 日 · 适用范围：LinScio 旗下所有软件产品及网站服务 ·
        服务提供方：LinScio（个人开发者，后期将更新为法律主体名称） · 联系方式：linscio@163.com
      </p>

      <section>
        <h2>一、服务内容</h2>
        <p>
          LinScio 提供包括 MedComm、Schola、QCC、Stats、Docs 在内的一系列专业功能软件，
          以及配套的用户中心（portal.linscio.com.cn）和各产品门户网站。
          所有软件产品均采用授权码激活方式，激活后即可获得使用许可方可正常使用。
        </p>
      </section>

      <section>
        <h2>二、账号与授权</h2>
        <ul>
          <li>每个账号对应一台绑定设备，每个授权区间内最多可自由换机 2 次</li>
          <li>授权码为一次性使用，激活后立即失效，请妥善保管</li>
          <li>基础版授权到期后，软件仍可正常使用，但无法获取新版本</li>
          <li>学科包授权一次购买，永久有效，不受基础版授权周期影响</li>
          <li>试用授权按天计算，激活后功能保留，到期后需升级正式版方可继续使用全部功能</li>
          <li>授权与账号绑定，不可转让给他人使用</li>
        </ul>
      </section>

      <section>
        <h2>三、使用限制</h2>
        <p>你同意不将软件用于以下不正当用途：</p>
        <ul>
          <li>反向工程、破解、复制任何已有注册或授权机制</li>
          <li>将授权代码、功能或数据给予第三方</li>
          <li>利用软件从事违法活动</li>
          <li>干扰系统运行及维护及网络安全</li>
        </ul>
        <p>违反上述规定，我们有权立即取消你的授权，且不予退款。</p>
      </section>

      <section>
        <h2>四、知识产权</h2>
        <p>
          LinScio 旗下所有软件、网站、文档及学科包内容的知识产权归 LinScio 所有。授权购买后获得使用许可，
          但非所有权。你不得复制、转售、传播，终端未经许可不得向任何第三方共享。
        </p>
        <p>
          你在软件内创作创建的内容（创作品、知识库等）归你所有，我们不主动抓取任何你的创作内容。
        </p>
      </section>

      <section>
        <h2>五、免责声明</h2>
        <p>软件按「现状」提供，我们不对以下情况承担责任：</p>
        <ul>
          <li>因使用软件产生的内容的准确性、完整性或适用性</li>
          <li>因不可抗力（包括自然灾害、网络中断、自然灾害等）导致的服务中断</li>
          <li>因用户操作不当导致的数据丢失或损害</li>
        </ul>
        <div class="notice">
          软件内容仅供辅助参考，不构成任何专业建议。使用软件生成的任何内容，用户须自行审核并承担相应责任。
        </div>
      </section>

      <section>
        <h2>六、服务变更与终止</h2>
        <p>
          我们在紧急情况下，暂停或终止部分服务的权利，但会提供合理过渡期并适当补偿。
          如因违规行为导致权限被限制，我们将以合适方式予以通知。
        </p>
      </section>

      <section>
        <h2>七、违约与赔偿</h2>
        <p>
          如因违反本条款造成 LinScio 或第三方损失，违约方应承担相应赔偿责任。
          赔偿范围包括但不限于直接损失及合理的维权费用。
        </p>
      </section>

      <section>
        <h2>八、法律适用</h2>
        <p>
          本条款适用中华人民共和国法律管辖。如发生争议，双方应首先协商解决；协商不成的，
          应交至有管辖权的人民法院诉讼解决。
        </p>
      </section>

      <section>
        <h2>九、联系我们</h2>
        <p>
          如对本条款有任何疑问，请发送邮件至 <a href="mailto:linscio@163.com">linscio@163.com</a>，我们将在 5 个工作日内回复。
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
