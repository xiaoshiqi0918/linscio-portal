import { createRouter, createWebHistory } from 'vue-router'
import { useAdminAuth } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
    },
    {
      path: '/',
      component: () => import('@/components/layout/AdminLayout.vue'),
      meta: { auth: true },
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/Index.vue') },
        { path: 'users', name: 'Users', component: () => import('@/views/users/Index.vue') },
        { path: 'licenses', name: 'Licenses', component: () => import('@/views/licenses/Index.vue') },
        { path: 'licenses/generate', name: 'LicenseGenerate', component: () => import('@/views/licenses/Generate.vue') },
        { path: 'devices', name: 'Devices', component: () => import('@/views/devices/Index.vue') },
        { path: 'migrations', name: 'Migrations', component: () => import('@/views/migrations/Index.vue') },
        { path: 'specialties', name: 'Specialties', component: () => import('@/views/specialties/Index.vue') },
        { path: 'bundles', name: 'Bundles', component: () => import('@/views/bundles/Index.vue') },
        { path: 'releases', name: 'Releases', component: () => import('@/views/releases/Index.vue') },
        { path: 'products', name: 'Products', component: () => import('@/views/products/Index.vue') },
        { path: 'logs/downloads', name: 'DownloadLogs', component: () => import('@/views/logs/Downloads.vue') },
        { path: 'logs/admin', name: 'AdminLogs', component: () => import('@/views/logs/Admin.vue') },
        { path: 'security', name: 'Security', component: () => import('@/views/security/Index.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAdminAuth()
  if (to.meta.auth && !auth.isLoggedIn) return { name: 'Login' }
  if (to.name === 'Login' && auth.isLoggedIn) return '/'
})

export default router
