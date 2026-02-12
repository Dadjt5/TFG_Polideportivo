from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.views.generic import RedirectView

router = routers.DefaultRouter()

# En el router vamos agnadiendo los endpoints a los viewsets
router.register(r'abonosDeportivos', views.AbonoDeportivoViewSet, basename="abono-deportivo")
router.register(r'abonosVerano', views.AbonoVeranoViewSet, basename="abono-verano")

router.register(r'compraAbono', views.CompraAbonoViewSet, basename="compra-abono")
router.register(r'compraBono', views.CompraBonoViewSet, basename="compra-bono")

router.register(r'actividades', views.ActividadViewSet, basename="actividad")
router.register(r'asistencias', views.AsistenciaViewSet, basename="asistencia")

router.register(r'agendas', views.AgendaViewSet, basename="agenda")

router.register(r'bonos', views.BonoViewSet, basename="bono")

router.register(r'configuraciones', views.ConfiguracionViewSet, basename="configuracion")

router.register(r'deportes', views.DeporteViewSet, basename="deporte")

router.register(r'descuentos', views.DescuentoViewSet, basename="descuento")

router.register(r'favoritos', views.FavoritoViewSet, basename="favorito")

router.register(r'foros', views.ForoViewSet, basename="foro")
router.register(r'canales', views.CanalViewSet, basename="canal")
router.register(r'usuariosCanal', views.UsuarioCanalViewSet, basename="usuario-canal")
router.register(r'mensaje', views.MensajeViewSet, basename="mensaje-canal")

router.register(r'horarios', views.HorarioViewSet, basename="horario")

router.register(r'instalaciones', views.InstalacionViewSet, basename="instalacion")
router.register(r'pabellones', views.PabellonViewSet, basename="pabellon")

router.register(r'listasEspera', views.ListaEsperaViewSet, basename="lista-espera")
router.register(r'entradasListaEspera', views.EntradaListaEsperaViewSet, basename="entrada-lista")

router.register(r'notificaciones', views.NotificacionViewSet, basename="notificacion")

router.register(r'pagos', views.PagoViewSet, basename="pago")

router.register(r'reservasActividad', views.ReservaActividadViewSet, basename="reservas-actividad")
router.register(r'alquileres', views.AlquilerViewSet, basename="alquiler-instalacion")

router.register(r'tarifasTDA', views.TarifaTDAViewSet, basename="tarifa-tda")
router.register(r'tarifasInstalacion', views.TarifaInstalacionViewSet, basename="tarifa-instalacion")
router.register(r'tarifasActividad', views.TarifaActividadViewSet, basename="tarifa-actividad")
router.register(r'actividadesComunes', views.ActividadComunViewSet, basename="tarifa-actividad-comun")
router.register(r'gruposReducidos', views.GrupoReducidoViewSet, basename="tarifa-grupo-reducido")
router.register(r'fisioterapias', views.FisioterapiaViewSet, basename="tarifa-fisioterapia")

router.register(r'tdas', views.TDAViewSet, basename="tda")

router.register(r'usuariosFinales', views.UsuarioFinalViewSet, basename="usuario-final")
router.register(r'monitores', views.MonitorViewSet, basename="monitor")
router.register(r'administradores', views.AdministradorViewSet, basename="administrador")
router.register(r'users', views.UserViewSet, basename="user")


urlpatterns = [
    path("me/", views.meAPIView.as_view(), name="me"),
    path("estadisticas/", views.EstadisticasView.as_view(), name="estadisticas"),
    path("tipos/", views.TiposViews.as_view(), name="tipos"),
    path("buscar/", views.BuscarView.as_view(), name="busqueda"),
    path("registrarse/", views.RegistroView.as_view(), name="registro"),
    path("registrar/monitor/", views.RegistroMonitorView.as_view(), name="registrar-monitor"),
    path("registrar/administrador/", views.RegistroAdministradorView.as_view(), name="registrar-administrador"),
    path("notificaciones/guardar/", views.GuardarNotificacionView.as_view(), name="modificar-notificacion"),
    path("tda/validar/", views.ValidarTDAView.as_view(), name="validar-tda"),
    path("marcar/favoritas/", views.AlterarFavoritosView.as_view(), name="marcar-favoritas"),
    path("obtener/favoritas/", views.ObtenerActividadesInstalaciones.as_view(), name="favoritas"),
    path("reservas/", views.ReservasView.as_view(), name="Reservas-favoritas"),
    path("foro/", views.ForoView.as_view(), name="Foro"),
    path("canales/<int:canal_id>/mensajes/", views.MensajesCanalView.as_view(), name="mensajes-canal"),
    path("monitores/<int:monitor_id>/sesiones/", views.SesionesMonitorView.as_view(), name="sesiones-monitor"),
    path("actividades/<int:actividad_id>/sesiones/<int:sesion_id>/", views.DetalleSesionView.as_view(), name="detalle-sesion"),
    path("actividades/<int:actividad_id>/sesiones/<int:sesion_id>/asistencia/", views.GuardarAsistenciaView.as_view(), name="guardar-asistencia"),
    path("tarifas/actividades/<int:actividad_id>/", views.TarifaActividadView.as_view(), name="tarifa-actividad"),
    path("tarifas/instalaciones/<int:instalacion_id>/", views.TarifaInstalacionView.as_view(), name="tarifa-instalacion"),
    path("pabellones/simple/", views.PabellonSimpleViewSet.as_view(), name="pabellones-simple"),
    path("instalaciones/simple/", views.InstalacionSimpleViewSet.as_view(), name="instalaciones-simple"),
    path("actividades/simple/", views.ActividadSimpleViewSet.as_view(), name="actividades-simple"),
    path("monitores/simple/", views.MonitorSimpleViewSet.as_view(), name="monitores-simple"),
    path("usuarios/", views.GestionUsuariosView.as_view(), name="obtener-usuarios"),
    path("espacios/", views.GestionEspaciosView.as_view(), name="obtener-espacios"),
    path("tarifas/", views.GestionTarifasView.as_view(), name="obtener-tarifas"),
    path('', include(router.urls)),
]