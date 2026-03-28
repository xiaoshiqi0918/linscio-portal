<template>
  <div>
    <SiteHeader />

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <h1 class="hero-title">面向专业场景的<br/>智能工具矩阵</h1>
        <p class="hero-subtitle">LinScio 为医学、学术、品管、统计等专业领域提供结构化内容创作与智能辅助工具</p>
        <div class="hero-actions">
          <a href="https://portal.linscio.com.cn" target="_blank" class="btn-primary">开始使用</a>
          <a href="https://medcomm.linscio.com.cn" target="_blank" class="btn-outline">了解 MedComm</a>
        </div>
      </div>
    </section>

    <!-- Products -->
    <section class="products">
      <div class="container">
        <h2 class="section-title">产品矩阵</h2>
        <p class="section-sub">每款产品专注一个专业场景，共享统一的 AI 引擎与授权体系</p>
        <div class="product-grid">
          <div v-for="p in products" :key="p.id" class="product-card">
            <div class="product-card__icon">{{ p.icon }}</div>
            <h3>{{ p.name }}</h3>
            <p class="product-card__tag">{{ p.tag }}</p>
            <p class="product-card__desc">{{ p.desc }}</p>
            <a v-if="p.link" :href="p.link" target="_blank" class="product-link">了解更多 &rarr;</a>
            <span v-else class="product-soon">即将推出</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Advantages -->
    <section class="advantages">
      <div class="container">
        <h2 class="section-title">为什么选择 LinScio</h2>
        <div class="adv-grid">
          <div v-for="a in advantages" :key="a.title" class="adv-card">
            <div class="adv-icon">{{ a.icon }}</div>
            <h3>{{ a.title }}</h3>
            <p>{{ a.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Vision -->
    <section class="vision">
      <div class="container">
        <h2 class="section-title">我们的理念</h2>
        <div class="vision-content">
          <p>
            LinScio 致力于将 AI 能力与专业知识深度融合。我们相信，优秀的专业工具不应只是通用 AI 的包装，
            而应当深入理解每个领域的工作流程、知识体系和质量标准。
          </p>
          <p>
            通过结构化的知识管理、防编造验证和专业学科包，我们确保 AI 生成的内容不仅高效，
            更经得起专业审视。本地优先的架构设计则让数据安全掌握在用户手中。
          </p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <div class="container cta-inner">
        <h2>准备好提升专业工作效率了吗？</h2>
        <p>MedComm 现已开放，更多产品即将上线</p>
        <a href="https://portal.linscio.com.cn/register" target="_blank" class="btn-primary">免费注册</a>
      </div>
    </section>

    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const products = [
  { id: 'medcomm', name: 'MedComm', icon: 'M', tag: '医学科普创作', desc: '结构化医学科普内容创作工具，融合 AI 写作、RAG 知识增强和防编造验证，支持 17 种科普形式与 7 种发布平台', link: 'https://medcomm.linscio.com.cn' },
  { id: 'schola', name: 'Schola', icon: 'S', tag: '学术写作辅助', desc: '学术论文写作辅助工具，支持论文结构规划、修改追踪、学术规范验证与文献管理', link: null },
  { id: 'qcc', name: 'QCC', icon: 'Q', tag: '品管圈管理', desc: '品管圈活动全流程管理工具，结构化管理 PDCA 循环、数据分析与成果汇报', link: null },
  { id: 'stats', name: 'Stats', icon: 'St', tag: '数据统计分析', desc: '面向临床科研的统计分析工具，支持常用统计方法、图表生成与结果解读', link: null },
  { id: 'docs', name: 'Docs', icon: 'D', tag: '文件知识管理', desc: '团队知识库与文档协作平台，集中管理科室文件、SOP 与培训资料', link: null },
]

const advantages = [
  { icon: '🎯', title: '专业场景深耕', desc: '每款产品深入理解特定领域的工作流程与专业标准，而非通用 AI 的简单套壳' },
  { icon: '🛡', title: '内容质量保障', desc: '多层验证管线确保 AI 生成内容的准确性，自动标记存疑内容供人工复核' },
  { icon: '📚', title: '专业知识增强', desc: '学科包体系提供领域专属的术语库、案例库和写作范式，提升 AI 输出的专业性' },
  { icon: '🔒', title: '本地优先架构', desc: '核心数据存储在本地，敏感内容无需上传云端，充分保障数据安全与隐私' },
  { icon: '🔄', title: '统一授权体系', desc: '一个账号管理所有产品授权，跨设备同步，灵活的授权码与学科包扩展机制' },
  { icon: '💡', title: '持续迭代进化', desc: '基于用户反馈持续优化 AI 模型与产品功能，学科包定期更新专业知识' },
]
</script>

<style scoped lang="scss">
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

.hero {
  padding: 100px 0 80px; text-align: center;
  background: linear-gradient(180deg, #f8faff 0%, #fff 100%);
}
.hero-title { font-size: 48px; font-weight: 700; line-height: 1.2; margin-bottom: 20px; letter-spacing: -1px; }
.hero-subtitle { font-size: 18px; color: var(--text-secondary); max-width: 600px; margin: 0 auto 32px; }
.hero-actions { display: flex; gap: 12px; justify-content: center; }

.btn-primary {
  padding: 12px 28px; background: var(--primary); color: #fff; border-radius: 8px;
  font-weight: 500; font-size: 15px; text-decoration: none;
  &:hover { background: #1240a8; text-decoration: none; }
}
.btn-outline {
  padding: 12px 28px; border: 1px solid var(--border); border-radius: 8px;
  font-weight: 500; font-size: 15px; color: var(--text-primary); text-decoration: none;
  &:hover { border-color: var(--primary); color: var(--primary); text-decoration: none; }
}

.section-title { font-size: 28px; font-weight: 600; text-align: center; margin-bottom: 12px; }
.section-sub { text-align: center; color: var(--text-secondary); margin-bottom: 40px; }

.products { padding: 80px 0; }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 24px; }
.product-card {
  background: #fff; border: 1px solid var(--border); border-radius: 12px;
  padding: 28px 24px; text-align: center; transition: box-shadow 0.2s;
  &:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
  &__icon {
    width: 48px; height: 48px; margin: 0 auto 16px;
    background: var(--primary-light); color: var(--primary);
    border-radius: 12px; display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 700;
  }
  h3 { font-size: 18px; margin-bottom: 4px; }
  &__tag { font-size: 12px; color: var(--primary); font-weight: 500; margin-bottom: 12px; }
  &__desc { font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 16px; }
}
.product-link { font-size: 13px; font-weight: 500; }
.product-soon { font-size: 12px; color: var(--text-muted); }

.advantages { padding: 80px 0; background: #f8faff; }
.adv-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.adv-card {
  padding: 28px; background: #fff; border-radius: 12px; border: 1px solid var(--border);
  h3 { font-size: 16px; margin: 12px 0 8px; }
  p { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
}
.adv-icon { font-size: 28px; }

.vision { padding: 80px 0; }
.vision-content {
  max-width: 700px; margin: 0 auto; text-align: center;
  p { color: var(--text-secondary); font-size: 15px; line-height: 1.8; margin-bottom: 16px; }
}

.cta { padding: 80px 0; background: linear-gradient(180deg, #f0f5ff 0%, #e8efff 100%); }
.cta-inner {
  text-align: center;
  h2 { font-size: 28px; font-weight: 600; margin-bottom: 12px; }
  p { color: var(--text-secondary); margin-bottom: 24px; }
}

@media (max-width: 768px) {
  .hero-title { font-size: 32px; }
  .adv-grid { grid-template-columns: 1fr; }
  .hero-actions { flex-direction: column; align-items: center; }
}
</style>
