<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <p class="page-label">功能介绍</p>
      <h1 class="page-title">MedComm 能做什么</h1>
      <p class="page-sub">从一键生成到去AI化改写，从AIGC检测到多格式导出，MedComm 覆盖科普内容创作的完整工作流。</p>

      <!-- 主要功能 -->
      <section class="section">
        <h2 class="section-label">主要功能</h2>
        <div class="hero-grid">
          <div class="hero-card hero-card--green">
            <span class="hero-tag hero-tag--green">智能写作</span>
            <h3>一键生成全文</h3>
            <p>选择主题和模板后一键生成完整文章，流式实时预览写作过程，支持正文、小结等多章节自动衔接。</p>
            <div class="hero-deco hero-deco--green">
              <div class="deco-bar"></div>
              <div class="deco-bar deco-bar--short"></div>
            </div>
          </div>
          <div class="hero-card hero-card--purple">
            <span class="hero-tag hero-tag--purple">去AI化</span>
            <h3>自动去AI化改写</h3>
            <p>生成完成后自动进入多轮改写，优化句式节奏、段落衔接与叙事结构，降低AIGC检测率。</p>
            <div class="hero-deco hero-deco--purple">
              <div class="deco-shape"></div>
              <div class="deco-shape deco-shape--sm"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- AI 绘图 -->
      <section class="section">
        <h2 class="section-label">AI 绘图 <span style="font-size: 11px; color: #e65100; font-weight: 400;">开发中</span></h2>
        <div class="hero-grid">
          <div class="hero-card hero-card--blue">
            <span class="hero-tag hero-tag--blue">文生图</span>
            <h3>文字描述生成配图</h3>
            <p>输入文字描述即可生成科普配图，支持 Midjourney、DALL·E、ComfyUI 等多种外部 API 提供商。</p>
            <div class="hero-deco hero-deco--blue">
              <div class="deco-shape"></div>
              <div class="deco-shape deco-shape--sm"></div>
            </div>
          </div>
          <div class="hero-card hero-card--orange">
            <span class="hero-tag hero-tag--orange">图生图</span>
            <h3>基于参考图的风格转换</h3>
            <p>上传参考图，通过 AI 进行风格转换和内容优化，快速生成符合场景的科普配图。</p>
            <div class="hero-deco hero-deco--orange">
              <div class="deco-bar"></div>
              <div class="deco-bar deco-bar--short"></div>
            </div>
          </div>
        </div>
        <div class="feature-rows" style="margin-top: 28px;">
          <div class="feature-row">
            <span class="feature-icon">🔑</span>
            <div>
              <h3>多提供商支持</h3>
              <p>支持配置 Midjourney、ComfyUI、DALL·E 等多种绘图 API，按需选择最适合的图像生成服务。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">✨</span>
            <div>
              <h3>智能提示词</h3>
              <p>根据写作主题和场景，AI 智能生成绘图提示词，无需专业绘图经验即可产出高质量配图。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 写作工具 -->
      <section class="section">
        <h2 class="section-label">写作与编辑</h2>
        <div class="feature-rows">
          <div class="feature-row">
            <span class="feature-icon">🔍</span>
            <div>
              <h3>AIGC 段落检测</h3>
              <p>段落级AI内容检测，精准定位AIGC特征显著的段落，支持针对性手动改写或AI辅助改写，直到检测通过。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">✍️</span>
            <div>
              <h3>AI 写作面板</h3>
              <p>选中段落即可使用AI改写、润色、扩写、缩写等能力，编辑器实时更新，支持自动保存与手动保存。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📋</span>
            <div>
              <h3>模板库管理</h3>
              <p>自定义章节结构与配置预设，支持拖拽排序编辑，模板驱动内容生成流程，创建文章时自动填充配置。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📚</span>
            <div>
              <h3>参考文献绑定</h3>
              <p>从文献库绑定参考文献，导出时自动附加到文章末尾，格式规范，无需手动整理。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📤</span>
            <div>
              <h3>多格式导出</h3>
              <p>支持 Word（.docx）、HTML、Markdown、纯文本导出，格式与编辑器一致，参考文献自动附加。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 平台与管理 -->
      <section class="section">
        <h2 class="section-label">平台与管理</h2>
        <div class="feature-rows">
          <div class="feature-row">
            <span class="feature-icon">🎯</span>
            <div>
              <h3>多平台风格适配</h3>
              <p>适配微信公众号、知乎、小红书等平台风格，自动调整语域、篇幅和表达方式，一篇内容多场景复用。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📄</span>
            <div>
              <h3>创作库</h3>
              <p>所有历史内容统一存储，支持分类管理与快速检索。历史作品随时可调阅，积累越多效率越高。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📦</span>
            <div>
              <h3>学科包扩展</h3>
              <p>按专业方向独立购买学科包，内容本地存储、离线可用，更新学科包不影响你的原有数据。</p>
            </div>
          </div>
          <div class="feature-row">
            <span class="feature-icon">📊</span>
            <div>
              <h3>智能模型路由</h3>
              <p>根据任务类型自动选择最优 LLM 模型，写作、改写、检测等不同环节匹配最适合的模型能力。</p>
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
