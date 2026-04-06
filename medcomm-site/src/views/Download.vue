<template>
  <div>
    <SiteHeader />
    <main class="container page">
      <p class="page-label">下载</p>
      <h1 class="page-title">下载 MedComm</h1>
      <p class="page-sub">选择对应平台下载，安装后使用授权码激活即可开始使用。</p>

      <div v-if="loading" class="loading-hint">正在获取版本信息...</div>

      <!-- 客户端下载 -->
      <h2 class="section-label">客户端</h2>
      <div class="download-list">
        <div v-for="p in platforms" :key="p.id" class="download-card" :class="{ 'download-card--disabled': p.status === 'suspended' }">
          <div class="download-icon">{{ p.icon }}</div>
          <div class="download-info">
            <h3>{{ p.name }}</h3>
            <p class="download-desc">{{ p.desc }}</p>
            <p class="download-meta">
              <template v-if="p.status === 'suspended'">
                <span class="status-tag status-tag--suspended">暂未开放</span>
              </template>
              <template v-else>
                v{{ productVersion }} · {{ p.filename || '等待版本信息' }}
              </template>
            </p>
          </div>
          <button v-if="p.status !== 'suspended'" class="download-btn" @click="handleDownload(p.id)">下载</button>
          <span v-else class="download-btn download-btn--disabled">敬请期待</span>
        </div>
      </div>

      <!-- ComfyUI 组件包 -->
      <template v-if="bundles.length">
        <h2 class="section-label">MedPic 绘图组件包（可选）</h2>
        <p class="section-note">安装客户端后可按需下载。基础包随 MedComm 授权开放，进阶包需额外授权。</p>
        <div class="download-list">
          <div v-for="b in bundles" :key="b.id" class="download-card">
            <div class="download-icon">🎨</div>
            <div class="download-info">
              <h3>{{ b.name }}</h3>
              <p class="download-desc">{{ b.description }}</p>
              <p class="download-meta">v{{ b.version }} · 需在客户端内下载安装</p>
            </div>
            <span class="download-btn download-btn--disabled">客户端内安装</span>
          </div>
        </div>
      </template>

      <!-- 更新日志 -->
      <div v-if="changelog.length" class="release-notes">
        <h3>更新日志</h3>
        <div v-for="cl in changelog" :key="cl.version" class="changelog-entry">
          <h4>v{{ cl.version }}</h4>
          <ul>
            <li v-for="(c, ci) in cl.changes" :key="ci">{{ c }}</li>
          </ul>
        </div>
      </div>

      <div class="notice-box">
        <span class="notice-icon">ⓘ</span>
        <p>点击「下载」后将跳转至 <strong>portal.linscio.com.cn</strong> 登录页。登录后验证授权状态，确认有效后自动获取下载链接。如尚未拥有授权码，可先<router-link to="/contact" class="link">联系我们</router-link>获取试用资格。</p>
      </div>

      <section class="sys-section">
        <h2 class="sys-title">系统要求</h2>
        <div class="sys-columns">
          <div class="sys-col">
            <h4>macOS（Apple Silicon）</h4>
            <div class="sys-table">
              <div class="sys-row"><span>最低系统版本</span><span>macOS 12</span></div>
              <div class="sys-row"><span>支持芯片</span><span>Apple Silicon（M1 / M2 / M3 / M4）</span></div>
              <div class="sys-row"><span>磁盘空间</span><span>客户端 500 MB · MedPic 需额外 5 GB+</span></div>
              <div class="sys-row"><span>内存</span><span>8 GB 以上（MedPic 建议 16 GB）</span></div>
            </div>
          </div>
          <div class="sys-col">
            <h4>Windows</h4>
            <div class="sys-table">
              <div class="sys-row"><span>最低系统版本</span><span>Windows 10</span></div>
              <div class="sys-row"><span>架构</span><span>x64</span></div>
              <div class="sys-row"><span>磁盘空间</span><span>客户端 500 MB · MedPic 需额外 5 GB+</span></div>
              <div class="sys-row"><span>内存</span><span>8 GB 以上（MedPic 建议 16 GB）</span></div>
            </div>
          </div>
        </div>
        <p class="sys-note">* macOS Intel 版本暂停开发，后续视需求开放。MedPic 绘图功能（ComfyUI）为可选组件，未安装不影响其他功能使用。</p>
      </section>
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SiteHeader from '@/components/layout/SiteHeader.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'

const productVersion = ref('0.1.1')
const loading = ref(true)

interface PlatformItem {
  id: string
  name: string
  desc: string
  icon: string
  filename: string
  status: string
}

interface BundleItem {
  id: string
  name: string
  description: string
  version: string
}

interface ChangelogEntry {
  version: string
  changes: string[]
}

const platforms = ref<PlatformItem[]>([
  { id: 'mac-arm64', name: 'macOS（Apple Silicon）', desc: '适用于 M1 / M2 / M3 / M4 · macOS 12 及以上', icon: '⊛', filename: '', status: 'available' },
  { id: 'mac-x64', name: 'macOS（Intel）', desc: '适用于 Intel 芯片 Mac · macOS 12 及以上', icon: '⊛', filename: '', status: 'available' },
  { id: 'win-x64', name: 'Windows', desc: '适用于 Windows 10 / 11 · x64', icon: '⊞', filename: '', status: 'available' },
])

