from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from django.contrib.auth import get_user_model

from .serializers import (
    AbonoDeportivoSerializer, AbonoVeranoSerializer, BonoSerializer,
    ActividadSerializer, AsistenciaSerializer, AgendaSerializer,
    ConfiguracionSerializer, DeporteSerializer, DescuentoSerializer,
    FavoritoSerializer, ForoSerializer, CanalSerializer, UsuarioCanalSerializer,
    HorarioSerializer, InstalacionSerializer, PabellonSerializer, ListaEsperaSerializer,
    EntradaListaEsperaSerializer, MonitorSerializer, NotificacionSerializer,
    PagoSerializer, ReservaActividadSerializer, AlquilerSerializer,
    TarifaTDASerializer, TarifaActividadSerializer, TarifaInstalacionSerializer,
    TDASerializer, UsuarioFinalSerializer, UserSerializer
)

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler
)


User = get_user_model()


# --- HAY QUE ESTABLECER LOS PERMISOS PARA QUE SEAN PARA ADMIN PARA CADA TIPO DE ADMIN Y A LO MEJOR HACER UN MODELO ADMIN CON CAMPO ROL

# ----------------
# Abonos
# ----------------

class AbonoDeportivoViewSet(viewsets.ModelViewSet):
    serializer_class = AbonoDeportivoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)
    
    def get_queryset(self):
        return AbonoDeportivo.objects.filter(usuarioFinal=self.request.user)


class AbonoVeranoViewSet(viewsets.ModelViewSet):
    serializer_class = AbonoVeranoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)
        
    def get_queryset(self):
        return AbonoVerano.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Actividades
# ----------------

class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_monitor:
            # Filtrar solo las actividades que dirige
            return Actividad.objects.filter(monitor=user)
        else:
            # Usuario final ve todas las actividades
            return Actividad.objects.all()


class AsistenciaViewSet(viewsets.ModelViewSet):
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return Asistencia.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Agenda
# ----------------

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [AllowAny]


# ----------------
# Bonos
# ----------------

class BonoViewSet(viewsets.ModelViewSet):
    serializer_class = BonoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return Bono.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Configuración
# ----------------

class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer
    permission_classes = [IsAuthenticated]  #Debemos añadir un permiso especial para admin raiz


# ----------------
# Deportes
# ----------------

class DeporteViewSet(viewsets.ModelViewSet):
    queryset = Deporte.objects.all()
    serializer_class = DeporteSerializer
    permission_classes = [AllowAny]


# ----------------
# Descuentos
# ----------------

class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer
    permission_classes = [AllowAny]


# ----------------
# Favoritos
# ----------------

class FavoritoViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return Favorito.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Foro
# ----------------

class ForoViewSet(viewsets.ModelViewSet):
    queryset = Foro.objects.all()
    serializer_class = ForoSerializer
    permission_classes = [IsAuthenticated]


class CanalViewSet(viewsets.ModelViewSet):
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer
    permission_classes = [IsAuthenticated]


class UsuarioCanalViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioCanalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return UsuarioCanal.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Horario
# ----------------

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [AllowAny]


# ----------------
# Instalaciones
# ----------------

class InstalacionViewSet(viewsets.ModelViewSet):
    queryset = Instalacion.objects.all()
    serializer_class = InstalacionSerializer
    permission_classes = [AllowAny]


class PabellonViewSet(viewsets.ModelViewSet):
    queryset = Pabellon.objects.all()
    serializer_class = PabellonSerializer
    permission_classes = [AllowAny]


# ----------------
# Lista de espera
# ----------------

class ListaEsperaViewSet(viewsets.ModelViewSet):
    queryset = ListaEspera.objects.all()
    serializer_class = ListaEsperaSerializer
    permission_classes = [AllowAny]


class EntradaListaEsperaViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaListaEsperaSerializer
    permission_classes = [IsAuthenticated]
     
    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return EntradaListaEspera.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Monitores
# ----------------

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Notificaciones
# ----------------

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)


# ----------------
# Pagos
# ----------------

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Reservas
# ----------------

class ReservaActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaActividadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return ReservaActividad.objects.filter(usuarioFinal=self.request.user)


class AlquilerViewSet(viewsets.ModelViewSet):
    serializer_class = AlquilerSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return Alquiler.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Tarifas
# ----------------

class TarifaTDAViewSet(viewsets.ModelViewSet):
    queryset = TarifaTDA.objects.all()
    serializer_class = TarifaTDASerializer
    permission_classes = [IsAuthenticated]


class TarifaActividadViewSet(viewsets.ModelViewSet):
    queryset = TarifaActividad.objects.all()
    serializer_class = TarifaActividadSerializer
    permission_classes = [IsAuthenticated]


class TarifaInstalacionViewSet(viewsets.ModelViewSet):
    queryset = TarifaInstalacion.objects.all()
    serializer_class = TarifaInstalacionSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# TDA
# ----------------

class TDAViewSet(viewsets.ModelViewSet):
    serializer_class = TDASerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuarioFinal=self.request.user)

    def get_queryset(self):
        return TDA.objects.filter(usuarioFinal=self.request.user)


# ----------------
# Usuarios finales
# ----------------

class UsuarioFinalViewSet(viewsets.ModelViewSet):
    queryset = UsuarioFinal.objects.all()
    serializer_class = UsuarioFinalSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# User (Django auth)
# ----------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
