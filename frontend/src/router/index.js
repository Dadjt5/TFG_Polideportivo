import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

/* Genericos */
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import ListaDeActividades from '@/components/ListaDeActividades.vue'
import Perfil from '@/components/Perfil.vue'
import Foro from '@/components/Foro.vue'
import Notificaciones from '@/components/Notificaciones.vue'
import Contacto from '@/components/Contacto.vue'
import FAQ from '@/components/FAQ.vue'

/*********** Usuario final ***********/
import HomeUsuarioFinal from '@/components/usuarioFinal/HomeUsuarioFinal.vue'
import Buscar from '@/components/usuarioFinal/Buscar.vue'
import Registro from '@/components/usuarioFinal/Registro.vue'

// Detalles
import DetallePabellon from '@/components/usuarioFinal/detalles/DetallePabellon.vue'
import DetalleInstalacion from '@/components/usuarioFinal/detalles/DetalleInstalacion.vue'
import DetalleActividad from '@/components/usuarioFinal/detalles/DetalleActividad.vue'
import DetalleSesion from '@/components/usuarioFinal/detalles/DetalleSesion.vue'

// Perfil
import VerAbonosBonos from '@/components/usuarioFinal/perfil/VerAbonosBonos.vue'
import TarjetaDeportivaAnual from '@/components/usuarioFinal/perfil/TarjetaDeportivaAnual.vue'
import ModificarDatosPersonales from '@/components/usuarioFinal/perfil/ModificarDatosPersonales.vue'

// Compras
import ComprarAbonosBonos from '@/components/usuarioFinal/compras/ComprarAbonosBonos.vue'
import ReservaActividad from '@/components/usuarioFinal/compras/ReservaActividad.vue'
import Alquiler from '@/components/usuarioFinal/compras/Alquiler.vue'
import ReservasRealizadas from '@/components/usuarioFinal/compras/ReservasRealizadas.vue'
import Pago from '@/components/usuarioFinal/compras/Pago.vue'


/*********** Monitor ***********/
import HomeMonitor from '@/components/monitor/HomeMonitor.vue'


/*********** Administrador ***********/
import HomeAdministrador from '@/components/administrador/HomeAdministrador.vue'

import GestionarUsuarios from '@/components/administrador/GestionarUsuarios.vue'
import GestionarEspacios from '@/components/administrador/GestionarEspacios.vue'
import GestionarActividades from '@/components/administrador/GestionarActividades.vue'
import GestionarTarifas from '@/components/administrador/GestionarTarifas.vue'
import Configuracion from '@/components/administrador/Configuracion.vue'
import EstadisticasAdministrador from '@/components/administrador/EstadisticasAdministrador.vue'

// Nuevos
import NuevoUsuarioFinal from '@/components/administrador/nuevos/NuevoUsuarioFinal.vue'
import NuevoMonitor from '@/components/administrador/nuevos/NuevoMonitor.vue'
import NuevoAdministrador from '@/components/administrador/nuevos/NuevoAdministrador.vue'

import NuevoPabellon from '@/components/administrador/nuevos/NuevoPabellon.vue'
import NuevaInstalacion from '@/components/administrador/nuevos/NuevaInstalacion.vue'
import NuevaActividad from '@/components/administrador/nuevos/NuevaActividad.vue'
import NuevaSesion from '@/components/administrador/nuevos/NuevaSesion.vue'
import NuevoCanal from '@/components/administrador/nuevos/NuevoCanal.vue'

import NuevaTarifaTDA from '@/components/administrador/nuevos/NuevaTarifaTDA.vue'
import NuevaTarifaInstalacion from '@/components/administrador/nuevos/NuevaTarifaInstalacion.vue'
import NuevaTarifaActividadComun from '@/components/administrador/nuevos/NuevaTarifaActividadComun.vue'
import NuevaTarifaGrupoReducido from '@/components/administrador/nuevos/NuevaTarifaGrupoReducido.vue'
import NuevaTarifaFisioterapia from '@/components/administrador/nuevos/NuevaTarifaFisioterapia.vue'
import NuevoAbonoDeportivo from '@/components/administrador/nuevos/NuevoAbonoDeportivo.vue'
import NuevoAbonoVerano from '@/components/administrador/nuevos/NuevoAbonoVerano.vue'
import NuevoBono from '@/components/administrador/nuevos/NuevoBono.vue'


// Editar
import DetalleUsuarioFinal from '@/components/administrador/editar/DetalleUsuarioFinal.vue'
import DetalleMonitor from '@/components/administrador/editar/DetalleMonitor.vue'
import DetalleAdministrador from '@/components/administrador/editar/DetalleAdministrador.vue'

