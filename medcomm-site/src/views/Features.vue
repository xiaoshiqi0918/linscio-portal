<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <p class="page-label">功能介绍</p>
      <h1 class="page-title">MedComm 能做什么</h1>
      <p class="page-sub">从内容创作到内容管理，MedComm 覆盖科普写作的完整工作流。</p>

      <!-- 主要功能 -->
      <section class="section">
        <h2 class="section-label">主要功能</h2>
        <div class="hero-grid">
          <div class="hero-card hero-card--green">
            <span class="hero-tag hero-tag--green">科普写作</span>
            <h3>结构化科普内容生成</h3>
            <p>基于模板与知识库，快速生成结构化规范的科普内容，支持多种格式输出与学科包扩展。</p>
            <div class="hero-deco hero-deco--green">
              <div class="deco-bar"></div>
              <div class="deco-bar deco-bar--short"></div>
            </div>
          </div>
          <div class="hero-card hero-card--purple">
            <span class="hero-tag hero-tag--purple">图像生成</span>
            <h3>配套图像一键生成</h3>
            <p>根据写作内容自动生成配套图像，无需额外设计工具，图文一体完成创作。</p>
            <div class="hero-deco hero-deco--purple">
              <div class="deco-shape"></div>
              <div class="deco-shape deco-shape--sm"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- MedPic 绘图 -->
      <section class="section">
        <h2 class="section-label">MedPic 医学绘图</h2>
        <div class="hero-grid">
          <div class="hero-card hero-card--blue">
            <span class="hero-tag hero-tag--blue">本地绘图</span>
            <h3>ComfyUI 本地引擎</h3>
            <p>基于 ComfyUI 的本地 AI 绘图引擎，数据不出本机，保护患者隐私与医疗数据安全。</p>
            <div class="hero-deco hero-deco--blue">
              <div class="deco-shape"></div>
              <div class="deco-shape deco-shape--sm"></div>
            </div>
          </div>
          <div class="hero-card hero-card--orange">
            <span class="hero-tag hero-tag--orange">智能提示词</span>
            <h3>AI 辅助生成提示词</h3>
            <p>根据写作主题和场景，AI 智能生成绘图提示词，无需专业绘图经验即可产出高质量配图。</p>
            <div class="hero-deco hero-deco--orange">
              <div class="deco-bar"></div>
              <div class="deco-bar deco-bar--short"></div>
            </div>
          </div>
        </div>
        <div class="feature-rows" style="margin-top: 28px;">
          <div class="feature-row">
            <span class="feature-icon">🎨</span>
            <div>
              <h3>多场景预设工作流</h3>
              <p>内置科普插画、解剖示意、流程图等 7 种医学场景工作流模板，选择场景即可开始绘制。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">⚡</span>
            <div>
              <h3>硬件自适应</h3>
              <p>根据设备性能自动调整绘图参数，普通办公电脑到专业工作站均可使用，步骤和分辨率按硬件档位优化。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📦</span>
            <div>
              <h3>按需扩展</h3>
              <p>基础绘图组件随 MedComm 授权开放；SDXL 进阶包、儿科专包、解剖图谱包等可按需额外授权下载。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 写作工具 -->
      <section class="section">
        <h2 class="section-label">写作工具</h2>
        <div class="feature-rows">
          <div class="feature-row">
            <span class="feature-icon">📋</span>
            <div>
              <h3>文献引用管理</h3>
              <p>内置文献管理系统，写作时可直接引用，确保内容有据可查。支持学科包扩展，按专业方向丰富文献范围。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">🔍</span>
            <div>
              <h3>确定性验证</h3>
              <p>对生成内容进行准确性验证，适配不同层面精度的表达风格，让输出内容更自然、更准确。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">⊞</span>
            <div>
              <h3>丰富样式</h3>
              <p>内置多种结构模版，覆盖独立科目的结构类型，选择模版和主题搭配填充内容，省却从零开始的设计困扰。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 内容管理 -->
      <section class="section">
        <h2 class="section-label">内容管理</h2>
        <div class="feature-rows">
          <div class="feature-row">
            <span class="feature-icon">📄</span>
            <div>
              <h3>创作库</h3>
              <p>所有历史内容统一存储，支持分类管理与快速检索。历史作品随时可调阅，积累越多效率越高。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">◎</span>
            <div>
              <h3>知识库</h3>
              <p>自建知识内容与学科包内容严格隔离，更新学科包不影响你积累的私有数据。本地存储，离线可用。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">✏</span>
            <div>
              <h3>发布管理</h3>
              <p>管理内容的发布状态，追踪已发布与草稿内容，使下系统化运营和后续复用。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="cta-section">
        <div class="cta-card">
          <div class="cta-left">
            <h2>准备好试试了吗？</h2>
            <p>下载软件，使用授权码激活后即可开始使用全部功能。</p>
          </div>
          <div class="cta-right">
            <router-link to="/download" class="cta-btn">下载软件</router-link>
            <router-link to="/contact" class="cta-btn">联系我们</router-link>
          </div>
        </div>
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
.page { padding: 60px 24px 0; max-width: 900px; }

