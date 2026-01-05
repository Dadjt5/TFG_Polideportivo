import { createRouter, createWebHistory } from 'vue-router'

import Home from '../components/Home.vue'
import HomeUsuarioFinal from '../components/HomeUsuarioFinal.vue'
import Buscar from '../components/Buscar.vue'
import Login from '../components/Login.vue'
import Registro from '../components/Registro.vue'
import DetalleActividad from '../components/DetalleActividad.vue'
import DetalleInstalacion from '../components/DetalleInstalacion.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home-usuario', component: HomeUsuarioFinal },
  { path: '/home', component: Home },
  { path: '/buscar', component: Buscar },
  { path: '/login', component: Login },
  { path: '/registrarse', component: Registro },
  { path: '/actividades/:id',
    component: DetalleActividad,
    name: 'detalle-actividad',
    props: true
  },
  { path: '/instalaciones/:id',
    component: DetalleInstalacion,
    name: 'detalle-instalacion',
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