const bundles = ref<BundleItem[]>([])
const changelog = ref<ChangelogEntry[]>([])

onMounted(async () => {
  try {
    const portalApi = import.meta.env.VITE_URL_PORTAL || ''
    const res = await fetch(`${portalApi}/api/download/product-info`)
    if (res.ok) {
      const data = await res.json()
      const medcomm = data.products?.MedComm || data.products?.medcomm
      if (medcomm) {
        productVersion.value = medcomm.latest_version || productVersion.value
        const files = medcomm.download_files || {}
        const statusMap = medcomm.platform_status || {}
        for (const p of platforms.value) {
          if (files[p.id]) p.filename = files[p.id]
          if (statusMap[p.id]) p.status = statusMap[p.id]
        }
        changelog.value = medcomm.changelog || []
      }
      if (data.bundles) {
        bundles.value = data.bundles
          .filter((b: any) => b.product_id?.toLowerCase() === 'medcomm')
          .map((b: any) => ({ id: b.id, name: b.name, description: b.description, version: b.version }))
      }
    }
  } catch {
    // fallback to defaults
  } finally {
    loading.value = false
  }
})

function handleDownload(platform: string) {
  const portalBase = import.meta.env.VITE_URL_PORTAL
  const redirect = encodeURIComponent(window.location.href)
  window.location.href = `${portalBase}/download?product=medcomm&platform=${platform}&redirect=${redirect}`
}
</script>

<style scoped lang="scss">
.page { padding: 60px 24px 80px; max-width: 900px; }

.page-label { font-size: 14px; color: var(--text-muted); margin-bottom: 8px; }
.page-title {
  font-size: 32px; font-weight: 700; color: var(--text-primary); margin-bottom: 16px;
  letter-spacing: -0.5px;
}
.page-sub { font-size: 15px; color: var(--text-secondary); margin-bottom: 40px; }
.section-label {
  font-size: 14px; font-weight: 600; color: var(--text-secondary);
  margin-bottom: 12px; margin-top: 8px;
}
.section-note { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }

.loading-hint { text-align: center; color: var(--text-muted); font-size: 14px; margin-bottom: 20px; }

/* ── Download cards ── */
.download-list { display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px; }
.download-card {
  display: flex; align-items: center; gap: 20px;
  background: var(--bg-card); border: 1px solid var(--border-card);
  border-radius: 14px; padding: 24px 28px;
  &--disabled { opacity: 0.55; }
}
.download-icon {
  width: 48px; height: 48px; flex-shrink: 0;
  background: var(--bg-surface); border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: var(--text-muted);
}
.download-info {
  flex: 1;
  h3 { font-size: 15px; font-weight: 500; color: var(--text-primary); margin-bottom: 4px; }
}
.download-desc { font-size: 13px; color: var(--text-muted); line-height: 1.6; }
.download-meta { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.download-btn {
  padding: 8px 24px; border: 1px solid var(--border); border-radius: 6px;
  background: transparent; color: var(--text-primary); font-size: 14px;
  cursor: pointer; flex-shrink: 0; transition: all 0.15s;
  &:hover { border-color: var(--primary); color: var(--primary); }
  &--disabled { cursor: default; opacity: 0.5; font-size: 13px; &:hover { border-color: var(--border); color: var(--text-primary); } }
}

.status-tag {
  display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500;
  &--suspended { background: #fef3c7; color: #92400e; }
}

/* ── Release notes / changelog ── */
.release-notes {
  padding: 20px 24px; background: var(--bg-surface); border: 1px solid var(--border-card);
  border-radius: 12px; margin-bottom: 24px;
  h3 { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 16px; }
}
.changelog-entry {
  margin-bottom: 16px;
  &:last-child { margin-bottom: 0; }
  h4 { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
  ul { padding-left: 18px; margin: 0; }
  li { font-size: 13px; color: var(--text-secondary); line-height: 1.8; }
}

/* ── Notice box ── */
.notice-box {
  display: flex; gap: 12px; padding: 20px 24px;
  background: var(--bg-surface); border: 1px solid var(--border-card);
  border-radius: 12px; margin-bottom: 48px;
  p { font-size: 13px; color: var(--text-secondary); line-height: 1.8; }
  strong { color: var(--text-primary); }
}
.notice-icon { font-size: 16px; color: var(--text-muted); flex-shrink: 0; margin-top: 2px; }
.link { color: var(--text-primary); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }

/* ── System requirements ── */
.sys-section { margin-top: 16px; }
.sys-title { font-size: 16px; font-weight: 500; color: var(--text-secondary); margin-bottom: 24px; }
.sys-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.sys-col {
  h4 { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 16px; }
}
.sys-table { display: flex; flex-direction: column; }
.sys-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 0; border-bottom: 1px solid var(--border); font-size: 13px;
  span:first-child { color: var(--text-muted); }
  span:last-child { color: var(--text-secondary); text-align: right; }
}
.sys-note { font-size: 12px; color: var(--text-muted); margin-top: 20px; line-height: 1.8; }

@media (max-width: 640px) {
  .download-card { flex-direction: column; align-items: flex-start; }
  .download-btn { align-self: flex-end; }
  .sys-columns { grid-template-columns: 1fr; gap: 32px; }
  .page-title { font-size: 24px; }
}
</style>
