import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('session_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('session_token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  },
)

export default api

// Auth
export const authRegister = (data: { email: string; password: string }) =>
  api.post('/api/auth/register', data)
export const authVerify = (data: { email: string; code: string }) =>
  api.post('/api/auth/verify', data)
export const authLogin = (data: { email: string; password: string }) =>
  api.post('/api/auth/login', data)
export const authLogout = () => api.post('/api/auth/logout')
export const authForgotPassword = (data: { email: string }) =>
  api.post('/api/auth/forgot-password', data)
export const authResetPassword = (data: { token: string; new_password: string }) =>
  api.post('/api/auth/reset-password', data)

// License
export const licenseActivate = (data: { code: string; device_fingerprint?: string; device_name?: string }) =>
  api.post('/api/license/activate', data)
export const licenseStatusAll = () =>
  api.get('/api/license/status/all')

// Products
export const getProducts = () => api.get('/api/products')

// Download
export const downloadSoftware = (data: { product_id: string; platform: string }) =>
  api.post('/api/download/software', data)

// Device
export const deviceVerify = (data: { product_id: string; code: string }) =>
  api.post('/api/device/change-code/verify', data)

// Account
export const changePassword = (data: { old_password: string; new_password: string }) =>
  api.post('/api/account/change-password', data)
export const changePhone = (data: { phone: string }) =>
  api.patch('/api/account/phone', data)
export const deleteAccount = (data: { password: string }) =>
  api.delete('/api/account', { data })
