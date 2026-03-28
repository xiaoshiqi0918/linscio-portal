import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: () => import('@/views/Home.vue') },
    { path: '/contact', name: 'Contact', component: () => import('@/views/Contact.vue') },
    { path: '/legal/privacy', name: 'Privacy', component: () => import('@/views/legal/Privacy.vue') },
    { path: '/legal/terms', name: 'Terms', component: () => import('@/views/legal/Terms.vue') },
    { path: '/legal', redirect: '/legal/privacy' },
  ],
  scrollBehavior: () => ({ top: 0 }),
})
