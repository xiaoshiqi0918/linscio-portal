<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <h1 class="page-title">帮助中心</h1>
      <p class="page-sub">常见问题解答</p>

      <div class="faq-list">
        <div v-for="(item, i) in faqs" :key="i" class="faq-item">
          <div class="faq-q" @click="toggle(i)">
            <span>{{ item.q }}</span>
            <span class="faq-arrow" :class="{ open: openIndex === i }">&#9660;</span>
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
    q: '如何获取授权码？',
    a: '请联系我们 (linscio@163.com) 获取授权码。获取后在授权门户 (portal.linscio.com.cn) 登录并激活。',
  },
  {
    q: '软件到期后还能使用吗？',
    a: '授权到期后仍可正常使用已有功能，但软件更新和学科包下载功能将被限制。续费后恢复所有功能。',
  },
  {
    q: '如何换绑新设备？',
    a: '1) 在新设备上打开 MedComm 软件，确保已联网；2) 按提示获取 6 位换机码；3) 在授权门户「我的设备」页面输入换机码完成换绑。每个授权周期最多可换绑 2 次。',
  },
  {
    q: '学科包是什么？',
    a: '学科包是按学科深度定制的专业知识库，包含术语、案例和引用来源，让 AI 生成的内容更加专业准确。购买学科包需要有正式版授权。',
  },
  {
    q: '支持哪些操作系统？',
    a: 'macOS 12 (Monterey) 或更高版本（支持 Apple Silicon 和 Intel），以及 Windows 10/11 64 位系统。',
  },
  {
    q: '忘记密码怎么办？',
    a: '在授权门户登录页面点击「忘记密码」，输入注册邮箱，系统将发送重置链接到您的邮箱。',
  },
]
</script>

<style scoped lang="scss">
.page { padding: 48px 24px; max-width: 720px; }
.page-title { font-size: 28px; font-weight: 600; margin-bottom: 8px; }
.page-sub { color: var(--text-secondary); margin-bottom: 32px; }

.faq-list { display: flex; flex-direction: column; gap: 12px; }
.faq-item { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.faq-q {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px; cursor: pointer; font-weight: 500; font-size: 15px;
  background: #fafafa; transition: background 0.2s;
  &:hover { background: #f0f5ff; }
}
.faq-arrow {
  font-size: 10px; color: var(--text-muted); transition: transform 0.2s;
  &.open { transform: rotate(180deg); }
}
.faq-a {
  padding: 12px 20px 16px; font-size: 14px; color: var(--text-secondary); line-height: 1.8;
  border-top: 1px solid var(--border); background: #fff;
}
</style>
