import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

/* Genericos */
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import RecuperarPassword from '@/components/RecuperarPassword.vue'
import ResetPassword from '@/components/ResetPassword.vue'
import ListaDeActividades from '@/components/ListaDeActividades.vue'
import Perfil from '@/components/Perfil.vue'
import Foro from '@/components/Foro.vue'
import Notificaciones from '@/components/Notificaciones.vue'
import Contacto from '@/components/Contacto.vue'
import FAQ from '@/components/FAQ.vue'
import Feedback from '@/components/Feedback.vue'

/*********** Usuario final ***********/
import HomeUsuarioFinal from '@/components/usuarioFinal/HomeUsuarioFinal.vue'
import Buscar from '@/components/usuarioFinal/Buscar.vue'
import Registro from '@/components/usuarioFinal/Registro.vue'
import VerAbonosBonos from '@/components/usuarioFinal/VerAbonosBonos.vue'

// Detalles
import DetallePabellon from '@/components/usuarioFinal/detalles/DetallePabellon.vue'
import DetalleInstalacion from '@/components/usuarioFinal/detalles/DetalleInstalacion.vue'
import DetalleActividad from '@/components/usuarioFinal/detalles/DetalleActividad.vue'
import DetalleSesion from '@/components/usuarioFinal/detalles/DetalleSesion.vue'

// Perfil
import TarjetaDeportivaAnual from '@/components/usuarioFinal/perfil/TarjetaDeportivaAnual.vue'
import ModificarDatosPersonales from '@/components/usuarioFinal/perfil/ModificarDatosPersonales.vue'
import EstadisticasUsuarios from '@/components/usuarioFinal/perfil/EstadisticasUsuarios.vue'

// Compras
import ComprarAbonosBonos from '@/components/usuarioFinal/compras/ComprarAbonosBonos.vue'
import ReservaActividad from '@/components/usuarioFinal/compras/ReservaActividad.vue'
import Alquiler from '@/components/usuarioFinal/compras/Alquiler.vue'
import ReservasRealizadas from '@/components/usuarioFinal/compras/ReservasRealizadas.vue'
import Pago from '@/components/usuarioFinal/compras/Pago.vue'
import ConfigurarAbono from '@/components/usuarioFinal/compras/ConfigurarAbono.vue'


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
import NuevaNotificacion from '@/components/administrador/NuevaNotificacion.vue'

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
import NuevoDescuento from '@/components/administrador/nuevos/NuevoDescuento.vue'

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
import EditarDescuento from '@/components/administrador/editar/EditarDescuento.vue'


