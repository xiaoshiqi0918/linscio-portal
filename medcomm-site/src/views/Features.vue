<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <h1 class="page-title">功能介绍</h1>

      <section class="feature-section">
        <h2>主要功能</h2>
        <div class="feature-list">
          <div class="feature-item">
            <h3>智能科普写作</h3>
            <p>支持 17 种科普形式（科普长文、短视频脚本、漫画脚本、手册、知识卡片等），AI 根据主题、受众和形式自动生成各章节内容，支持 SSE 流式输出实时展示。</p>
          </div>
          <div class="feature-item">
            <h3>AI 图像生成</h3>
            <p>配套科普插图自动生成，支持多种视觉风格，按内容上下文智能匹配最佳图文搭配。</p>
          </div>
        </div>
      </section>

      <section class="feature-section">
        <h2>写作工具</h2>
        <div class="feature-list">
          <div class="feature-item">
            <h3>形式感知编辑器</h3>
            <p>根据科普形式自动加载对应的 Tiptap 扩展，如漫画分镜、口播脚本标注、互动问答块等。</p>
          </div>
          <div class="feature-item">
            <h3>防编造验证</h3>
            <p>AI 生成内容经过多层验证管线，自动标记缺乏证据的医学声明，确保科普内容的准确性。</p>
          </div>
          <div class="feature-item">
            <h3>知识增强 (RAG)</h3>
            <p>术语注入、FTS5 全文检索、Few-shot 示例匹配，让 AI 基于专业知识库生成内容。</p>
          </div>
        </div>
      </section>

      <section class="feature-section">
        <h2>内容管理</h2>
        <div class="feature-list">
          <div class="feature-item">
            <h3>文献管理</h3>
            <p>集成 PubMed、Semantic Scholar、CrossRef 多源检索，支持 BibTeX/RIS 导入，引用自动格式化。</p>
          </div>
          <div class="feature-item">
            <h3>模板与导出</h3>
            <p>内置多种科普模板，支持 HTML/DOCX/PDF 多格式导出，适配 7 种主流发布平台。</p>
          </div>
          <div class="feature-item">
            <h3>知识库管理</h3>
            <p>系统知识 + 用户自定义知识，支持学科包扩展，按领域组织专业术语和范文。</p>
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
.page { padding: 48px 24px; max-width: 800px; }
.page-title { font-size: 28px; font-weight: 600; margin-bottom: 40px; }

.feature-section {
  margin-bottom: 48px;
  h2 { font-size: 20px; font-weight: 600; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 2px solid var(--primary-light); }
}

.feature-list { display: flex; flex-direction: column; gap: 20px; }
.feature-item {
  padding: 20px 24px; background: #f9fafb; border-radius: 10px;
  h3 { font-size: 16px; margin-bottom: 8px; }
  p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; }
}
</style>
