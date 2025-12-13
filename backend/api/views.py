from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    BasePermission,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model

from serializers import (
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

class AbonoDeportivoViewSet(viewsets.ModelViewSet):
    queryset = AbonoDeportivo.objects.all()
    serializer_class = AbonoDeportivoSerializer


# ----------------
# Abonos
# ----------------

class AbonoDeportivoViewSet(viewsets.ModelViewSet):
    queryset = AbonoDeportivo.objects.all()
    serializer_class = AbonoDeportivoSerializer
    permission_classes = [IsAuthenticated]


class AbonoVeranoViewSet(viewsets.ModelViewSet):
    queryset = AbonoVerano.objects.all()
    serializer_class = AbonoVeranoSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Actividades
# ----------------

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Agenda
# ----------------

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Bonos
# ----------------

class BonoViewSet(viewsets.ModelViewSet):
    queryset = Bono.objects.all()
    serializer_class = BonoSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Configuración
# ----------------

class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Deportes
# ----------------

class DeporteViewSet(viewsets.ModelViewSet):
    queryset = Deporte.objects.all()
    serializer_class = DeporteSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Descuentos
# ----------------

class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Favoritos
# ----------------

class FavoritoViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]


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
    queryset = UsuarioCanal.objects.all()
    serializer_class = UsuarioCanalSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Horario
# ----------------

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Instalaciones
# ----------------

class InstalacionViewSet(viewsets.ModelViewSet):
    queryset = Instalacion.objects.all()
    serializer_class = InstalacionSerializer
    permission_classes = [IsAuthenticated]


class PabellonViewSet(viewsets.ModelViewSet):
    queryset = Pabellon.objects.all()
    serializer_class = PabellonSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Lista de espera
# ----------------

class ListaEsperaViewSet(viewsets.ModelViewSet):
    queryset = ListaEspera.objects.all()
    serializer_class = ListaEsperaSerializer
    permission_classes = [IsAuthenticated]


class EntradaListaEsperaViewSet(viewsets.ModelViewSet):
    queryset = EntradaListaEspera.objects.all()
    serializer_class = EntradaListaEsperaSerializer
    permission_classes = [IsAuthenticated]


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
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]


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
    queryset = ReservaActividad.objects.all()
    serializer_class = ReservaActividadSerializer
    permission_classes = [IsAuthenticated]


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Tarifas
# ----------------

class TarifaTDASerializerViewSet(viewsets.ModelViewSet):
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
    queryset = TDA.objects.all()
    serializer_class = TDASerializer
    permission_classes = [IsAuthenticated]


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



class SearchTournamentsAPIView(APIView):
    permission_classes = []

    def post(self, request):
        search_string = request.data.get("search_string", "")
        tournaments = Tournament.objects.filter(name__icontains=search_string)\
            .order_by("-id")

        result = []
        for t in tournaments:
            result.append(
                {
                    "id": t.id,
                    "name": t.name,
                    "tournament_type": t.tournament_type,
                    "board_type": t.board_type,
                    "tournament_speed": t.tournament_speed,
                    "start_date": t.start_date,
                }
            )

        return Response(result, status=status.HTTP_200_OK)