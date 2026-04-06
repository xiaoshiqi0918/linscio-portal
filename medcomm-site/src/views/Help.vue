<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <p class="page-label">帮助中心</p>
      <h1 class="page-title">常见问题</h1>
      <p class="page-sub">找不到答案？<router-link to="/contact" class="link">联系我们</router-link>，通常 1–2 个工作日内回复。</p>

      <div class="faq-list">
        <div v-for="(item, i) in faqs" :key="i" class="faq-item" @click="toggle(i)">
          <div class="faq-q">
            <span>{{ item.q }}</span>
            <span class="faq-toggle" :class="{ open: openIndex === i }">+</span>
          </div>
          <div v-show="openIndex === i" class="faq-a">{{ item.a }}</div>
        </div>
      </div>
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const openIndex = ref(-1)
function toggle(i: number) { openIndex.value = openIndex.value === i ? -1 : i }

const faqs = [
  {
    q: '如何激活授权码？',
    a: '登录授权门户 (portal.linscio.com.cn)，进入「激活授权码」页面，输入您获得的授权码并确认即可完成激活。',
  },
  {
    q: '如何下载软件？',
    a: '登录授权门户后，在「下载」页面选择您的操作系统版本进行下载。下载完成后打开安装包，按照提示安装即可。',
  },
  {
    q: '如何换机？',
    a: '在新设备上打开 MedComm 软件，确保已联网；按提示获取 6 位换机码；在授权门户「我的设备」页面输入换机码完成换绑。每个授权周期最多可换绑 2 次。',
  },
  {
    q: '授权到期后软件还能用吗？',
    a: '授权到期后仍可正常使用已有功能，但软件更新和学科包下载功能将被限制。续费后恢复所有功能。',
  },
  {
    q: '学科包是什么？',
    a: '学科包是按学科深度定制的专业知识库，包含术语、案例和引用来源，让内容创作更加专业准确。购买学科包需要有正式版授权。',
  },
  {
    q: 'MedPic 绘图功能是什么？',
    a: 'MedPic 是 MedComm 内置的 AI 医学绘图模块，基于 ComfyUI 本地引擎，可在本机生成科普配图、解剖示意等医学图像。数据全部在本地处理，不上传至云端。',
  },
  {
    q: '如何安装 MedPic 绘图组件包？',
    a: '安装 MedComm 客户端后，首次进入 MedPic 页面会提示下载基础绘图组件包。选择您的硬件档位后点击「下载基础组件包」，客户端会自动完成下载、校验和安装。组件包约 3-5 GB，请确保磁盘空间充足。',
  },
  {
    q: 'MedPic 对电脑配置有什么要求？',
    a: 'MedPic 绘图功能为可选组件，不安装不影响其他功能。基础使用建议 8 GB 内存，流畅使用建议 16 GB 以上。目前支持 macOS（Apple Silicon）和 Windows（x64），macOS Intel 版本暂停开发。',
  },
  {
    q: 'MedPic 进阶绘图包和基础包有什么区别？',
    a: '基础包包含 SD1.5 模型和 7 种预设场景工作流，随 MedComm 授权免费使用。进阶包（如 SDXL Pro、儿科专包、解剖图谱包）提供更高质量的模型和专业工作流，需额外授权。',
  },
  {
    q: 'macOS Intel 版本为什么暂停了？',
    a: 'ComfyUI 绘图引擎在 Intel Mac 上需要特殊的依赖编译环境，目前暂停该平台的 MedPic 功能开发。客户端基础功能（写作、内容管理）仍可正常使用，后续视用户需求考虑恢复。',
  },
  {
    q: '如何联系客服？',
    a: '发送邮件至 linscio@163.com，或通过微信添加客服（备注 linscio），通常 1–2 个工作日内回复。',
  },
]
</script>

<style scoped lang="scss">
.page { padding: 60px 24px 80px; max-width: 900px; }

.page-label {
  font-size: 14px; color: var(--text-muted); margin-bottom: 8px;
}
.page-title {
  font-size: 32px; font-weight: 700; color: var(--text-primary); margin-bottom: 16px;
  letter-spacing: -0.5px;
}
.page-sub {
  font-size: 15px; color: var(--text-secondary); margin-bottom: 48px;
}
.link { color: var(--text-primary); text-decoration: underline; text-underline-offset: 3px; }

.faq-list { display: flex; flex-direction: column; }

.faq-item {
  border-bottom: 1px solid var(--border); cursor: pointer;
}
.faq-q {
  display: flex; justify-content: space-between; align-items: center;
  padding: 24px 0; font-size: 15px; font-weight: 500; color: var(--text-secondary);
  transition: color 0.15s;
  &:hover { color: var(--text-primary); }
}
.faq-toggle {
  font-size: 20px; color: var(--text-muted); transition: transform 0.2s;
  flex-shrink: 0; margin-left: 16px;
  &.open { transform: rotate(45deg); }
}
.faq-a {
  padding: 0 0 24px; font-size: 14px; color: var(--text-secondary); line-height: 1.8;
}
</style>
