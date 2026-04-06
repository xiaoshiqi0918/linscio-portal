import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import {
  clearPortalEmailCookie,
  readPortalEmailCookie,
  setPortalEmailCookie,
} from '@/utils/portalIdentityCookie'

function initialUserEmail(): string {
  const fromLs = localStorage.getItem('user_email') || ''
  if (fromLs) return fromLs
  if (localStorage.getItem('session_token')) {
    const fromCk = readPortalEmailCookie()
    if (fromCk) {
      localStorage.setItem('user_email', fromCk)
      return fromCk
    }
  }
  return ''
}

export const useAuthStore = defineStore('auth', () => {
  const sessionToken = ref(localStorage.getItem('session_token') || '')
  const isAdmin = ref(localStorage.getItem('is_admin') === '1')
  const userEmail = ref(initialUserEmail())

  const isLoggedIn = computed(() => !!sessionToken.value)

  function setSession(token: string, admin: boolean, email: string) {
    sessionToken.value = token
    isAdmin.value = admin
    userEmail.value = email
    localStorage.setItem('session_token', token)
    localStorage.setItem('is_admin', admin ? '1' : '0')
    localStorage.setItem('user_email', email)
    setPortalEmailCookie(email)
  }

  function clearSession() {
    sessionToken.value = ''
    isAdmin.value = false
    userEmail.value = ''
    localStorage.removeItem('session_token')
    localStorage.removeItem('is_admin')
    localStorage.removeItem('user_email')
    clearPortalEmailCookie()
  }

  return { sessionToken, isAdmin, userEmail, isLoggedIn, setSession, clearSession }
})
