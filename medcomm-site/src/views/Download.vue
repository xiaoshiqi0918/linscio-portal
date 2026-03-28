<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <h1 class="page-title">下载 MedComm</h1>
      <p class="page-sub">选择您的操作系统，登录后即可下载</p>

      <div class="platform-grid">
        <div v-for="p in platforms" :key="p.id" class="platform-card" @click="handleDownload(p.id)">
          <div class="platform-icon">{{ p.icon }}</div>
          <h3>{{ p.name }}</h3>
          <p>{{ p.desc }}</p>
          <span class="download-btn">下载</span>
        </div>
      </div>

      <div class="download-note">
        <h3>下载说明</h3>
        <ul>
          <li>点击下载按钮后将跳转至授权门户完成身份验证</li>
          <li>您需要有效的授权码才能下载，如需获取请联系我们</li>
          <li>下载完成后打开安装包，按照提示安装即可</li>
        </ul>
      </div>

      <div class="sys-req">
        <h3>系统要求</h3>
        <ul>
          <li><strong>macOS:</strong> macOS 12 (Monterey) 或更高，Apple Silicon / Intel</li>
          <li><strong>Windows:</strong> Windows 10 (64-bit) 或更高</li>
          <li><strong>内存:</strong> 4 GB RAM 以上</li>
          <li><strong>磁盘:</strong> 500 MB 可用空间</li>
        </ul>
      </div>
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const platforms = [
  { id: 'mac-arm64', name: 'macOS (Apple Silicon)', desc: 'M1 / M2 / M3 / M4', icon: 'A' },
  { id: 'mac-x64', name: 'macOS (Intel)', desc: 'Intel 芯片 Mac', icon: 'I' },
  { id: 'win-x64', name: 'Windows', desc: 'Windows 10/11 64位', icon: 'W' },
]

function handleDownload(platform: string) {
  const portalBase = 'https://portal.linscio.com.cn'
  const redirect = encodeURIComponent(window.location.href)
  window.location.href = `${portalBase}/download?product=MedComm&platform=${platform}&redirect=${redirect}`
}
</script>

<style scoped lang="scss">
.page { padding: 48px 24px; max-width: 800px; }
.page-title { font-size: 28px; font-weight: 600; margin-bottom: 8px; }
.page-sub { color: var(--text-secondary); margin-bottom: 32px; }

.platform-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }
.platform-card {
  text-align: center; padding: 32px 20px; background: #f9fafb;
  border: 1px solid var(--border); border-radius: 12px; cursor: pointer;
  transition: all 0.2s;
  &:hover { border-color: var(--primary); box-shadow: 0 4px 12px rgba(26,86,219,0.1); }
  h3 { font-size: 15px; margin: 12px 0 6px; }
  p { font-size: 12px; color: var(--text-muted); margin-bottom: 16px; }
}
.platform-icon {
  width: 48px; height: 48px; margin: 0 auto; background: var(--primary-light);
  color: var(--primary); border-radius: 12px; display: flex; align-items: center;
  justify-content: center; font-size: 18px; font-weight: 700;
}
.download-btn {
  display: inline-block; padding: 6px 20px; background: var(--primary); color: #fff;
  border-radius: 6px; font-size: 13px; font-weight: 500;
}

.download-note, .sys-req {
  margin-bottom: 32px;
  h3 { font-size: 16px; margin-bottom: 12px; }
  ul { padding-left: 20px; color: var(--text-secondary); font-size: 14px; line-height: 2; }
}
</style>
