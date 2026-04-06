<template>
  <div>
    <SiteHeader />

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <div class="hero-tag">LinScio MedComm</div>
        <h1 class="hero-title">结构化内容创作，<br/>专注表达本身</h1>
        <p class="hero-sub">
          MedComm 帮助你快速组织思路、生成规范内容、支持学科<br/>
          包按需扩展、适配不同专业场景。
        </p>
        <div class="hero-actions">
          <router-link to="/download" class="btn-ghost">下载软件</router-link>
          <router-link to="/features" class="btn-ghost">了解功能</router-link>
        </div>
        <p class="hero-note">支持 macOS（Apple Silicon）· Windows ｜ 授权码激活后使用</p>
      </div>
    </section>

    <!-- Core features -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">核心功能</h2>
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
        <p class="section-sub">
          学科包是针对专业方向的内容扩展，一次购买永久有效，独立于基础授权更新。
        </p>
        <div class="spec-grid">
          <div v-for="s in specialties" :key="s.name" class="spec-card">
            <div class="spec-card__header">
              <span>{{ s.desc }}</span>
            </div>
            <div class="spec-card__body">
              <h3>{{ s.name }}</h3>
            </div>
            <div class="spec-card__footer">
              <span class="spec-tag">即将上线</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- System requirements -->
    <section class="sys-section">
      <div class="container">
        <h2 class="section-title">系统要求</h2>
        <div class="sys-table">
          <div class="sys-row sys-row--header">
            <div>平台</div>
            <div>macOS（Apple Silicon）</div>
            <div>平台</div>
            <div>Windows 10 / 11</div>
          </div>
          <div class="sys-row">
            <div>芯片</div>
            <div>M1 / M2 / M3 / M4</div>
            <div>架构</div>
            <div>x64</div>
          </div>
          <div class="sys-row">
            <div>磁盘空间</div>
            <div>客户端 500 MB · MedPic 额外 5 GB+</div>
            <div>磁盘空间</div>
            <div>客户端 500 MB · MedPic 额外 5 GB+</div>
          </div>
          <div class="sys-row">
            <div>内存</div>
            <div>8 GB（MedPic 建议 16 GB）</div>
            <div>内存</div>
            <div>8 GB（MedPic 建议 16 GB）</div>
          </div>
        </div>
        <p class="sys-note">* macOS Intel 版本暂停开发。MedPic 绘图功能（ComfyUI）为可选组件，未安装不影响其他功能。</p>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-card">
          <div class="cta-left">
            <h2>准备好开始了吗？</h2>
            <p>下载软件后使用授权码激活，学科包可在激活后按需购<br/>买。</p>
          </div>
          <div class="cta-right">
            <router-link to="/download" class="cta-btn">下载软件</router-link>
            <router-link to="/contact" class="cta-btn">联系我们</router-link>
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

const features = [
  { icon: '📋', title: '结构化输出', desc: '内容按层级模板生成，格式统一、减少反复调整的时间。' },
  { icon: '🎨', title: 'MedPic 医学绘图', desc: '基于 ComfyUI 的本地 AI 绘图引擎，数据不出本机。AI 智能提示词 + 多场景预设工作流，无需绘图经验。' },
  { icon: '📦', title: '学科包扩展', desc: '按专业方向独立购买，内容本地存储、离线可用，更新不覆盖自建内容。' },
  { icon: '◎', title: '本地优先', desc: '数据存储在本地，不依赖持续联网，断网状态下正常使用。' },
  { icon: '⊘', title: '内容隔离', desc: '各类内容与学科包内容严格分开，更新学科包不影响你的原有数据。' },
  { icon: '🔓', title: '授权到期不锁功能', desc: '授权到期后软件仍可正常使用，仅暂停更新通道，续费后恢复。' },
]

const specialties = [
  { name: '内分泌科', desc: '专科内容，构建基于内分泌方向的写作辅助能力' },
  { name: '心血管科', desc: '专科内容，围绕心血管方向知识构建写作辅助工具' },
  { name: '更多学科', desc: '更多专业方向的学科包将在后续持续推出' },
]
</script>