const routes = [
  /******************* REDIRECCIÓN *******************/
  { path: '/', redirect: '/home' },

  /******************* GENÉRICAS *******************/
  { path: '/home', component: Home, meta: { public: true } },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/recuperar-password', component: RecuperarPassword, meta: { public: true } },
  { path: '/reset-password/:token', name: ResetPassword },
  { path: '/buscar', component: Buscar, meta: { public: true } },
  { path: '/actividades', component: ListaDeActividades, meta: { public: true } },
  { path: '/foro', component: Foro, name: 'foro', meta: { requiresAuth: true } },
  { path: '/contacto', component: Contacto, meta: { public: true } },
  { path: '/faq', component: FAQ, meta: { public: true } },
  { path: '/feedback', component: Feedback, meta: { public: true } },


  /******************* USUARIO FINAL *******************/
  {
    path: '/home-usuario',
    component: HomeUsuarioFinal,
    meta: { requiresAuth: true, allowedRoles: ['usuario_final'] }
  },
  { path: '/notificaciones', component: Notificaciones, name: 'notificaciones', meta: { requiresAuth: true, } },
  { path: '/registrarse', component: Registro, meta: { public: true } },
  { path: '/ver-abonos', component: VerAbonosBonos, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },

  /* Perfil */
  { path: '/perfil', component: Perfil, meta: { requiresAuth: true } },
  { path: '/ver-tda', component: TarjetaDeportivaAnual, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },
  { path: '/modificar-datos', component: ModificarDatosPersonales, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },
  { path: '/estadisticas/usuarioFinal', component: EstadisticasUsuarios, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },

  /* Comprar */
  { path: '/comprar-abonos', component: ComprarAbonosBonos, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },
  { path: '/abonos/:id/:tipo/confirmar', component: ConfigurarAbono, name: 'configurar-abono', props: true, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },
  { path: '/reservas-realizadas', component: ReservasRealizadas, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },

  { path: '/actividad/:id/reservar', component: ReservaActividad, name: 'reservar-actividad', props: true, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },
  { path: '/instalacion/:id/reservar', component: Alquiler, name: 'reservar-instalacion', props: true, meta: { requiresAuth: true, allowedRoles: ['usuario_final'] } },

  { path: '/pago/:tipo/:id', component: Pago, props: true, name: 'pasarela-pago', meta: { requiresAuth: true, allowedRoles: ['usuario_final'] }},
  { path: '/pago/finalizado/:id', component: Pago, props: true, name: 'pago-finalizado', meta: { requiresAuth: true, allowedRoles: ['usuario_final'] }},

  /* Detalle */
  { path: '/pabellones/:id', component: DetallePabellon, name: 'detalle-pabellon', props: true, meta: { public: true } },
  { path: '/instalaciones/:id', component: DetalleInstalacion, name: 'detalle-instalacion', props: true, meta: { public: true } },
  { path: '/actividades/:id', component: DetalleActividad, name: 'detalle-actividad', props: true, meta: { public: true } },
  { path: '/actividades/:idAct/sesiones/:idSesion', component: DetalleSesion, name: 'detalle-sesion', props: true, meta: { public: true } },


  /******************* MONITOR *******************/
  { path: '/home-monitor', component: HomeMonitor, meta: { requiresAuth: true, allowedRoles: ['monitor'] } },


  /******************* ADMINISTRADOR *******************/
  { path: '/home-administrador', component: HomeAdministrador, meta: { requiresAuth: true, allowedRoles: ['administrador'] } },

  { path: '/gestion/usuarios', component: GestionarUsuarios, name: 'gestion-usuarios', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },
  { path: '/gestion/espacios', component: GestionarEspacios, name: 'gestion-espacios', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/gestion/actividades', component: GestionarActividades, name: 'gestion-actividades', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/gestion/tarifas', component: GestionarTarifas, name: 'gestion-tarifas', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/configuracion', component: Configuracion, name: 'configuracion', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ'] } },
  { path: '/estadisticas/administrador', component: EstadisticasAdministrador, name: 'estadisticas-administrador', meta: { requiresAuth: true, allowedRoles: ['administrador'] } },
  { path: '/notificaciones/nueva', component: NuevaNotificacion, name: 'nueva-notificacion', meta: { requiresAuth: true, allowedRoles: ['administrador'] } },

  /* Nuevo */
  { path: '/registrar/usuario', component: NuevoUsuarioFinal, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },
  { path: '/registrar/monitor', component: NuevoMonitor, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },
  { path: '/registrar/administrador', component: NuevoAdministrador, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },

  { path: '/crear/pabellon', component: NuevoPabellon, name: 'crear-pabellon', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/crear/instalacion', component: NuevaInstalacion, name: 'crear-instalacion', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/crear/actividad', component: NuevaActividad, name: 'crear-actividad', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/crear/sesion/:id', component: NuevaSesion, props: true, name: 'crear-sesion', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/crear/canal/:id', component: NuevoCanal, props: true, name: 'crear-canal', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },

  { path: '/crear/tarifa/tda', component: NuevaTarifaTDA, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/tarifa/instalacion', component: NuevaTarifaInstalacion, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/tarifa/comun', component: NuevaTarifaActividadComun, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/tarifa/grupos', component: NuevaTarifaGrupoReducido, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/tarifa/fisioterapia', component: NuevaTarifaFisioterapia, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/abono/deportivo', component: NuevoAbonoDeportivo, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/abono/verano', component: NuevoAbonoVerano, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/bono', component: NuevoBono, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/crear/descuento', component: NuevoDescuento, meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },

  /* Editar */
  { path: '/usuarioFinal/:id', component: DetalleUsuarioFinal, props: true, name: 'detalle-usuarioFinal', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },
  { path: '/monitor/:id', component: DetalleMonitor, props: true, name: 'detalle-monitor', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },
  { path: '/administrador/:id', component: DetalleAdministrador, props: true, name: 'detalle-administrador', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'USUARIOS'] } },

  { path: '/admin/pabellones/:id', component: EditarPabellon, props: true, name: 'editar-pabellon', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/admin/instalaciones/:id', component: EditarInstalacion, props: true, name: 'editar-instalacion', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/admin/actividades/:id', component: EditarActividad, props: true, name: 'editar-actividad', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/admin/actividades/:idAct/sesiones/:idSesion', component: EditarSesion, props: true, name: 'editar-sesion', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },
  { path: '/admin/foros/:idForo/canales/:idCanal', component: EditarCanal, props: true, name: 'editar-canal', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'ESPACIOS'] } },

  { path: '/editar/tarifa/tda/:id', component: EditarTarifaTDA, props: true, name: 'editar-tarifa-tda', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/tarifa/instalacion/:id', component: EditarTarifaInstalacion, props: true, name: 'editar-tarifa-instalacion', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/tarifa/comun/:id', component: EditarTarifaActividadComun, props: true, name: 'editar-tarifa-comun', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/tarifa/grupos/:id', component: EditarTarifaGrupoReducido, props: true, name: 'editar-tarifa-grupos', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/tarifa/fisioterapia/:id', component: EditarTarifaFisioterapia, props: true, name: 'editar-tarifa-fisioterapia', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/abono/deportivo/:id', component: EditarAbonoDeportivo, props: true, name: 'editar-abono-deportivo', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/abono/verano/:id', component: EditarAbonoVerano, props: true, name: 'editar-abono-verano', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/bono/:id', component: EditarBono, props: true, name: 'editar-bono', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
  { path: '/editar/descuento/:id', component: EditarDescuento, props: true, name: 'editar-descuento', meta: { requiresAuth: true, allowedAdminRoles: ['RAIZ', 'TARIFAS'] } },
]


/* Cada vez que se accede a una página se redirige el scrollbar arriba */
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  }
})

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (!auth.user) {
    await auth.fetchUser();
  }

  if (to.path === '/home') {
    if (auth.isUsuarioFinal) return '/home-usuario';
    if (auth.isMonitor) return '/home-monitor';
    if (auth.isAdmin) return '/home-administrador';
  }

  // Rutas públicas
  if (to.meta.public) return true;

  // Requiere login
  if (!auth.isAuthenticated) return '/login';

  // Roles
  if (to.meta.allowedRoles) {
    const allowed = to.meta.allowedRoles;

    if (
      (allowed.includes('usuario_final') && auth.isUsuarioFinal) ||
      (allowed.includes('monitor') && auth.isMonitor) ||
      (allowed.includes('administrador') && auth.isAdmin)
    ) {
      return true;
    }

    return '/login';
  }

  // Roles de admin
  if (to.meta.allowedAdminRoles) {
    const allowedAdmin = to.meta.allowedAdminRoles;

    if (!auth.isAdmin) return '/login';

    if (allowedAdmin.includes(auth.adminRole)) {
      return true;
    }

    return '/login';
  }

  return true;
});

export default router
