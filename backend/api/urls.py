from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.views.generic import RedirectView

router = routers.DefaultRouter()

# En el router vamos agnadiendo los endpoints a los viewsets
router.register(r'feedback', views.FeedbackViewSet, basename="feedback")

router.register(r'abonosDeportivos', views.AbonoDeportivoViewSet, basename="abono-deportivo")
router.register(r'abonosVerano', views.AbonoVeranoViewSet, basename="abono-verano")

router.register(r'compraAbono', views.CompraAbonoViewSet, basename="compra-abono")
router.register(r'compraBono', views.CompraBonoViewSet, basename="compra-bono")

router.register(r'actividades', views.ActividadViewSet, basename="actividad")
router.register(r'sesiones', views.SesionViewSet, basename="sesion")
router.register(r'asistencias', views.AsistenciaViewSet, basename="asistencia")

router.register(r'canales', views.CanalViewSet, basename="canal")

router.register(r'agendas', views.AgendaViewSet, basename="agenda")

router.register(r'bonos', views.BonoViewSet, basename="bono")

router.register(r'deportes', views.DeporteViewSet, basename="deporte")

router.register(r'descuentos', views.DescuentoViewSet, basename="descuento")

router.register(r'favoritos', views.FavoritoViewSet, basename="favorito")

router.register(r'instalaciones', views.InstalacionViewSet, basename="instalacion")
router.register(r'pabellones', views.PabellonViewSet, basename="pabellon")
router.register(r'calles', views.CalleViewSet, basename="calle")

router.register(r'listasEspera', views.ListaEsperaViewSet, basename="lista-espera")
router.register(r'entradasListaEspera', views.EntradaListaEsperaViewSet, basename="entrada-lista")

router.register(r'notificaciones', views.NotificacionViewSet, basename="notificacion")

router.register(r'pagos', views.PagoViewSet, basename="pago")

router.register(r'reservasActividad', views.ReservaActividadViewSet, basename="reservas-actividad")
router.register(r'alquileres', views.AlquilerViewSet, basename="alquiler-instalacion")

router.register(r'reservasActividadSimple', views.ReservaActividadSimpleViewSet, basename="reservas-actividad-simple")
router.register(r'alquileresSimple', views.AlquilerSimpleViewSet, basename="alquiler-instalacion-simple")

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

router.register(r'pabellonesSimple', views.PabellonSimpleViewSet, basename="pabellones-simple")
router.register(r'instalacionesSimple', views.InstalacionSimpleViewSet, basename="instalaciones-simple")
router.register(r'actividadesSimple', views.ActividadSimpleViewSet, basename="actividades-simple")
router.register(r'monitoresSimple', views.MonitorSimpleViewSet, basename="monitores-simple")

