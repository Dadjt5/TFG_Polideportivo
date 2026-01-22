import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Home from '../components/Home.vue'
import Contacto from '../components/Contacto.vue'
import FAQ from '../components/FAQ.vue'
import HomeUsuarioFinal from '../components/HomeUsuarioFinal.vue'
import Buscar from '../components/Buscar.vue'
import Login from '../components/Login.vue'
import Registro from '../components/Registro.vue'
import DetalleActividad from '../components/DetalleActividad.vue'
import DetalleInstalacion from '../components/DetalleInstalacion.vue'
import Notificaciones from '../components/Notificaciones.vue'
import Perfil from '../components/Perfil.vue'
import ComprarAbonosBonos from '../components/ComprarAbonosBonos.vue'
import VerAbonosBonos from '../components/VerAbonosBonos.vue'
import TarjetaDeportivaAnual from '../components/TarjetaDeportivaAnual.vue'
import ModificarDatosPersonales from '../components/ModificarDatosPersonales.vue'
import ListaDeActividades from '../components/ListaDeActividades.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: Home, meta: { public: true } },
  { path: '/buscar', component: Buscar, meta: { public: true } },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/registrarse', component: Registro, meta: { public: true } },
  {
    path: '/home-usuario',
    component: HomeUsuarioFinal,
    meta: { requiresAuth: true, role: 'usuario_final' }
  },
  {
    path: '/actividades/:id',
    component: DetalleActividad,
    name: 'detalle-actividad',
    props: true,
    meta: { public: true }
  },
  {
    path: '/instalaciones/:id',
    component: DetalleInstalacion,
    name: 'detalle-instalacion',
    props: true,
    meta: { public: true }
  },
  { path: '/notificaciones', component: Notificaciones, meta: { requiresAuth: true } },
  { path: '/perfil', component: Perfil, meta: { requiresAuth: true } },
  { path: '/comprar-abonos', component: ComprarAbonosBonos, meta: { requiresAuth: true } },
  { path: '/contacto', component: Contacto, meta: { public: true } },
  { path: '/faq', component: FAQ, meta: { public: true } },
  { path: '/actividades', component: ListaDeActividades, meta: {public: true} },
  { path: '/ver-tda', component: TarjetaDeportivaAnual, meta: { requiresAuth: true }},
  //{ path: '/ver-deportes-favoritos', component: DeportesFavoritos, meta: { requiresAuth: true }},
  { path: '/modificar-datos', component: ModificarDatosPersonales, meta: { requiresAuth: true }},
  { path: '/ver-abonos', component: VerAbonosBonos, meta: { requiresAuth: true }},
]

/* Cada vez que se accede a una página se redirige el scrollbar arriba */
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  }
})

/* Antes de acceder a una direccion revisamos los campos clave y las redirecciones necesarias cuando hay usuarios logueados */
router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (!auth.user) {
    await auth.fetchUser();
  }

  if (to.path === '/home') {
    if (auth.role === 'usuario_final') return '/home-usuario';
    if (auth.role === 'monitor') return '/home-monitor';
    if (auth.role === 'admin') return '/home-admin';
  }

  if (to.meta.public) {
    return true;
  }

  if (!auth.isAuthenticated) {
    return '/login';
  }

  if (to.meta.role && auth.role !== to.meta.role) {
    return '/login';
  }

  return true;
});

export default router
