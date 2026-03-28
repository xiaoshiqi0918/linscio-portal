import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const sessionToken = ref(localStorage.getItem('session_token') || '')
  const isAdmin = ref(localStorage.getItem('is_admin') === '1')

  const isLoggedIn = computed(() => !!sessionToken.value)

  function setSession(token: string, admin: boolean) {
    sessionToken.value = token
    isAdmin.value = admin
    localStorage.setItem('session_token', token)
    localStorage.setItem('is_admin', admin ? '1' : '0')
  }

  function clearSession() {
    sessionToken.value = ''
    isAdmin.value = false
    localStorage.removeItem('session_token')
    localStorage.removeItem('is_admin')
  }

  return { sessionToken, isAdmin, isLoggedIn, setSession, clearSession }
})
