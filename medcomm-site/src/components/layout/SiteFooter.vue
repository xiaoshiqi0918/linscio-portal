<template>
  <footer class="footer">
    <div class="container footer-inner">
      <span>&copy; {{ new Date().getFullYear() }} LinScio MedComm</span>
      <div>
        <a href="https://www.linscio.com.cn" target="_blank">LinScio 主站</a>
        <span class="sep">|</span>
        <a href="https://portal.linscio.com.cn" target="_blank">用户登录</a>
        <span class="sep">|</span>
        <a href="mailto:linscio@163.com">linscio@163.com</a>
      </div>
    </div>
  </footer>
</template>

<style scoped lang="scss">
.footer { padding: 24px 0; border-top: 1px solid var(--border); margin-top: 80px; }
.footer-inner {
  display: flex; justify-content: space-between; font-size: 13px; color: var(--text-muted);
  a { color: var(--text-muted); &:hover { color: var(--primary); } }
}
.sep { margin: 0 8px; color: #ddd; }
</style>
