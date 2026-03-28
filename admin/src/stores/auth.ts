import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAdminAuth = defineStore('adminAuth', () => {
  const token = ref(localStorage.getItem('admin_session_token') || '')
  const isLoggedIn = computed(() => !!token.value)

  function setToken(t: string) {
    token.value = t
    localStorage.setItem('admin_session_token', t)
  }

  function clear() {
    token.value = ''
    localStorage.removeItem('admin_session_token')
  }

  return { token, isLoggedIn, setToken, clear }
})
