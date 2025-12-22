import { createRouter, createWebHistory } from 'vue-router'

import Home from "@/components/Home.vue";
import Login from "@/components/Login.vue";
import HomeUsuario from "@/components/HomeUsuario.vue";
import HomeMonitor from "@/components/HomeMonitor.vue";
import HomeAdmin from "@/components/HomeAdmin.vue";

const routes = [
  { path: '/', redirect: '/Home' },
  { path: '/Home', component: Home },

  { path: '/login', component: Login },

  { path: '/usuario', component: HomeUsuario },
  { path: '/monitor', component: HomeMonitor },
  { path: '/admin', component: HomeAdmin },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