urlpatterns = [
    path("me/", views.meAPIView.as_view(), name="me"),
    path("estadisticas/", views.EstadisticasView.as_view(), name="estadisticas"),
    path("estadisticas/administrador/", views.ObtenerEstadisticasAdministradorView.as_view(), name="estadisticas-admin"),
    path("estadisticas/usuarioFinal/", views.ObtenerEstadisticasUsuarioFinalView.as_view(), name="estadisticas-usuarioFinal"),
    path("tipos/", views.TiposViews.as_view(), name="tipos"),
    path("buscar/", views.BuscarView.as_view(), name="busqueda"),
    path("registrarse/", views.RegistroView.as_view(), name="registro"),
    path("registrar/monitor/", views.RegistroMonitorView.as_view(), name="registrar-monitor"),
    path("registrar/administrador/", views.RegistroAdministradorView.as_view(), name="registrar-administrador"),
    path("notificaciones/nueva/", views.NuevaNotificacionView.as_view(), name="crear-notificacion"),
    path("notificaciones/guardar/", views.GuardarNotificacionView.as_view(), name="modificar-leer-notificacion"),
    path("notificaciones/<int:notificacion_id>/responder/", views.AccionNotificacionView.as_view(), name="reaccionar-notificacion"),
    path("tda/validar/", views.ValidarTDAView.as_view(), name="validar-tda"),
    path("marcar/favoritas/", views.AlterarFavoritosView.as_view(), name="marcar-favoritas"),
    path("obtener/favoritas/", views.ObtenerActividadesInstalaciones.as_view(), name="favoritas"),
    path("reservas/", views.ReservasView.as_view(), name="Reservas-favoritas"),
    path("abonos/", views.ObtenerAbonosView.as_view(), name="Obtener-abonos"),
    path("abonos/<int:abono_id>/comprar/", views.ComprarAbonoView.as_view(), name="comprar-abono"),
    path("bonos/<int:bono_id>/comprar/", views.ComprarBonoView.as_view(), name="comprar-bono"),
    path("tda/comprar/", views.ComprarTDAView.as_view(), name="comprar-TDA"),
    path("foro/", views.ForoView.as_view(), name="Foro"),
    path("foros/<int:foro_id>/canal/", views.NuevoCanalView.as_view(), name="crear-canal"),
    path("canales/<int:canal_id>/mensajes/", views.MensajesCanalView.as_view(), name="mensajes-canal"),
    path("canales/<int:canal_id>/admin/", views.CanalAdministradorView.as_view(), name="detalles-canal-admin"),
    path("canales/<int:canal_id>/modificar/<int:usuario_id>/", views.GestionarUsuarioCanalView.as_view(), name="gestionar-usuario-canal"),
    path("monitores/<int:monitor_id>/sesiones/", views.SesionesMonitorView.as_view(), name="sesiones-monitor"),
    path("actividades/crear/", views.NuevaActividadView.as_view(), name="nueva-actividad"),
    path("actividades/<int:actividad_id>/editar/", views.EditarActividadView.as_view(), name="editar-actividad"),
    path("actividades/<int:actividad_id>/sesiones/<int:sesion_id>/", views.DetalleSesionView.as_view(), name="detalle-sesion"),
    path("actividades/<int:actividad_id>/sesion/", views.NuevaSesionView.as_view(), name="crear-sesion"),
    path("actividades/<int:actividad_id>/sesiones/<int:sesion_id>/asistencia/", views.GuardarAsistenciaView.as_view(), name="guardar-asistencia"),
    path("actividades/<int:actividad_id>/reservar/", views.ReservarActividadView.as_view(), name="reservar-actividad"),
    path("actividades/<int:actividad_id>/esperar/", views.PasarListaEsperaView.as_view(), name="pasar-a-espera"),
    path("instalaciones/crear/", views.NuevaInstalacionView.as_view(), name="nueva-instalacion"),
    path("instalaciones/<int:instalacion_id>/editar/", views.EditarInstalacionView.as_view(), name="editar-instalacion"),
    path("instalaciones/<int:instalacion_id>/alquilar/", views.ReservaInstalacionView.as_view(), name="reservar-instalacion"),
    path("instalaciones/<int:instalacion_id>/comprobar/alquiler/", views.ComprobarAlquileresView.as_view(), name="comprobar-alquileres"),
    path("tarifas/actividades/<int:actividad_id>/", views.TarifaActividadView.as_view(), name="tarifa-actividad"),
    path("tarifas/instalaciones/<int:instalacion_id>/", views.TarifaInstalacionView.as_view(), name="tarifa-instalacion"),
    path("instalaciones/<int:instalacion_id>/obtener/alquileres/", views.ReservasPorDiaView.as_view(), name="obtener-alquileres-por-dia"),
    path("usuarios/", views.GestionUsuariosView.as_view(), name="obtener-usuarios"),
    path("espacios/", views.GestionEspaciosView.as_view(), name="obtener-espacios"),
    path("tarifas/", views.GestionTarifasView.as_view(), name="obtener-tarifas"),
    path("configuracion/", views.ObtenerConfiguracionView.as_view(), name="obtener-configuracion"),
    path("pagos/resumen/<str:tipo>/<int:pago_id>/", views.ResumenPagoView.as_view(), name="resumen-pago"),
    path("pagos/<int:pago_id>/comenzar/", views.CrearIntentoPagoView.as_view(), name="intentar-pago"),
    path("pagos/<int:pago_id>/confirmar/", views.ConfirmarPagoView.as_view(), name="confirmar-pago"),
    path("pagos/<int:pago_id>/cancelar/", views.CancelarPagoView.as_view(), name="cancelar-pago"),
    path("reservas/<int:reserva_id>/cancelar/", views.CancelarReservaActividadView.as_view(), name="cancelar-reserva"),
    path("alquileres/<int:alquiler_id>/cancelar/", views.CancelarAlquilerView.as_view(), name="cancelar-alquiler"),
    path("abonos/<int:compra_id>/cancelar/", views.CancelarAbonoView.as_view(), name="cancelar-abono"),
    path("bonos/<int:compra_id>/cancelar/", views.CancelarBonoView.as_view(), name="cancelar-bono"),
    path("stripe/webhook/", views.StripeWebhookView.as_view(), name="webhook-stripe"),
    path("password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    path("instalaciones/<int:instalacion_id>/descargar/horario/", views.DescargarHorarioView.as_view(), name="descargar-horario"),
    path("actividades/<int:actividad_id>/descargar/horario/", views.DescargarHorarioSesionesView.as_view(), name="descargar-horario-sesiones"),
    path('', include(router.urls)),
]