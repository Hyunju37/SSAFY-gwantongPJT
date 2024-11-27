// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import BoardCreateView from '@/views/BoardCreateView.vue'
import ChatbotView from '@/views/ChatbotView.vue'
import NewsPostsView from '@/views/NewsPostsView.vue'
import SearchNewsView from '@/views/SearchNewsView.vue'

import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    // meta: { requiresAuth: true } // 인증이 필요한 라우트
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guest: true } // 게스트만 접근 가능한 라우트
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupView,
    meta: { guest: true } // 게스트만 접근 가능한 라우트
  },
  {
    path: '/create-board',
    name: 'CreateBoard',
    component: BoardCreateView,
    meta: { requiresAuth: true } // 인증이 필요한 라우트
  },
  {
    path: '/chatbot',
    name: 'Chatbot',
    component: ChatbotView,
    meta: { requiresAuth: true } // 인증이 필요한 라우트
  },
  {
    path: '/news-posts/:id',
    name: 'NewsPosts',
    component: NewsPostsView,
    // meta: { requiresAuth: true },
    props: true // URL 파라미터를 props로 전달
  },
  {
    path: '/search',
    name: 'SearchNews',
    component: SearchNewsView,
    // meta: { requiresAuth: true }
  },
  // 기타 라우트들...
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guard: 인증이 필요한 라우트에 접근 시 로그인 여부 확인
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isLoggedIn = !!userStore.token

  if (to.meta.requiresAuth && !isLoggedIn) {
    // 인증이 필요한 라우트인데 로그인이 안 된 경우
    next({ name: 'Login' })
  } else if (to.meta.guest && isLoggedIn) {
    // 게스트만 접근 가능한 라우트인데 로그인이 된 경우
    next({ name: 'Dashboard' })
  } else {
    // 그 외의 경우
    next()
  }
})

export default router
