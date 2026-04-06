import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_session_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

function formatErrorDetail(detail: unknown): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail))
    return detail.map((x: { msg?: string }) => x?.msg).filter(Boolean).join('; ') || '请求失败'
  return '没有权限'
}

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err.response?.status
    // 401：会话失效，需重新登录。403：多为管理端 IP 白名单等，不应清 token（否则表现为「登录后立刻被踢出」）
    if (status === 401) {
      localStorage.removeItem('admin_session_token')
      window.location.href = '/login'
      return Promise.reject(err)
    }
    if (status === 403) {
      ElMessage.error(formatErrorDetail(err.response?.data?.detail))
      return Promise.reject(err)
    }
    return Promise.reject(err)
  },
)

export default api

// Auth
export const adminLogin = (data: { email: string; password: string }) =>
  api.post('/api/auth/login', data)

// Stats
export const getStatsOverview = () => api.get('/admin/stats/overview')

// Users
export const getUsers = (params: any) => api.get('/admin/users', { params })
export const banUser = (id: number, data: any) => api.post(`/admin/users/${id}/ban`, data)
export const unbanUser = (id: number) => api.post(`/admin/users/${id}/unban`)
export const deleteUser = (id: number, data?: { reason?: string }) =>
  api.post(`/admin/users/${id}/delete`, data ?? {})

// Licenses
export const generateLicenses = (data: any) => api.post('/admin/licenses/generate', data)
export const getLicenses = (params: any) => api.get('/admin/licenses', { params })
export const voidLicenseCode = (id: number) => api.post(`/admin/licenses/${id}/void`)

// Devices
export const getDevices = (params: any) => api.get('/admin/devices', { params })
export const forceRebind = (data: any) => api.post('/admin/devices/reset', data)

// Migrations
export const getMigrations = (params: any) => api.get('/admin/migrations', { params })
export const handleMigration = (id: number, data: any) => api.post(`/admin/migrations/${id}/handle`, data)

// Specialties
export const getSpecialties = () => api.get('/admin/specialties')
export const updateSpecialtyPolicy = (id: string, productId: string, data: any) =>
  api.put(`/admin/specialties/${id}/policy?product_id=${productId}`, data)

// Releases
export const getReleases = () => api.get('/admin/releases')

// Products
export const getProducts = () => api.get('/admin/products')
export const updateProduct = (id: string, data: any) => api.patch(`/admin/products/${id}`, data)

// Logs
export const getDownloadLogs = (params: any) => api.get('/admin/logs/downloads', { params })
export const getAdminLogs = (params: any) => api.get('/admin/logs/admin', { params })

// Security
export const getSecurityLimits = (params: any) => api.get('/admin/security/limits', { params })
export const unlockSecurity = (data: any) => api.post('/admin/security/unlock', data)