import EditarPabellon from '@/components/administrador/editar/EditarPabellon.vue'
import EditarInstalacion from '@/components/administrador/editar/EditarInstalacion.vue'
import EditarActividad from '@/components/administrador/editar/EditarActividad.vue'
import EditarSesion from '@/components/administrador/editar/EditarSesion.vue'
import EditarCanal from '@/components/administrador/editar/EditarCanal.vue'

import EditarTarifaTDA from '@/components/administrador/editar/EditarTarifaTDA.vue'
import EditarTarifaInstalacion from '@/components/administrador/editar/EditarTarifaInstalacion.vue'
import EditarTarifaActividadComun from '@/components/administrador/editar/EditarTarifaActividadComun.vue'
import EditarTarifaGrupoReducido from '@/components/administrador/editar/EditarTarifaGrupoReducido.vue'
import EditarTarifaFisioterapia from '@/components/administrador/editar/EditarTarifaFisioterapia.vue'
import EditarAbonoDeportivo from '@/components/administrador/editar/EditarAbonoDeportivo.vue'
import EditarAbonoVerano from '@/components/administrador/editar/EditarAbonoVerano.vue'
import EditarBono from '@/components/administrador/editar/EditarBono.vue'

const routes = [
  /******************* REDIRECCIÓN *******************/
  { path: '/', redirect: '/home' },

  /******************* GENÉRICAS *******************/
  { path: '/home', component: Home, meta: { public: true } },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/buscar', component: Buscar, meta: { public: true } },
  { path: '/actividades', component: ListaDeActividades, meta: { public: true } },
  { path: '/foro', component: Foro, meta: { requiresAuth: true } },
  { path: '/contacto', component: Contacto, meta: { public: true } },
  { path: '/faq', component: FAQ, meta: { public: true } },


  /******************* USUARIO FINAL *******************/
  {
    path: '/home-usuario',
    component: HomeUsuarioFinal,
    meta: { requiresAuth: true, role: 'usuario_final' }
  },
  { path: '/notificaciones', component: Notificaciones, meta: { requiresAuth: true } },
  { path: '/registrarse', component: Registro, meta: { public: true } },

  /* Perfil */
  { path: '/perfil', component: Perfil, meta: { requiresAuth: true } },
  { path: '/ver-tda', component: TarjetaDeportivaAnual, meta: { requiresAuth: true } },
  { path: '/ver-abonos', component: VerAbonosBonos, meta: { requiresAuth: true } },
  { path: '/modificar-datos', component: ModificarDatosPersonales, meta: { requiresAuth: true } },

  /* Comprar */
  { path: '/comprar-abonos', component: ComprarAbonosBonos, meta: { requiresAuth: true } },
  { path: '/reservas-realizadas', component: ReservasRealizadas, meta: { requiresAuth: true } },

  { path: '/actividad/:id/reservar', component: ReservaActividad, name: 'reservar-actividad', props: true, meta: { requiresAuth: true } },
  { path: '/instalacion/:id/reservar', component: Alquiler, name: 'reservar-instalacion', props: true, meta: { requiresAuth: true } },

  { path: '/pago/:tipo/:id', component: Pago, props: true, name: 'pasarela-pago', meta: { requiresAuth: true }},
  { path: '/pago/finalizado/:id', component: Pago, props: true, name: 'pago-finalizado', meta: { requiresAuth: true }},

  /* Detalle */
  { path: '/pabellones/:id', component: DetallePabellon, name: 'detalle-pabellon', props: true, meta: { public: true } },
  { path: '/instalaciones/:id', component: DetalleInstalacion, name: 'detalle-instalacion', props: true, meta: { public: true } },
  { path: '/actividades/:id', component: DetalleActividad, name: 'detalle-actividad', props: true, meta: { public: true } },
  { path: '/actividades/:idAct/sesiones/:idSesion', component: DetalleSesion, name: 'detalle-sesion', props: true, meta: { requiresAuth: true } },


  /******************* MONITOR *******************/
  { path: '/home-monitor', component: HomeMonitor, meta: { requiresAuth: true, role: 'monitor' } },


  /******************* ADMINISTRADOR *******************/
  { path: '/home-administrador', component: HomeAdministrador, meta: { requiresAuth: true, role: 'administrador' } },

  { path: '/gestion/usuarios', component: GestionarUsuarios, name: 'gestion-usuarios', meta: { requiresAuth: true } },
  { path: '/gestion/espacios', component: GestionarEspacios, name: 'gestion-espacios', meta: { requiresAuth: true } },
  { path: '/gestion/actividades', component: GestionarActividades, name: 'gestion-actividades', meta: { requiresAuth: true } },
  { path: '/gestion/tarifas', component: GestionarTarifas, name: 'gestion-tarifas', meta: { requiresAuth: true } },
  { path: '/configuracion', component: Configuracion, name: 'configuracion', meta: { requiresAuth: true } },
  { path: '/estadisticas/administrador', component: EstadisticasAdministrador, name: 'estadisticas-administrador', meta: { requiresAuth: true } },

  /* Nuevo */
  { path: '/registrar/usuario', component: NuevoUsuarioFinal, meta: { requiresAuth: true } },
  { path: '/registrar/monitor', component: NuevoMonitor, meta: { requiresAuth: true } },
  { path: '/registrar/administrador', component: NuevoAdministrador, meta: { requiresAuth: true } },

  { path: '/crear/pabellon', component: NuevoPabellon, name: 'crear-pabellon', meta: { requiresAuth: true } },
  { path: '/crear/instalacion', component: NuevaInstalacion, name: 'crear-instalacion', meta: { requiresAuth: true } },
  { path: '/crear/actividad', component: NuevaActividad, name: 'crear-actividad', meta: { requiresAuth: true } },
  { path: '/crear/sesion/:id', component: NuevaSesion, props: true, name: 'crear-sesion', meta: { requiresAuth: true } },
  { path: '/crear/canal/:id', component: NuevoCanal, props: true, name: 'crear-canal', meta: { requiresAuth: true } },

  { path: '/crear/tarifa/tda', component: NuevaTarifaTDA, meta: { requiresAuth: true } },
  { path: '/crear/tarifa/instalacion', component: NuevaTarifaInstalacion, meta: { requiresAuth: true } },
  { path: '/crear/tarifa/comun', component: NuevaTarifaActividadComun, meta: { requiresAuth: true } },
  { path: '/crear/tarifa/grupos', component: NuevaTarifaGrupoReducido, meta: { requiresAuth: true } },
  { path: '/crear/tarifa/fisioterapia', component: NuevaTarifaFisioterapia, meta: { requiresAuth: true } },
  { path: '/crear/abono/deportivo', component: NuevoAbonoDeportivo, meta: { requiresAuth: true } },
  { path: '/crear/abono/verano', component: NuevoAbonoVerano, meta: { requiresAuth: true } },
  { path: '/crear/bono', component: NuevoBono, meta: { requiresAuth: true } },

  /* Editar */
  { path: '/usuarioFinal/:id', component: DetalleUsuarioFinal, props: true, name: 'detalle-usuarioFinal', meta: { requiresAuth: true } },
  { path: '/monitor/:id', component: DetalleMonitor, props: true, name: 'detalle-monitor', meta: { requiresAuth: true } },
  { path: '/administrador/:id', component: DetalleAdministrador, props: true, name: 'detalle-administrador', meta: { requiresAuth: true } },

  { path: '/admin/pabellones/:id', component: EditarPabellon, props: true, name: 'editar-pabellon', meta: { requiresAuth: true } },
  { path: '/admin/instalaciones/:id', component: EditarInstalacion, props: true, name: 'editar-instalacion', meta: { requiresAuth: true } },
  { path: '/admin/actividades/:id', component: EditarActividad, props: true, name: 'editar-actividad', meta: { requiresAuth: true } },
  { path: '/admin/actividades/:idAct/sesiones/:idSesion', component: EditarSesion, props: true, name: 'editar-sesion', meta: { requiresAuth: true } },
  { path: '/admin/foros/:idForo/canales/:idCanal', component: EditarCanal, props: true, name: 'editar-canal', meta: { requiresAuth: true } },

  { path: '/editar/tarifa/tda/:id', component: EditarTarifaTDA, props: true, name: 'editar-tarifa-tda', meta: { requiresAuth: true } },
  { path: '/editar/tarifa/instalacion/:id', component: EditarTarifaInstalacion, props: true, name: 'editar-tarifa-instalacion', meta: { requiresAuth: true } },
  { path: '/editar/tarifa/comun/:id', component: EditarTarifaActividadComun, props: true, name: 'editar-tarifa-comun', meta: { requiresAuth: true } },
  { path: '/editar/tarifa/grupos/:id', component: EditarTarifaGrupoReducido, props: true, name: 'editar-tarifa-grupos', meta: { requiresAuth: true } },
  { path: '/editar/tarifa/fisioterapia/:id', component: EditarTarifaFisioterapia, props: true, name: 'editar-tarifa-fisioterapia', meta: { requiresAuth: true } },
  { path: '/editar/abono/deportivo', component: EditarAbonoDeportivo, props: true, name: 'editar-abono-deportivo', meta: { requiresAuth: true } },
  { path: '/editar/abono/verano', component: EditarAbonoVerano, props: true, name: 'editar-abono-verano', meta: { requiresAuth: true } },
  { path: '/editar/bono', component: EditarBono, props: true, name: 'editar-bono', meta: { requiresAuth: true } },
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