<style scoped lang="scss">
.section-title {
  font-size: 16px; font-weight: 500; color: var(--text-secondary);
  margin-bottom: 20px;
}
.section-sub {
  font-size: 14px; color: var(--text-muted); margin-bottom: 28px;
}

/* ── Hero ── */
.hero {
  padding: 80px 0 60px;
  background: linear-gradient(180deg, var(--bg-dark-secondary) 0%, var(--bg-dark-secondary) 10%, var(--bg-hero) 35%, var(--bg-page) 100%);
}
.hero-tag {
  font-size: 12px; color: rgba(255,255,255,0.85);
  margin-bottom: 28px; line-height: 1.6;
}
.hero-title {
  font-size: 36px; font-weight: 700; line-height: 1.25;
  color: var(--text-secondary); letter-spacing: -0.5px; margin-bottom: 20px;
}
.hero-sub {
  font-size: 14px; color: var(--text-secondary);
  line-height: 1.8; margin-bottom: 28px;
}
.hero-actions {
  display: flex; gap: 12px; margin-bottom: 20px;
}
.btn-ghost {
  padding: 10px 24px; border: 1px solid var(--border);
  border-radius: 6px; font-size: 14px; color: var(--text-primary);
  text-decoration: none; transition: all 0.15s;
  &:hover { border-color: var(--primary); color: var(--primary); }
}
.hero-note {
  font-size: 13px; color: var(--text-muted);
}

/* ── Features ── */
.features-section { padding: 60px 0 80px; background: var(--bg-alt); }
.feature-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
}
.feature-card {
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 14px;
  padding: 24px; color: var(--text-primary);
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  h3 { font-size: 15px; font-weight: 600; margin: 14px 0 8px; color: var(--text-primary); }
  p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; }
}
.feature-icon {
  font-size: 18px;
}

/* ── Specialty ── */
.spec-section { padding: 60px 0; }
.spec-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
}
.spec-card {
  background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 14px;
  padding: 24px; color: var(--text-primary);
  display: flex; flex-direction: column; min-height: 160px;
  &__header {
    font-size: 13px; color: var(--text-muted); margin-bottom: 12px; flex: 1;
  }
  &__body {
    h3 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }
  }
  &__footer { margin-top: auto; }
}
.spec-tag {
  display: inline-block; padding: 4px 12px; font-size: 12px;
  background: #e8f5e9; color: #2e7d32; border-radius: 4px; font-weight: 500;
}

/* ── System Requirements ── */
.sys-section { padding: 60px 0; }
.sys-table {
  display: grid; gap: 0;
  border-top: 1px solid var(--border);
}
.sys-row {
  display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 0;
  border-bottom: 1px solid var(--border);
  > div {
    padding: 14px 0; font-size: 13px; color: var(--text-secondary);
    &:nth-child(odd) { color: var(--text-muted); font-size: 12px; }
  }
  &--header > div { font-weight: 500; }
}
.sys-note { font-size: 12px; color: var(--text-muted); margin-top: 16px; line-height: 1.8; }

/* ── CTA ── */
.cta-section { padding: 60px 0 80px; background: var(--bg-alt); }
.cta-card {
  background: var(--bg-card); border: 1px solid var(--border-card);
  border-radius: 16px; padding: 48px 40px;
  display: flex; justify-content: space-between; align-items: center;
  gap: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.cta-left {
  h2 { font-size: 20px; font-weight: 600; color: var(--text-primary); margin-bottom: 10px; }
  p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; }
}
.cta-right {
  display: flex; flex-direction: column; gap: 10px; flex-shrink: 0;
}
.cta-btn {
  padding: 10px 28px; border: 1px solid var(--border);
  border-radius: 6px; font-size: 14px; color: var(--text-primary);
  text-decoration: none; text-align: center; transition: all 0.15s;
  white-space: nowrap;
  &:hover { border-color: var(--primary); color: var(--primary); }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .hero-title { font-size: 26px; }
  .hero-sub br, .cta-left p br { display: none; }
  .feature-grid, .spec-grid { grid-template-columns: 1fr; }
  .sys-row { grid-template-columns: 1fr 1fr; }
  .cta-card { flex-direction: column; text-align: center; padding: 36px 24px; }
  .cta-right { flex-direction: row; }
  .hero-actions { flex-direction: column; align-items: flex-start; }
}
</style>
