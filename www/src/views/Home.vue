<template>
  <div>
    <SiteHeader />

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <h1 class="hero-title">专注做好每一个工具</h1>
        <p class="hero-subtitle">
          LinScio 旗下一系列独立软件产品，各自解决一类具体问题，<br/>互不依赖，按需选用。
        </p>
        <div class="hero-actions">
          <a href="mailto:linscio@163.com" class="btn-primary">申请试用</a>
          <a href="#products" class="btn-ghost" @click.prevent="scrollTo('products')">查看产品 →</a>
        </div>
      </div>
    </section>

    <!-- Products -->
    <section id="products" class="products">
      <div class="container">
        <h2 class="section-title">产品</h2>
        <div class="product-grid">
          <a v-for="p in products" :key="p.id" :href="p.link || '#'" class="product-card" :class="{ disabled: !p.link }" target="_blank" @click="!p.link && $event.preventDefault()">
            <div class="product-icon" :style="{ background: p.bgColor }">
              <span :style="{ color: p.iconColor }">{{ p.icon }}</span>
            </div>
            <h3>{{ p.name }}</h3>
            <p class="product-desc">{{ p.desc }}</p>
            <span class="product-link" v-if="p.domain">{{ p.domain }} →</span>
          </a>
          <div class="product-card product-card--more">
            <div class="more-icon">+</div>
            <p class="more-text">更多产品持续推出</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Vision -->
    <section id="vision" class="vision">
      <div class="container">
        <h2 class="section-title">理念</h2>
        <div class="vision-grid">
          <div v-for="v in visions" :key="v.title" class="vision-card">
            <h3>{{ v.title }}</h3>
            <p>{{ v.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <div class="container">
        <div class="cta-card">
          <h2>想了解哪款产品？</h2>
          <p>所有产品均通过授权码激活使用，欢迎联系我们获取试用资<br/>格或进一步了解。</p>
          <div class="cta-actions">
            <a href="mailto:linscio@163.com" class="btn-primary">发送邮件</a>
            <a href="/contact" class="btn-outline">微信咨询</a>
            <a href="mailto:linscio@163.com" class="btn-outline">申请试用</a>
          </div>
        </div>
      </div>
    </section>

    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const products = [
  {
    id: 'medcomm', name: 'MedComm',
    icon: '📋', bgColor: '#e8f5e9', iconColor: '#2e7d32',
    desc: '科普内容创作助手，一键生成全文并自动去AI化改写，支持AIGC检测与多格式导出',
    link: import.meta.env.VITE_URL_MEDCOMM,
    domain: 'medcomm.linscio.com.cn',
  },
  {
    id: 'schola', name: 'Schola',
    icon: '📖', bgColor: '#e3f2fd', iconColor: '#1565c0',
    desc: '学术写作辅助工具，覆盖文献整理、格式规范与全文结构组织',
    link: null, domain: 'schola.linscio.com.cn',
  },
  {
    id: 'qcc', name: 'QCC',
    icon: '⚙', bgColor: '#fff8e1', iconColor: '#f9a825',
    desc: '品管圈活动管理工具，全流程记录、数据整理与标准化报告输出',
    link: null, domain: 'qcc.linscio.com.cn',
  },
  {
    id: 'stats', name: 'Stats',
    icon: '📊', bgColor: '#fce4ec', iconColor: '#c62828',
    desc: '数据统计分析工具，无需编程基础，导入数据即可完成常用分析',
    link: null, domain: 'stats.linscio.com.cn',
  },
  {
    id: 'docs', name: 'Docs',
    icon: '📁', bgColor: '#fbe9e7', iconColor: '#d84315',
    desc: '文件集中管理工具，统一存储、分类检索与版本追踪',
    link: null, domain: 'docs.linscio.com.cn',
  },
]

const visions = [
  { title: '独立、聚焦', desc: '每款产品只解决一类问题，不搞全能，不强迫捆绑。' },
  { title: '简洁、好用', desc: '功能不堆砌，交互不繁琐，工具的价值在于减少障碍。' },
  { title: '本地优先', desc: '数据存储在本地，离线可用，不依赖持续联网。' },
]

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped lang="scss">
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }

.section-title {
  font-size: 16px; font-weight: 500; color: var(--text-secondary);
  margin-bottom: 28px;
}

/* ── Hero ── */
.hero {
  padding: 100px 0 80px; text-align: center;
  background: linear-gradient(180deg, var(--bg-dark-secondary) 0%, var(--bg-hero) 40%, var(--bg-page) 100%);
}
.hero-title {
  font-size: 42px; font-weight: 700; line-height: 1.2;
  margin-bottom: 20px; color: var(--text-primary); letter-spacing: -1px;
}
.hero-subtitle {
  font-size: 15px; color: var(--text-secondary);
  max-width: 520px; margin: 0 auto 36px; line-height: 1.8;
}
.hero-actions {
  display: flex; gap: 12px; justify-content: center;
}
.btn-primary {
  display: inline-block;
  padding: 10px 28px; border-radius: 6px;
  font-size: 14px; font-weight: 500;
  background: var(--primary); color: #fff;
  text-decoration: none; transition: background 0.15s;
  &:hover { background: var(--primary-dark); }
}
.btn-ghost {
  display: inline-block;
  padding: 10px 24px; border: 1px solid var(--border);
  border-radius: 6px; font-size: 14px; color: var(--text-primary);
  text-decoration: none; transition: all 0.15s;
  &:hover { border-color: var(--primary); color: var(--primary); }
}

/* ── Products ── */
.products { padding: 60px 0 80px; background: var(--bg-alt); }
.product-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;
}
.product-card {
  display: block;
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 14px;
  padding: 28px; text-decoration: none; color: var(--text-primary);
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: box-shadow 0.2s, transform 0.2s;
  &:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.07); transform: translateY(-2px); }
  &.disabled { cursor: default; &:hover { transform: none; } }
  h3 { font-size: 16px; font-weight: 600; margin-bottom: 8px; color: var(--text-primary); }
}
.product-icon {
  width: 40px; height: 40px; border-radius: 10px; margin-bottom: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.product-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 16px; }
