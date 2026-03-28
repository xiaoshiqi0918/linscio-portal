import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: () => import('@/views/Home.vue') },
    { path: '/features', name: 'Features', component: () => import('@/views/Features.vue') },
    { path: '/download', name: 'Download', component: () => import('@/views/Download.vue') },
    { path: '/help', name: 'Help', component: () => import('@/views/Help.vue') },
    { path: '/contact', name: 'Contact', component: () => import('@/views/Contact.vue') },
  ],
  scrollBehavior: () => ({ top: 0 }),
})
