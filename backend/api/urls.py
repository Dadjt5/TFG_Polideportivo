from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.views.generic import RedirectView

router = routers.DefaultRouter()

# En el router vamos agnadiendo los endpoints a los viewsets
router.register(r'abonosDeportivos', views.AbonoDeportivoViewSet, basename="abono-deportivo")
router.register(r'abonosVerano', views.AbonoVeranoViewSet, basename="abono-verano")

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

router.register(r'horarios', views.HorarioViewSet, basename="horario")

router.register(r'instalaciones', views.InstalacionViewSet, basename="instalacion")
router.register(r'pabellones', views.PabellonViewSet, basename="pabellon")

router.register(r'listasEspera', views.ListaEsperaViewSet, basename="lista-espera")
router.register(r'entradasListaEspera', views.EntradaListaEsperaViewSet, basename="entrada-lista")

router.register(r'notificaciones', views.NotificacionViewSet, basename="notificacion")

router.register(r'pagos', views.PagoViewSet, basename="pago")

router.register(r'reservasActividad', views.ReservaActividadViewSet, basename="reserva-actividad")
router.register(r'alquileres', views.AlquilerViewSet, basename="alquiler-instalacion")

router.register(r'tarifasTDA', views.TarifaTDAViewSet, basename="tarifa-tda")
router.register(r'tarifasActividad', views.TarifaActividadViewSet, basename="tarifa-actividad")
router.register(r'tarifasInstalacion', views.TarifaInstalacionViewSet, basename="tarifa-instalacion")

router.register(r'tdas', views.TDAViewSet, basename="tda")

router.register(r'usuariosFinales', views.UsuarioFinalViewSet, basename="usuario-final")
router.register(r'monitores', views.MonitorViewSet, basename="monitor")
router.register(r'users', views.UserViewSet, basename="user")


urlpatterns = [
    path('', include(router.urls)),
    path("me/", views.meAPIView.as_view(), name="me"),
    path("estadisticas/", views.EstadisticasView.as_view(), name="estadisticas"),
    path("buscar/", views.BuscarView.as_view(), name="busqueda"),
    path("registrarse/", views.RegistroView.as_view(), name="registro"),
    path("notificaciones/guardar/", views.GuardarNotificacionView.as_view(), name="modificar-notificacion"),
    path("tda/validar/", views.ValidarTDAView.as_view(), name="validar-tda"),
    path("marcar/favoritas/", views.AlterarFavoritosView.as_view(), name="marcar-favoritas"),
    path("obtener/favoritas/", views.ObtenerActividadesInstalaciones.as_view(), name="favoritas"),
]