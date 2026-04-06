/** 读取门户在 .linscio.com.cn 上写入的展示用邮箱 Cookie */

const COOKIE_NAME = 'linscio_portal_email'

export function getPortalEmailFromCookie(): string {
  if (typeof document === 'undefined') return ''
  const m = document.cookie.match(new RegExp(`(?:^|; )${COOKIE_NAME}=([^;]*)`))
  return m ? decodeURIComponent(m[1]) : ''
}