.product-link { font-size: 12px; color: var(--text-muted); }
.product-card--more {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: transparent; border: 1px dashed var(--border);
  cursor: default;
}
.more-icon {
  font-size: 28px; color: var(--text-muted); margin-bottom: 8px; font-weight: 300;
}
.more-text { font-size: 13px; color: var(--text-muted); }

/* ── Vision ── */
.vision { padding: 80px 0; }
.vision-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px;
}
.vision-card {
  h3 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; }
  p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; }
}

/* ── CTA ── */
.cta { padding: 60px 0 80px; background: var(--bg-alt); }
.cta-card {
  background: var(--bg-card); border: 1px solid var(--border-card);
  border-radius: 16px; padding: 56px 40px; text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  h2 { font-size: 22px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }
  p { font-size: 14px; color: var(--text-secondary); line-height: 1.8; margin-bottom: 28px; }
}
.cta-actions {
  display: flex; gap: 12px; justify-content: center;
}
.btn-outline {
  display: inline-block;
  padding: 10px 24px; border: 1px solid var(--border);
  border-radius: 6px; font-size: 14px; color: var(--text-primary);
  text-decoration: none; transition: all 0.15s;
  &:hover { border-color: var(--primary); color: var(--primary); }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .hero-title { font-size: 28px; }
  .hero-subtitle br { display: none; }
  .product-grid { grid-template-columns: 1fr; }
  .vision-grid { grid-template-columns: 1fr; gap: 24px; }
  .hero-actions, .cta-actions { flex-direction: column; align-items: center; }
  .cta-card { padding: 40px 24px; }
}
</style>
