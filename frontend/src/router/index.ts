import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/HomeView.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/ProfileView.vue'), meta: { requiresAuth: true } },
  { path: '/wordlists', name: 'Wordlists', component: () => import('../views/WordlistView.vue') },
  { path: '/wordlists/:id/practice', name: 'Practice', component: () => import('../views/PracticeView.vue'), meta: { requiresAuth: true } },
  { path: '/wordlists/:id/dictation', name: 'Dictation', component: () => import('../views/DictationView.vue'), meta: { requiresAuth: true } },
  { path: '/errors', name: 'ErrorBook', component: () => import('../views/ErrorBookView.vue'), meta: { requiresAuth: true } },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/leaderboard', name: 'Leaderboard', component: () => import('../views/LeaderboardView.vue') },
  { path: '/favorites', name: 'Favorites', component: () => import('../views/FavoritesView.vue'), meta: { requiresAuth: true } },
  { path: '/checkin', name: 'Checkin', component: () => import('../views/CheckinView.vue'), meta: { requiresAuth: true } },
  { path: '/admin', name: 'Admin', component: () => import('../views/admin/AdminLayout.vue'), meta: { requiresAuth: true },
    children: [
      { path: 'wordlists', component: () => import('../views/admin/WordlistManage.vue') },
      { path: 'content', component: () => import('../views/admin/ContentManage.vue') },
      { path: 'users', component: () => import('../views/admin/UserManage.vue') },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('zhixu_access_token')
    if (!token) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  next()
})

export default router
