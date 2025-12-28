from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.views.generic import RedirectView

router = routers.DefaultRouter()

# En el router vamos agnadiendo los endpoints a los viewsets
router.register(r'abonosDeportivos', views.AbonoDeportivoViewSet)
router.register(r'abonosVerano', views.AbonoVeranoViewSet)

router.register(r'actividades', views.ActividadViewSet)
router.register(r'asistencias', views.AsistenciaViewSet)

router.register(r'agendas', views.AgendaViewSet)

router.register(r'bonos', views.BonoViewSet)

router.register(r'configuraciones', views.ConfiguracionViewSet)

router.register(r'deportes', views.DeporteViewSet)

router.register(r'descuentos', views.DescuentoViewSet)

router.register(r'favoritos', views.FavoritoViewSet)

router.register(r'foros', views.ForoViewSet)
router.register(r'canales', views.CanalViewSet)
router.register(r'usuariosCanal', views.UsuarioCanalViewSet)

router.register(r'horarios', views.HorarioViewSet)

router.register(r'instalaciones', views.InstalacionViewSet)
router.register(r'pabellones', views.PabellonViewSet)

router.register(r'listasEspera', views.ListaEsperaViewSet)
router.register(r'entradasListaEspera', views.EntradaListaEsperaViewSet)

router.register(r'notificaciones', views.NotificacionViewSet)

router.register(r'pagos', views.PagoViewSet)

router.register(r'reservasActividad', views.ReservaActividadViewSet)
router.register(r'alquileres', views.AlquilerViewSet)

router.register(r'tarifasTDA', views.TarifaTDAViewSet)
router.register(r'tarifasActividad', views.TarifaActividadViewSet)
router.register(r'tarifasInstalacion', views.TarifaInstalacionViewSet)

router.register(r'tdas', views.TDAViewSet)

router.register(r'usuariosFinales', views.UsuarioFinalViewSet)
router.register(r'monitores', views.MonitorViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("me/", views.meAPIView.as_view(), name="me"),
    path("buscar/", views.BuscarView.as_view(), name="busqueda"),
]