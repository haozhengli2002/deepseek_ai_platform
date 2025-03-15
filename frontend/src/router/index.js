import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Chat from '@/views/Chat.vue'
const routes = [
  { 
    path: '/',
    redirect: '/login' // 根路径自动跳转登录页
  },
  {
    path: '/login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    component: () => import('@/views/Register.vue')
  }, 
  {
    path: '/chat',
    component: () => import('@/views/Chat.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router