import { createRouter, createWebHistory } from 'vue-router'

import Home from '../components/Home.vue'
import Buscar from '../components/Buscar.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: Home },
  { path: '/buscar', component: Buscar }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
