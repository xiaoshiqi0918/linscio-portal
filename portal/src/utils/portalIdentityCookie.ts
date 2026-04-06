/** 在 *.linscio.com.cn 子域间共享「展示用」登录邮箱（非鉴权；鉴权仍以 session_token 为准） */

const COOKIE_NAME = 'linscio_portal_email'
const MAX_AGE_SEC = 60 * 60 * 24 * 30

function cookieRootDomain(): string | null {
  if (typeof window === 'undefined') return null
  const h = window.location.hostname
  if (h === 'localhost' || h === '127.0.0.1') return null
  const parts = h.split('.')
  if (parts.length >= 3) return `.${parts.slice(-3).join('.')}`
  if (parts.length === 2) return `.${parts.join('.')}`
  return null
}

export function setPortalEmailCookie(email: string) {
  const domain = cookieRootDomain()
  if (!domain || !email) return
  const secure = window.location.protocol === 'https:' ? '; Secure' : ''
  document.cookie = `${COOKIE_NAME}=${encodeURIComponent(email)}; path=/; domain=${domain}; max-age=${MAX_AGE_SEC}; SameSite=Lax${secure}`
}

export function clearPortalEmailCookie() {
  const domain = cookieRootDomain()
  if (!domain) return
  document.cookie = `${COOKIE_NAME}=; path=/; domain=${domain}; max-age=0; SameSite=Lax`
}

export function readPortalEmailCookie(): string {
  if (typeof document === 'undefined') return ''
  const m = document.cookie.match(new RegExp(`(?:^|; )${COOKIE_NAME}=([^;]*)`))
  return m ? decodeURIComponent(m[1]) : ''
}