.page-label { font-size: 14px; color: var(--text-muted); margin-bottom: 8px; }
.page-title {
  font-size: 32px; font-weight: 700; color: var(--text-primary); margin-bottom: 16px;
  letter-spacing: -0.5px;
}
.page-sub { font-size: 15px; color: var(--text-secondary); margin-bottom: 48px; }

.section { margin-bottom: 56px; }
.section-label { font-size: 14px; font-weight: 500; color: var(--text-muted); margin-bottom: 20px; }

/* ── Hero cards ── */
.hero-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.hero-card {
  border-radius: 16px; padding: 28px; position: relative; overflow: hidden;
  min-height: 240px; display: flex; flex-direction: column;
  h3 { font-size: 18px; font-weight: 600; margin-bottom: 10px; }
  p { font-size: 13px; line-height: 1.7; max-width: 280px; }
}
.hero-card--green {
  background: #e8f5e9; color: #1b3a1b;
  h3 { color: #1b3a1b; }
  p { color: #3a5a3a; }
}
.hero-card--purple {
  background: #f3e8ff; color: #2d1b4e;
  h3 { color: #2d1b4e; }
  p { color: #5a3a7a; }
}
.hero-card--blue {
  background: #e3f2fd; color: #0d47a1;
  h3 { color: #0d47a1; }
  p { color: #1565c0; }
}
.hero-card--orange {
  background: #fff3e0; color: #e65100;
  h3 { color: #e65100; }
  p { color: #bf360c; }
}
.hero-tag {
  display: inline-block; padding: 3px 10px; border-radius: 4px;
  font-size: 11px; font-weight: 500; margin-bottom: 14px; width: fit-content;
}
.hero-tag--green { background: #43a047; color: #fff; }
.hero-tag--purple { background: #8e24aa; color: #fff; }
.hero-tag--blue { background: #1976d2; color: #fff; }
.hero-tag--orange { background: #e65100; color: #fff; }

.hero-deco {
  position: absolute; bottom: 16px; left: 28px; right: 28px;
  height: 48px; display: flex; flex-direction: column; gap: 8px; justify-content: flex-end;
}
.hero-deco--green {
  .deco-bar {
    height: 10px; border-radius: 5px; background: rgba(67, 160, 71, 0.35); width: 70%;
    &--short { width: 45%; }
  }
}
.hero-deco--purple {
  flex-direction: row; gap: 12px; align-items: flex-end;
  .deco-shape {
    width: 48px; height: 36px; border-radius: 8px 8px 2px 2px;
    background: rgba(142, 36, 170, 0.25);
    &--sm { width: 36px; height: 24px; }
  }
}
.hero-deco--blue {
  flex-direction: row; gap: 12px; align-items: flex-end;
  .deco-shape {
    width: 48px; height: 36px; border-radius: 8px 8px 2px 2px;
    background: rgba(25, 118, 210, 0.25);
    &--sm { width: 36px; height: 24px; }
  }
}
.hero-deco--orange {
  .deco-bar {
    height: 10px; border-radius: 5px; background: rgba(230, 81, 0, 0.3); width: 65%;
    &--short { width: 40%; }
  }
}

/* ── Feature rows ── */
.feature-rows { display: flex; flex-direction: column; gap: 28px; }
.feature-row {
  display: flex; gap: 16px; align-items: flex-start;
  h3 { font-size: 14px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
  p { font-size: 13px; color: var(--text-muted); line-height: 1.7; }
}
.feature-icon {
  width: 36px; height: 36px; flex-shrink: 0; margin-top: 2px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}

/* ── CTA ── */
.cta-section { padding: 40px 0 80px; background: var(--bg-alt); }
.cta-card {
  background: var(--bg-card); border: 1px solid var(--border-card);
  border-radius: 16px; padding: 48px 40px;
  display: flex; justify-content: space-between; align-items: center; gap: 40px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.cta-left {
  h2 { font-size: 20px; font-weight: 600; color: var(--text-primary); margin-bottom: 10px; }
  p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; }
}
.cta-right { display: flex; flex-direction: column; gap: 10px; flex-shrink: 0; }
.cta-btn {
  padding: 10px 28px; border: 1px solid var(--border); border-radius: 6px;
  font-size: 14px; color: var(--text-primary); text-decoration: none;
  text-align: center; transition: all 0.15s; white-space: nowrap;
  &:hover { border-color: var(--primary); color: var(--primary); }
}

@media (max-width: 640px) {
  .hero-grid { grid-template-columns: 1fr; }
  .page-title { font-size: 24px; }
  .cta-card { flex-direction: column; text-align: center; padding: 36px 24px; }
  .cta-right { flex-direction: row; }
}
</style>
