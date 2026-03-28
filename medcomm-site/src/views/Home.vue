<template>
  <div>
    <SiteHeader />

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <h1>结构化医学科普<br/>内容创作工具</h1>
        <p class="hero-sub">融合 AI 写作、RAG 知识增强和防编造验证，让医学科普更专业、更高效</p>
        <div class="hero-actions">
          <router-link to="/download" class="btn-primary">下载 MedComm</router-link>
          <router-link to="/features" class="btn-outline">了解功能</router-link>
        </div>
      </div>
    </section>

    <!-- Features overview -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">核心能力</h2>
        <div class="feature-grid">
          <div v-for="f in features" :key="f.title" class="feature-card">
            <div class="feature-icon">{{ f.icon }}</div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Specialty packs -->
    <section class="spec-section">
      <div class="container">
        <h2 class="section-title">学科包</h2>
        <p class="section-sub">按学科深度定制的专业知识库，覆盖术语、案例、引用来源</p>
        <div class="spec-banner">
          <span>即将上线：内分泌科 · 心血管科</span>
        </div>
      </div>
    </section>

    <!-- System requirements -->
    <section class="sys-section">
      <div class="container">
        <h2 class="section-title">系统要求</h2>
        <div class="sys-grid">
          <div class="sys-card">
            <h4>macOS</h4>
            <p>macOS 12 (Monterey) 或更高<br/>Apple Silicon / Intel</p>
          </div>
          <div class="sys-card">
            <h4>Windows</h4>
            <p>Windows 10 (64-bit) 或更高<br/>x86_64</p>
          </div>
          <div class="sys-card">
            <h4>通用要求</h4>
            <p>4 GB RAM 以上<br/>500 MB 可用磁盘空间</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container" style="text-align:center;">
        <h2>准备好开始了吗？</h2>
        <p style="color:var(--text-secondary);margin:12px 0 24px;">免费试用，体验 AI 驱动的医学科普写作</p>
        <router-link to="/download" class="btn-primary">立即下载</router-link>
      </div>
    </section>

    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const features = [
  { icon: 'AI', title: '智能科普写作', desc: '支持 17 种科普形式，AI 辅助生成各章节内容' },
  { icon: 'V', title: '防编造验证', desc: '自动验证医学事实准确性，标记可疑内容' },
  { icon: 'K', title: '知识增强', desc: 'RAG + 术语注入 + Few-shot 示例，确保专业性' },
  { icon: 'I', title: '图像生成', desc: '配套科普插图自动生成，支持多种风格' },
  { icon: 'E', title: '富文本编辑', desc: '形式感知编辑器，按科普形式加载对应工具集' },
  { icon: 'P', title: '多平台发布', desc: '7 种发布平台适配，一键导出对应格式' },
]
</script>

<style scoped lang="scss">
.hero {
  padding: 100px 0 80px; text-align: center;
  background: linear-gradient(180deg, #f0f5ff 0%, #fff 100%);

  h1 { font-size: 48px; font-weight: 700; line-height: 1.2; letter-spacing: -1px; }
  .hero-sub { font-size: 18px; color: var(--text-secondary); max-width: 560px; margin: 20px auto 32px; }
}

.hero-actions {
  display: flex; gap: 12px; justify-content: center;
}
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

.section-title { font-size: 28px; font-weight: 600; text-align: center; margin-bottom: 16px; }
.section-sub { text-align: center; color: var(--text-secondary); margin-bottom: 32px; }

.features-section { padding: 80px 0; }
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.feature-card {
  background: #f9fafb; border: 1px solid var(--border); border-radius: 12px;
  padding: 28px; transition: box-shadow 0.2s;
  &:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  h3 { font-size: 16px; margin: 12px 0 8px; }
  p { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
}
.feature-icon {
  width: 40px; height: 40px; background: var(--primary-light); color: var(--primary);
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700;
}

.spec-section { padding: 60px 0; background: #f8faff; }
.spec-banner {
  text-align: center; padding: 24px; background: #fff; border: 1px dashed var(--border);
  border-radius: 12px; color: var(--text-secondary); font-size: 15px;
}

.sys-section { padding: 60px 0; }
.sys-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.sys-card {
  text-align: center; padding: 24px; background: #f9fafb; border-radius: 12px;
  h4 { margin-bottom: 8px; }
  p { font-size: 13px; color: var(--text-secondary); line-height: 1.8; }
}

.cta-section { padding: 80px 0; background: #f0f5ff; }
</style>
