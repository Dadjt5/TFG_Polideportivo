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
import DetallePabellon from '../components/DetallePabellon.vue'
import Notificaciones from '../components/Notificaciones.vue'
import Perfil from '../components/Perfil.vue'
import ComprarAbonosBonos from '../components/ComprarAbonosBonos.vue'
import VerAbonosBonos from '../components/VerAbonosBonos.vue'
import TarjetaDeportivaAnual from '../components/TarjetaDeportivaAnual.vue'
import ModificarDatosPersonales from '../components/ModificarDatosPersonales.vue'
import ListaDeActividades from '../components/ListaDeActividades.vue'
import ReservasRealizadas from '../components/ReservasRealizadas.vue'
import Foro from '../components/Foro.vue'
import NuevoMonitor from '../components/NuevoMonitor.vue'
import HomeMonitor from '../components/HomeMonitor.vue'
import DetalleSesion from '../components/DetalleSesion.vue'
import ReservaActividad from '../components/ReservaActividad.vue'
import Alquiler from '../components/Alquiler.vue'
import HomeAdministrador from '../components/HomeAdministrador.vue'
import NuevoAdministrador from '../components/NuevoAdministrador.vue'
import NuevoUsuarioFinal from '../components/NuevoUsuarioFinal.vue'
import GestionarUsuarios from '../components/GestionarUsuarios.vue'
import DetalleUsuarioFinal from '../components/DetalleUsuarioFinal.vue'
import DetalleMonitor from '../components/DetalleMonitor.vue'
import DetalleAdministrador from '../components/DetalleAdministrador.vue'
import GestionarEspacios from '../components/GestionarEspacios.vue'
import EditarInstalacion from '../components/EditarInstalacion.vue'
import EditarActividad from '../components/EditarActividad.vue'
import EditarSesion from '../components/EditarSesion.vue'
import NuevaInstalacion from '../components/NuevaInstalacion.vue'
import NuevoPabellon from '../components/NuevoPabellon.vue'
import NuevaSesion from '../components/NuevaSesion.vue'
import NuevaActividad from '../components/NuevaActividad.vue'
import GestionarActividades from '../components/GestionarActividades.vue'
import GestionarTarifas from '../components/GestionarTarifas.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: Home, meta: { public: true } },
  { path: '/buscar', component: Buscar, meta: { public: true } },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/registrarse', component: Registro, meta: { public: true } },
  { path: '/registrar/monitor', component: NuevoMonitor, meta: { requiresAuth: true }},
  { path: '/registrar/administrador', component: NuevoAdministrador, meta: { requiresAuth: true }},
  { path: '/registrar/usuario', component: NuevoUsuarioFinal, meta: { requiresAuth: true }},
  {
    path: '/home-usuario',
    component: HomeUsuarioFinal,
    meta: { requiresAuth: true, role: 'usuario_final' }
  },
  {
    path: '/home-monitor',
    component: HomeMonitor,
    meta: { requiresAuth: true, role: 'monitor' }
  },
  {
    path: '/home-administrador',
    component: HomeAdministrador,
    meta: { requiresAuth: true, role: 'administrador' }
  },
  {
    path: '/actividades/:id',
    component: DetalleActividad,
    name: 'detalle-actividad',
    props: true,
    meta: { public: true }
  },
  {
    path: '/admin/actividades/:id',
    component: EditarActividad,
    name: 'editar-actividad',
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/instalaciones/:id',
    component: DetalleInstalacion,
    name: 'detalle-instalacion',
    props: true,
    meta: { public: true }
  },
  {
    path: '/admin/instalaciones/:id/',
    component: EditarInstalacion,
    name: 'editar-instalacion',
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/pabellones/:id',
    component: DetallePabellon,
    name: 'detalle-pabellon',
    props: true,
    meta: { public: true }
  },
  {
    path: '/usuarioFinal/:id',
    component: DetalleUsuarioFinal,
    name: 'detalle-usuarioFinal',
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/monitor/:id',
    component: DetalleMonitor,
    name: 'detalle-monitor',
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/administrador/:id',
    component: DetalleAdministrador,
    name: 'detalle-administrador',
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/actividades/:idAct/sesiones/:idSesion',
    component: DetalleSesion,
    name: 'detalle-sesion',
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/actividades/:idAct/sesiones/:idSesion',
    component: EditarSesion,
    name: 'editar-sesion',
    props: true,
    meta: { requiresAuth: true }
  },
  { path: '/notificaciones', component: Notificaciones, meta: { requiresAuth: true } },
  { path: '/reservas-realizadas', component: ReservasRealizadas, meta: { requiresAuth: true } },
  { path: '/perfil', component: Perfil, meta: { requiresAuth: true } },
  { path: '/comprar-abonos', component: ComprarAbonosBonos, meta: { requiresAuth: true } },
  { path: '/contacto', component: Contacto, meta: { public: true } },
  { path: '/faq', component: FAQ, meta: { public: true } },
  { path: '/actividades', component: ListaDeActividades, meta: {public: true} },
  { path: '/ver-tda', component: TarjetaDeportivaAnual, meta: { requiresAuth: true }},
  { path: '/modificar-datos', component: ModificarDatosPersonales, meta: { requiresAuth: true }},
  { path: '/ver-abonos', component: VerAbonosBonos, meta: { requiresAuth: true }},
  { path: '/foro', component: Foro, meta: {requiresAuth: true }},
  {
    path: '/actividad/:id/reservar',
    component: ReservaActividad,
    name: 'reservar-actividad',
    props: true,
    meta: { requiresAuth: true }
  },
    {
    path: '/instalacion/:id/reservar',
    component: Alquiler,
    name: 'reservar-instalacion',
    props: true,
    meta: { requiresAuth: true }
  },
  { path: '/crear/pabellon', component: NuevoPabellon, name: 'crear-pabellon', meta: { requiresAuth: true } },
  { path: '/crear/instalacion', component: NuevaInstalacion, name: 'crear-instalacion', meta: { requiresAuth: true } },
  { path: '/crear/actividad', component: NuevaActividad, name: 'crear-actividad', meta: { requiresAuth: true } },
  { path: '/crear/sesion', component: NuevaSesion, name: 'crear-sesion', meta: { requiresAuth: true } },
  { path: '/crear/tarifa/instalacion', component: NuevaTarifaInstalacion, name: 'crear-tarifa-instalacion', meta: { requiresAuth: true } },
  { path: '/crear/tarifa/comun', component: NuevaTarifaActividadComun, name: 'crear-tarifa-actividad-comun', meta: { requiresAuth: true } },
  { path: '/crear/tarifa/grupos', component: NuevaTarifaGruposReducidos, name: 'crear-tarifa-grupo-reducido', meta: { requiresAuth: true } },
  { path: '/crear/tarifa/fisioterapia', component: NuevaTarifaFisioterapia, name: 'crear-tarifa-fisioterapia', meta: { requiresAuth: true } },
  { path: '/gestion/usuarios', component: GestionarUsuarios, name: 'gestionar-usuarios', meta: { requiresAuth: true } },
  { path: '/gestion/espacios', component: GestionarEspacios, name: 'gestionar-espacios', meta: { requiresAuth: true } },
  { path: '/gestion/actividades', component: GestionarActividades, name: 'gestionar-actividades', meta: { requiresAuth: true } },
  { path: '/gestion/tarifas', component: GestionarTarifas, name: 'gestionar-tarifas', meta: { requiresAuth: true } },
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
    if (auth.role === 'administrador') return '/home-administrador';
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
