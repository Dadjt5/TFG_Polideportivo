from rest_framework import viewsets
from rest_framework.views import APIView
import json
from rest_framework.response import Response
import re
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
import resend
import os
from django.db.models import Case, When, IntegerField
from rest_framework import status
import stripe
from django.core.mail import send_mail
from rest_framework.exceptions import PermissionDenied
from django.utils.dateparse import parse_date
from datetime import date
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models.deletion import RestrictedError
from django.conf import settings
from django.db.models import Q
from django.db.models import Sum, Count
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth, ExtractWeekDay
from datetime import timedelta, datetime
import random
from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import threading
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

from .permissions import IsAdministradorRaiz, IsAdministradorEspacios, IsAdministradorTarifas, IsAdministradorUsuarios, IsMonitor, IsUsuarioFinal, IsAdministrador, IsSuperUser

from .serializers import (
    AbonoDeportivoSerializer, AbonoVeranoSerializer, BonoSerializer,
    ActividadSerializer, AsistenciaSerializer, AgendaSerializer,
    ConfiguracionSerializer, DeporteSerializer, DescuentoSerializer,
    FavoritoSerializer, ForoSerializer, CanalUsuarioFinalSerializer,
    InstalacionSerializer, PabellonSerializer, ListaEsperaSerializer,
    EntradaListaEsperaSerializer, MonitorSerializer, NotificacionSerializer,
    PagoSerializer, ReservaActividadSerializer, AlquilerSerializer,
    TarifaTDASerializer, TarifaActividadSerializer, TarifaInstalacionSerializer,
    TDASerializer, UsuarioFinalSerializer, UserSerializer, AdministradorSerializer,
    CompraBonoSerializer, CompraAbonoSerializer, MensajeSerializer, SesionSerializer,
    MapaReservasSerializer, AdministradorSimpleSerializer, MonitorSimpleSerializer,
    UsuarioFinalSimpleSerializer, PabellonSimpleSerializer, ActividadSimpleSerializer,
    InstalacionSimpleSerializer, ActividadComunSerializer, GrupoReducidoSerializer,
    FisioterapiaSerializer, TarifaInstalacionSimpleSerializer, TarifaTDASimpleSerializer,
    ActividadComunSimpleSerializer, GrupoReducidoSimpleSerializer, FisioterapiaSimpleSerializer,
    CanalSerializer, CanalAdministradorSerializer, ReservaActividadSimpleSerializer,
    AlquilerSimpleSerializer, FeedbackSerializer, CalleSerializer, InstalacionSinAgendaSerializer
)

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, User, CompraBono, CompraAbono,
    Mensaje, Sesion, MapaReservas, TipoActividad, TipoInstalacion, FormaReserva,
    Terreno, Estado, Dia, ActividadComun, GrupoReducido, Fisioterapia, EstadoPago,
    EstadoReserva, Periodo, Feedback, Calle, RolAdministrador, TipoReserva, TipoPago,
    CodigoResetPassword
)


# ----------------
# Feedback
# ----------------

class FeedbackViewSet(viewsets.ModelViewSet):

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsSuperUser()]
        elif self.action == "create":
            return []
        else:
            return [IsSuperUser()]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feedback.objects.all().order_by("-fecha")

        return Feedback.objects.none()


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


class CompraAbonoViewSet(viewsets.ModelViewSet):
    serializer_class = CompraAbonoSerializer
    permission_classes = [IsUsuarioFinal]

    def get_queryset(self):
        return CompraAbono.objects.filter(usuarioFinal__user=self.request.user, estado=EstadoReserva.CONFIRMADA)


# ----------------
# Actividades
# ----------------

class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and getattr(user, "is_monitor", False):
            return Actividad.objects.filter(monitor__user=user)

        return Actividad.objects.all()

    def destroy(self, request, *args, **kwargs):
        actividad = self.get_object()

        Notificacion.notificarEliminacionActividad(actividad)

        reservas = ReservaActividad.objects.filter(
            actividad=actividad,
            estado=EstadoReserva.CONFIRMADA
        )

        for reserva in reservas:
            reserva_ct = ContentType.objects.get_for_model(ReservaActividad)
            pago = Pago.objects.get(content_type=reserva_ct, object_id=reserva.id)

            pago.cancelarPago()

        self.perform_destroy(actividad)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActividadSimpleViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSimpleSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class AsistenciaViewSet(viewsets.ModelViewSet):
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        user = self.request.user
        if user.is_usuario_final:
            return Asistencia.objects.filter(usuarioFinal__user=user)
        elif user.is_monitor:
            return Asistencia.objects.filter(sesion__monitor__user=user)
        elif user.is_administrador:
            return Asistencia.objects.all()
        return []

# ----------------
# Agenda
# ----------------

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        sesion = self.get_object()

        dia = sesion.dia
        horaInicio = sesion.horaInicio
        horaFin = sesion.horaFin
        calle = sesion.calle

        agenda = Agenda.objects.filter(dia__iexact=dia).first()

        if agenda:
            agenda.mapa_reservas.filter(
                calle=calle,
                horaInicio__gte=horaInicio,
                horaInicio__lt=horaFin,
                estado=TipoReserva.ACTIVIDAD
            ).update(estado=TipoReserva.LIBRE)

        self.perform_destroy(sesion)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MapaReservasViewSet(viewsets.ModelViewSet):
    queryset = MapaReservas.objects.all()
    serializer_class = MapaReservasSerializer
    permission_classes = [AllowAny]


# ----------------
# Canales
# ----------------

class CanalViewSet(viewsets.ModelViewSet):
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer
    permission_classes = [IsAuthenticated]
    

# ----------------
# Sesiones
# ----------------

class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Bonos
# ----------------
    
class BonoViewSet(viewsets.ModelViewSet):
    queryset = Bono.objects.all()
    serializer_class = BonoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class CompraBonoViewSet(viewsets.ModelViewSet):
    serializer_class = CompraBonoSerializer
    permission_classes = [IsUsuarioFinal]
    
    def get_queryset(self):
        return CompraBono.objects.filter(usuarioFinal__user=self.request.user, estado=EstadoReserva.CONFIRMADA)

    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


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
    permission_classes = [AllowAny]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response(
                {"respuesta": "Deporte eliminado correctamente"},
                status=status.HTTP_204_NO_CONTENT
            )

        except RestrictedError:
            return Response(
                {"respuesta": "No se puede eliminar el deporte porque está siendo utilizado en una o más actividades"},
                status=status.HTTP_400_BAD_REQUEST
            )


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
# Instalaciones
# ----------------

class CalleViewSet(viewsets.ModelViewSet):
    queryset = Calle.objects.all()
    serializer_class = CalleSerializer
    permission_classes = [AllowAny]


class InstalacionViewSet(viewsets.ModelViewSet):
    queryset = Instalacion.objects.all()
    serializer_class = InstalacionSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def destroy(self, request, *args, **kwargs):
        instalacion = self.get_object()

        Notificacion.notificarEliminacionInstalacion(instalacion)

        reservas = Alquiler.objects.filter(
            instalacion=instalacion,
            estado=EstadoReserva.CONFIRMADA
        )

        for reserva in reservas:
            reserva_ct = ContentType.objects.get_for_model(Alquiler)
            pago = Pago.objects.get(content_type=reserva_ct, object_id=reserva.id)

            pago.cancelarPago()

        self.perform_destroy(instalacion)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InstalacionSinAgendaViewSet(viewsets.ModelViewSet):
    serializer_class = InstalacionSinAgendaSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Instalacion.objects.prefetch_related("agenda")


class InstalacionSimpleViewSet(viewsets.ModelViewSet):
    serializer_class = InstalacionSimpleSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Instalacion.objects.prefetch_related("agenda")


class PabellonViewSet(viewsets.ModelViewSet):
    queryset = Pabellon.objects.all()
    serializer_class = PabellonSerializer
    permission_classes = [AllowAny]

class PabellonSimpleViewSet(viewsets.ModelViewSet):
    queryset = Pabellon.objects.all()
    serializer_class = PabellonSimpleSerializer
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
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return EntradaListaEspera.objects.filter(usuarioFinal__user=self.request.user)


# ----------------
# Monitores
# ----------------

class MonitorViewSet(viewsets.ModelViewSet):
    serializer_class = MonitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_monitor:
            return Monitor.objects.filter(user=self.request.user)
        elif user.is_administrador:
            return Monitor.objects.all()

    def update(self, request, *args, **kwargs):
        monitor = self.get_queryset().first()
        serializer = self.get_serializer(
            monitor,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MonitorSimpleViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSimpleSerializer
    permission_classes = [IsAuthenticated]


# ----------------
# Notificaciones
# ----------------


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

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
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return ReservaActividad.objects.filter(usuarioFinal__user=self.request.user)


class ReservaActividadSimpleViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaActividadSimpleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return ReservaActividad.objects.filter(usuarioFinal__user=self.request.user)


class AlquilerViewSet(viewsets.ModelViewSet):
    serializer_class = AlquilerSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return Alquiler.objects.filter(usuarioFinal__user=self.request.user)


class AlquilerSimpleViewSet(viewsets.ModelViewSet):
    serializer_class = AlquilerSimpleSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return Alquiler.objects.filter(usuarioFinal__user=self.request.user)


# ----------------
# Tarifas
# ----------------

class TarifaTDAViewSet(viewsets.ModelViewSet):
    queryset = TarifaTDA.objects.all()
    serializer_class = TarifaTDASerializer
    permission_classes = [IsAuthenticated]


class TarifaInstalacionViewSet(viewsets.ModelViewSet):
    queryset = TarifaInstalacion.objects.all()
    serializer_class = TarifaInstalacionSerializer
    permission_classes = [IsAuthenticated]


class TarifaActividadViewSet(viewsets.ModelViewSet):
    queryset = TarifaActividad.objects.all()
    serializer_class = TarifaActividadSerializer
    permission_classes = [IsAdministradorTarifas]


class ActividadComunViewSet(viewsets.ModelViewSet):
    queryset = ActividadComun.objects.all()
    serializer_class = ActividadComunSerializer
    permission_classes = [IsAdministradorTarifas]


class GrupoReducidoViewSet(viewsets.ModelViewSet):
    queryset = GrupoReducido.objects.all()
    serializer_class = GrupoReducidoSerializer
    permission_classes = [IsAdministradorTarifas]


class FisioterapiaViewSet(viewsets.ModelViewSet):
    queryset = Fisioterapia.objects.all()
    serializer_class = FisioterapiaSerializer
    permission_classes = [IsAdministradorTarifas]


# ----------------
# TDA
# ----------------

class TDAViewSet(viewsets.ModelViewSet):
    serializer_class = TDASerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # El usuario puede ver su TDA
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            # Solo administrador puede modificar/borrar/crear
            permission_classes = [IsAdministradorUsuarios]
        else:
            permission_classes = [IsAdministradorUsuarios]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        try:
            if self.request.user.usuario_final:
                return TDA.objects.filter(usuarioFinal__user=self.request.user)
            return TDA.objects.all()
        except:
            return TDA.objects.all()

    def perform_create(self, serializer):
        usuario_id = self.request.data.get("usuario_id")
        usuario_final = UsuarioFinal.objects.get(id=usuario_id)

        tarifa = TarifaTDA.objects.first()

        serializer.save(
            usuarioFinal=usuario_final,
            fechaExpiracion=now().date() + relativedelta(years=1),
            estado=EstadoReserva.CONFIRMADA,
            tarifa=tarifa
        )

        usuario_final.tieneTDA = True
        usuario_final.save()
    
    def perform_destroy(self, instance):
        usuario_final = instance.usuarioFinal

        if usuario_final:
            usuario_final.tieneTDA = False
            usuario_final.save()

        instance.delete()


# ----------------
# Usuarios finales
# ----------------

class UsuarioFinalViewSet(viewsets.ModelViewSet):
    queryset = UsuarioFinal.objects.all()
    serializer_class = UsuarioFinalSerializer
    permission_classes = [AllowAny]

# ----------------
# Administradores
# ----------------

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        admin = self.request.user.administrador
        rol = serializer.validated_data.get("rol")

        if admin.rol != RolAdministrador.RAIZ and rol == RolAdministrador.RAIZ:
            raise PermissionDenied("No puedes crear administradores raíz")

        serializer.save()

    def perform_update(self, serializer):
        admin = self.request.user.administrador
        adminNuevo = self.get_object()

        nuevoRol = serializer.validated_data.get("rol", adminNuevo.rol)

        if admin.rol != RolAdministrador.RAIZ and adminNuevo.rol == RolAdministrador.RAIZ:
            raise PermissionDenied("No se puede modificar al administrador raíz")

        if admin.rol != RolAdministrador.RAIZ and nuevoRol == RolAdministrador.RAIZ:
            raise PermissionDenied("No puedes convertir a nadie en administrador raíz")

        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        admin = request.user.administrador
        adminObjetivo = self.get_object()

        if admin.rol != RolAdministrador.RAIZ and adminObjetivo.rol == RolAdministrador.RAIZ:
            raise PermissionDenied("No se puede eliminar al administrador raíz")

        return super().destroy(request, *args, **kwargs)


# ----------------
# User (Django auth) modificado
# ----------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministradorUsuarios]



# Otros endpoints

# Para devolver el usuario registrado
class meAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_monitor": getattr(user, "is_monitor", False),
            "is_usuario_final": getattr(user, "is_usuario_final", False),
            "is_administrador": getattr(user, "is_administrador", False),
            "is_superuser": getattr(user, "is_superuser", False),
        }

        try:
            data["usuario_final_id"] = user.usuario_final.id
        except User.usuario_final.RelatedObjectDoesNotExist:
            data["usuario_final_id"] = None

        try:
            data["monitor_id"] = user.monitor.id
        except User.monitor.RelatedObjectDoesNotExist:
            data["monitor_id"] = None

        try:
            admin = user.administrador
            data["administrador_id"] = admin.id
            data["rol"] = getattr(admin, "rol", None)
        except User.administrador.RelatedObjectDoesNotExist:
            data["administrador_id"] = None
            data["rol"] = None

        return Response(data)


class CodigoNuevaPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        tipo = request.data.get("tipo")

        if tipo == "enviar":
            codigo = str(random.randint(100000, 999999))
            user = User.objects.filter(email=email).first()

            if not user:
                return Response({"respuesta": "El correo no existe en el sistema", "tipo": "email"}, status=status.HTTP_400_BAD_REQUEST)

            CodigoResetPassword.objects.filter(email=email).delete()
            CodigoResetPassword.objects.create(email=email, codigo=codigo)

            try:
                resend.api_key = os.environ.get("RESEND_API_KEY")
                resend.Emails.send({
                    "from": "Polideportivo <onboarding@resend.dev>",
                    "to": email,
                    "subject": "Código de recuperación",
                    "text": f"Tu código de recuperación es: {codigo}"
                })

                print("EMAIL ENVIADO CORRECTAMENTE A:", email)

            except Exception as e:
                print("ERROR SEND MAIL:", type(e).__name__, str(e))
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Código enviado"})

        elif tipo == "verificar":
            codigo = request.data.get("codigo")

            try:
                reset_code = CodigoResetPassword.objects.get(email=email, codigo=codigo)
                if not reset_code.isValid():
                    return Response({"respuesta": "Código expirado"}, status=status.HTTP_400_BAD_REQUEST)

                user = User.objects.filter(email=email).first()
                usuario = UsuarioFinal.objects.filter(user=user).first()
                return Response({"respuesta": "Codigo correcto", "id_usuario": usuario.id}, status=status.HTTP_200_OK)

            except CodigoResetPassword.DoesNotExist:
                return Response({"respuesta": "Código inválido"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"respuesta": "Error, decisión inválida"}, status=status.HTTP_400_BAD_REQUEST)


# Funcion auxuliar para obtener el formato de las enumeraciones
def format_choices(choices):
    return [value for value, label in choices]

# Estadisticas para el usuario
class EstadisticasView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):                
        deportes = list(Deporte.objects.values("id", "titulo"))

        data = {
            "instalaciones": Instalacion.contar(),
            "actividades": Actividad.contar(),
            "pabellones": Pabellon.contar(),
            "deportes": Deporte.contar(),
            "usuarios": UsuarioFinal.contar(),
            "tiposActividad": format_choices(TipoActividad.choices),
            "tiposInstalacion": format_choices(TipoInstalacion.choices),
            "tiposDeporte": deportes
        }

        return Response(data)


# Informacion con los tipos de cada grupo necesario: reservas, actividades, terrenos, etc
class TiposViews(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "tiposActividad": format_choices(TipoActividad.choices),
            "tiposInstalacion": format_choices(TipoInstalacion.choices),
            "tiposReserva": format_choices(FormaReserva.choices),
            "terrenos": format_choices(Terreno.choices),
            "estados": format_choices(Estado.choices),
            "dias": format_choices(Dia.choices),
            "periodos": format_choices(Periodo.choices)
        }

        return Response(data)


# Busquedas
class BuscarView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nombre = request.query_params.get('busqueda')
        horaApertura = request.query_params.get('tiempoInicioInstalacion')
        horaCierre = request.query_params.get('tiempoFinInstalacion')
        horaInicioSesion = request.query_params.get('tiempoInicioActividad')
        horaFinSesion = request.query_params.get('tiempoFinActividad')

        dias = request.query_params.getlist('dias')
        dias = [d.lower() for d in dias]

        tiposActividad = request.query_params.getlist('tiposActividad')
        tiposInstalacion = request.query_params.getlist('tiposInstalacion')

        instalaciones = Instalacion.buscar(nombre, tiposInstalacion, horaApertura, horaCierre)
        actividades = Actividad.buscar(nombre, tiposActividad, horaInicioSesion, horaFinSesion, dias)

        data = {
            "instalaciones": InstalacionSimpleSerializer(instalaciones, many=True).data,
            "actividades": ActividadSimpleSerializer(actividades, many=True).data,
        }

        return Response(data)


# Registro
class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        sexo = request.data.get('sexo')
        fechaNacimiento = request.data.get('fechaNacimiento')
        dni = request.data.get('dni')
        telefono = request.data.get('telefono')
        email = request.data.get('email')
        provincia = request.data.get('provincia')
        municipio = request.data.get('municipio')
        localidad = request.data.get('localidad')
        codigoPostal = request.data.get('codigoPostal')
        password = request.data.get('password')
        esUAM = request.data.get('esUAM')

        respuesta = UsuarioFinal.registrarUsuario(
            nombre=nombre, apellidos=apellidos, sexo=sexo, fechaNacimiento=fechaNacimiento,
            dni=dni, telefono=telefono, email=email, provincia=provincia,
            municipio=municipio, localidad=localidad, codigoPostal=codigoPostal,
            password=password, esUAM=esUAM
        )

        if respuesta["error"]:
            return Response({"mensaje": respuesta["respuesta"], "tipo": respuesta["tipo"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsuarioFinalSerializer(respuesta["respuesta"])
        usuarioFinal = serializer.data

        return Response(usuarioFinal)


# Registrar monitor
class RegistroMonitorView(APIView):
    permission_classes = [IsAdministradorUsuarios]

    def post(self, request):
        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        email = request.data.get('email')
        dni = request.data.get('dni')
        password = request.data.get('password')

        respuesta = Monitor.registrarMonitor(
            nombre=nombre, apellidos=apellidos, dni=dni, 
            email=email, password=password
        )

        if respuesta["error"]:
            return Response({"mensaje": respuesta["respuesta"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MonitorSerializer(respuesta["respuesta"])
        monitor = serializer.data

        return Response(monitor)

# Registrar administrador
class RegistroAdministradorView(APIView):
    permission_classes = [IsAdministradorUsuarios]

    def post(self, request):
        nombre = request.data.get('nombre')
        rol = request.data.get('rol')
        email = request.data.get('email')
        dni = request.data.get('DNI')
        password = request.data.get('password')

        respuesta = Administrador.registrarAdministrador(
            nombre=nombre, rol=rol, dni=dni, 
            email=email, password=password
        )

        if respuesta["error"]:
            return Response({"mensaje": respuesta["respuesta"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdministradorSerializer(respuesta["respuesta"])
        admin = serializer.data

        return Response(admin)


# Reaccionar a la notificacion de la lista de espera
class AccionNotificacionView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, notificacion_id):
        notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
        aceptar = request.data.get("aceptar", False)

        notificacion.actividad.plazasReservadas -= 1
        notificacion.actividad.save()

        if not aceptar:
            lista_espera = notificacion.actividad.lista_espera
            while notificacion.actividad.plazasReservadas < notificacion.actividad.plazasMaximas:
                entrada = lista_espera.siguienteUsuario()
                if not entrada:
                    break

                notificacion.actividad.plazasReservadas += 1
                notificacion.actividad.save()

                Notificacion.notificarSalidaListaDeEspera(entrada.usuarioFinal, notificacion.actividad)

        return Response({"respuesta": "Exito"},  status=status.HTTP_200_OK)


# Crear nuevas notificaciones
class NuevaNotificacionView(APIView):
    permission_classes = [IsAdministrador]

    def post(self, request):
        titulo = request.data.get("titulo")
        descripcion = request.data.get("descripcion")
        tipo = request.data.get("usuarios")
        actividad_id = request.data.get("actividad_id", "")
        instalacion_id = request.data.get("instalacion_id", "")
        pabellon_id = request.data.get("pabellon_id", "")

        complemento = None

        if tipo == "ACTIVIDAD":
            complemento = actividad_id
        elif tipo == "INSTALACION":
            complemento = instalacion_id
        elif tipo == "PABELLON":
            complemento = pabellon_id

        Notificacion.nuevaNotificacion(titulo, descripcion, tipo, complemento)
        return Response({"respuesta": "Notificacion creada correctamente"}, status=status.HTTP_200_OK)


# Guardar informacion de notificaciones o recuperarlas
class GuardarNotificacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_usuario_final:
            user.usuario_final.revisarActividades()
        elif user.is_monitor:
            user.monitor.revisarActividades()

        notificaciones = Notificacion.objects.filter(usuario=user)
        return Response(NotificacionSerializer(notificaciones, many=True).data)

    def post(self, request):
        notificaciones = request.data.get('notificaciones', [])

        for n in notificaciones:
            Notificacion.cambiarEstado(
                usuario=request.user,
                id=n['id'],
                leido=n['leido'],
                fijado=n['fijado']
            )

        return Response({"respuesta": "Notificacion modificada correctamente"}, status=status.HTTP_200_OK)


# Asignar la TDA al usuario
class ValidarTDAView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request):
        codigo = request.data.get("codigo")

        tda = TDA.objects.filter(usuarioFinal__isnull=True, codigo_qr=codigo).first()

        if tda:
            resultado = tda.asignarUsuario(codigo, request.user.usuario_final)
            if resultado:
                return Response({"respuesta": "TDA validada correctamente"}, status=status.HTTP_200_OK)

        return Response({"respuesta": "Error al validar la TDA correctamente"}, status=status.HTTP_400_BAD_REQUEST)


# Obtener actividades e instalaciones de una lista de ids dados
class ObtenerActividadesInstalaciones(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        actividad_ids = request.data.get("actividad_ids", [])
        instalacion_ids = request.data.get("instalacion_ids", [])

        actividades = Actividad.objects.filter(id__in=actividad_ids)
        instalaciones = Instalacion.objects.filter(id__in=instalacion_ids)

        data = {
            "actividades": ActividadSerializer(actividades, many=True).data,
            "instalaciones": InstalacionSerializer(instalaciones, many=True).data,
        }

        return Response(data)


# Obtener actividades e instalaciones favoritos de un usuario
class ObtenerActividadesInstalacionesFavoritas(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request):
        usuarioFinal = request.user.usuario_final

        actividades = Actividad.objects.filter(favorita__usuarioFinal=usuarioFinal)
        instalaciones = Instalacion.objects.filter(favorito__usuarioFinal=usuarioFinal)

        data = {
            "actividades": ActividadSerializer(actividades, many=True).data,
            "instalaciones": InstalacionSerializer(instalaciones, many=True).data,
        }

        return Response(data)



# Crear nuevas sesiones en una actividad
class NuevaSesionView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)
        instalacion = get_object_or_404(Instalacion, id=actividad.instalacion.id)
        
        sesiones = request.data
        if isinstance(sesiones, dict):
            sesiones = [sesiones]

        for sesion in sesiones:
            dia = sesion.get('dia')
            horaInicio = sesion.get('horaInicio')
            horaFin = sesion.get('horaFin')
            
            respuesta = instalacion.controlarHorarioActividad(dia, horaInicio, horaFin)
            if not respuesta:
                return Response({"respuesta": "Una o más sesiones no se pueden realizar en esta instalación en el horario previsto"}, status=status.HTTP_400_BAD_REQUEST)

            respuesta = actividad.nuevaSesion(dia, horaInicio, horaFin)

            if not respuesta:
                return Response({"respuesta": "No se ha podido crear ninguna sesión"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"respuesta": "sesiones creadas correctamente"}, status=status.HTTP_200_OK)        


# Marcar o desmarcar actividades o instalaciones como favoritos
class AlterarFavoritosView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request):
        usuarioFinal = request.user.usuario_final

        actividad_ids = request.data.get("actividad_ids", [])
        instalacion_ids = request.data.get("instalacion_ids", [])

        if not actividad_ids and not instalacion_ids:
            return Response({"status": "error"})

        for act_id in actividad_ids:
            actividad = Actividad.objects.filter(id=act_id).first()
            if actividad:
                usuarioFinal.cambiarFavorito(actividad=actividad)

        for ins_id in instalacion_ids:
            instalacion = Instalacion.objects.filter(id=ins_id).first()
            if instalacion:
                usuarioFinal.cambiarFavorito(instalacion=instalacion)
        
        return Response({"status": "ok"})


# Obtener las reservas tanto de alquileres de instalaciones como reservas de actividades
class ReservasView(APIView):
    permission_classes = [IsUsuarioFinal]

    def get(self, request):
        user = request.user
        reservas = []
        ahora = timezone.now()
        hoy = ahora.date()
        hora_actual = ahora.time()

        alquileres = Alquiler.objects.filter(
            usuarioFinal__user=user,
            estado=EstadoReserva.CONFIRMADA
        ).filter(
            Q(fecha__gt=hoy) |
            Q(fecha=hoy, horaInicio__gte=hora_actual)
        )

        actividades = ReservaActividad.objects.filter(usuarioFinal__user=user, estado=EstadoReserva.CONFIRMADA)
        listas_espera = EntradaListaEspera.objects.filter(usuarioFinal__user=user)

        alquiler_ct = ContentType.objects.get_for_model(Alquiler)
        reserva_ct = ContentType.objects.get_for_model(ReservaActividad)

        for alquiler in alquileres:
            pago = Pago.objects.get(content_type=alquiler_ct, object_id=alquiler.id)

            calle = None
            if alquiler.calle:
                calle = alquiler.calle.numero

            reservas.append({
                "id": alquiler.id,
                "tipo": "ALQUILER",
                "estado": alquiler.estado,
                "puede_cancelar": True,
                "instalacion": {
                    "id": alquiler.instalacion.id,
                    "nombre": alquiler.instalacion.nombre,
                    "tipo": getattr(alquiler.instalacion, "tipoInstalacion", None),
                },
                "actividad": None,
                "fecha": str(alquiler.fecha) if hasattr(alquiler, "fecha") else None,
                "calle": calle,
                "horaInicio": alquiler.horaInicio,
                "horaFin": alquiler.horaFin,
                "coste": pago.costeFinal,
                "tarifa": None,
                "descuentos": [],
            })

        for reserva_act in actividades:
            pago = Pago.objects.get(content_type=reserva_ct, object_id=reserva_act.id)

            sesiones = reserva_act.actividad.sesiones.all()
            reservas.append({
                "id": reserva_act.id,
                "tipo": "RESERVA",
                "estado": reserva_act.estado,
                "puede_cancelar": True,
                "actividad": {
                    "id": reserva_act.actividad.id,
                    "nombre": reserva_act.actividad.nombre,
                    "dias": [
                        {
                            "dia": s.dia,
                            "horaInicio": s.horaInicio.strftime("%H:%M"),
                            "horaFin": s.horaFin.strftime("%H:%M"),
                        }
                        for s in sesiones
                    ],
                    "horasSemanales": getattr(reserva_act.actividad, "calcularHorasSemanales", lambda: None)(),
                    "periodo": reserva_act.actividad.periodo,
                },
                "instalacion": None,
                "fecha": str(reserva_act.actividad.periodo_inicio) if hasattr(reserva_act.actividad, "periodo_inicio") else None,
                "horaInicio": None,
                "horaFin": None,
                "coste": pago.costeFinal,
                "descuentos": [
                    {"id": d.id, "nombre": d.nombre, "porcentaje": d.porcentaje} 
                    for d in getattr(reserva_act, "descuentos", []).all()
                ],
            })
        
        for entrada in listas_espera:
            actividad = entrada.listaEspera.actividad
            sesiones = actividad.sesiones.all()

            # Calcular posicion en la lista
            posicion = list(actividad.lista_espera.registro.all()).index(entrada) + 1

            reservas.append({
                "id": entrada.id,
                "tipo": "LISTA_ESPERA",
                "estado": "En espera",
                "puede_cancelar": True,

                "actividad": {
                    "id": actividad.id,
                    "nombre": actividad.nombre,
                    "dias": [
                        {
                            "dia": s.dia,
                            "horaInicio": s.horaInicio.strftime("%H:%M"),
                            "horaFin": s.horaFin.strftime("%H:%M"),
                        }
                        for s in sesiones
                    ],
                    "horasSemanales": getattr(actividad, "calcularHorasSemanales", lambda: None)(),
                    "periodo": actividad.periodo,
                },

                "instalacion": None,
                "fecha": str(entrada.fechaEntrada),
                "horaInicio": entrada.horaEntrada,
                "horaFin": None,
                "coste": None,
                "posicion": posicion,

                "descuentos": [],
            })

        return Response(reservas)


# Mostrar todos los abonos tanto deportivos como de verano
class ObtenerAbonosView(APIView):
    permission_classes = [IsUsuarioFinal | IsAdministradorTarifas]
    
    def get(self, request):
        abonos_deportivos = AbonoDeportivo.objects.all()
        abonos_verano = AbonoVerano.objects.all()

        return Response({
            "abonosDeportivos": AbonoDeportivoSerializer(abonos_deportivos, many=True).data,
            "abonosVerano": AbonoVeranoSerializer(abonos_verano, many=True).data
        })


# Mostrar el foro y los canales, pero sin los mensajes
class ForoView(APIView):
    permission_classes = [IsUsuarioFinal | IsAdministradorUsuarios]

    def get(self, request):
        foro = Foro.objects.first()

        if request.user.is_usuario_final:
            canales = Canal.objects.filter(
                foro=foro,
                oculto=False,
                usuarioFinal__usuarioFinal=request.user.usuario_final,
                usuarioFinal__expulsado=False
            ).distinct()

            serializer = CanalUsuarioFinalSerializer(
                canales,
                many=True,
                context={"request": request}
            )
            return Response(serializer.data)

        elif request.user.is_administrador:
            serializer = ForoSerializer(foro)
            return Response(serializer.data)

        return Response({"respuesta": "Usuario incorrecto"}, status=status.HTTP_400_BAD_REQUEST)


# Mostrar la informacion de un canal para el admin
class CanalAdministradorView(APIView):
    permission_classes = [IsAdministradorUsuarios]

    def get(self, request, canal_id):
        canal = get_object_or_404(Canal, id=canal_id)

        serializer = CanalAdministradorSerializer(canal)
        return Response(serializer.data)


# Crear nuevos canales en el foro
class NuevoCanalView(APIView):
    permission_classes = [IsAdministradorUsuarios]

    def post(self, request, foro_id):
        foro = get_object_or_404(Foro, id=foro_id)

        titulo = request.data.get('titulo')
        tema = request.data.get('tema')
        secreto = request.data.get('secreto')
        oculto = request.data.get('oculto')

        respuesta = foro.nuevoCanal(titulo, tema, secreto, oculto)
        
        if respuesta:
            return Response({"respuesta": "Exito al crear el canal"}, status=status.HTTP_200_OK)

        return Response({"respuesta": "No se ha podido crear el canal"}, status=status.HTTP_400_BAD_REQUEST)


# Mostrar los mensajes de un canal o escribir nuevos
class MensajesCanalView(APIView):
    permission_classes = [IsUsuarioFinal | IsAdministradorUsuarios]
    
    def get(self, request, canal_id):
        canal = get_object_or_404(Canal, id=canal_id)

        mensajes = canal.getMensajes().order_by("fechaEnvio")
        
        serializer = MensajeSerializer(mensajes, many=True)

        return Response(serializer.data)

    def post(self, request, canal_id):
        canal = get_object_or_404(Canal, id=canal_id)

        resultado = canal.nuevoMensaje(request.user, request.data.get("texto", ""))

        if resultado:
            return Response({"respuesta": "Mensaje enviado"}, status=status.HTTP_201_CREATED)

        return Response({"respuesta": "No puedes escribir en este canal"}, status=status.HTTP_400_BAD_REQUEST)


class GestionarUsuarioCanalView(APIView):
    permission_classes = [IsAdministradorUsuarios]

    def patch(self, request, canal_id, usuario_id):
        accion = request.data
        canal = get_object_or_404(Canal, id=canal_id)
        usuarioFinal = get_object_or_404(UsuarioFinal, id=usuario_id)

        if accion == "silenciar":
            if canal.cambiarSilencioUsuario(usuarioFinal):
                return Response({"respuesta": "Usuario silenciado con exito"}, status=status.HTTP_201_CREATED)

        elif accion == "expulsar":
            if canal.cambiarExpulsionUsuario(usuarioFinal):
                return Response({"respuesta": "Usuario expulsado con exito"}, status=status.HTTP_201_CREATED)

        return Response({"respuesta": "Error"}, status=status.HTTP_400_BAD_REQUEST)


# Mostrar las sesiones del monitor
class SesionesMonitorView(APIView):
    permission_classes = [IsMonitor | IsAdministradorEspacios]

    def get(self, request, monitor_id):
        sesiones = []

        actividades = Actividad.objects.filter(monitor_id=monitor_id)
        
        for actividad in actividades:
            for sesion in actividad.sesiones.all():
                sesiones.append({
                    "idActividad": actividad.id,
                    "idSesion": sesion.id,
                    "nombre": actividad.nombre,
                    "dia": sesion.dia,
                    "horaInicio": sesion.horaInicio,
                    "horaFin": sesion.horaFin
                })

        return Response(sesiones)


# Mostrar informacion en detalle de una sesion para el monitor
class DetalleSesionView(APIView):
    permission_classes = [IsMonitor | IsAdministradorEspacios]

    def get(self, request, actividad_id, sesion_id):
        data = []

        actividad = get_object_or_404(Actividad, id=actividad_id)
        sesion = get_object_or_404(Sesion, id=sesion_id, actividad=actividad)

        data = {
            "id": sesion.id,
            "dia": sesion.dia,
            "horaInicio": sesion.horaInicio,
            "horaFin": sesion.horaFin,
            "duracion": sesion.numeroHoras * 60,
            "totalParticipantes": actividad.plazasReservadas,
            "presentes": sesion.asistencias.filter(presente=True).count(),
            "actividad": {
                "nombre": actividad.nombre,
                "periodo": actividad.periodo,
                "terreno": actividad.terreno,
                "nivel": actividad.nivel,
                "instalacion": {
                    "id": actividad.instalacion.id,
                    "nombre": actividad.instalacion.nombre
                }
                },
                "participantes": []
            }

        for asistencia in sesion.asistencias.all():
            data["participantes"].append({
                "id": asistencia.usuarioFinal.id,
                "nombre": asistencia.usuarioFinal.nombre,
                "presente": asistencia.presente
            })

        return Response(data)


class GuardarAsistenciaView(APIView):
    permission_classes = [IsMonitor]

    def post(self, request, actividad_id, sesion_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)
        sesion = get_object_or_404(Sesion, id=sesion_id, actividad=actividad)

        # Desde el frontend enviamos los usuarios que han cambiado en el campo presente
        participantes = request.data.get("participantes", [])

        for participante in participantes:
            usuarioFinal = get_object_or_404(UsuarioFinal, id=participante["id"])
            resultado = sesion.cambiarFalta(usuarioFinal, participante["presente"])

            if not resultado:
                return Response({"respuesta": "Error al pasar lista"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"respuesta": "Resultados cambiados correctamente"}, status=status.HTTP_200_OK)


class NuevaInstalacionView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request):

        instalacion_json = request.POST.get("instalacion", "{}")
        instalacion_data = json.loads(instalacion_json)
        imagen = request.FILES.get("imagen")

        pabellon_id = instalacion_data.pop("pabellon", None)
        tarifa_id = instalacion_data.pop("tarifa", None)
        numero_calles = instalacion_data.pop("numeroCalles", 0)

        if not pabellon_id or not tarifa_id:
            return Response(
                {"respuesta": "Faltan datos obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pabellon = get_object_or_404(Pabellon, id=pabellon_id)
        tarifa = get_object_or_404(TarifaInstalacion, id=tarifa_id)

        instalacion = Instalacion.objects.create(
            **instalacion_data,
            pabellon=pabellon,
            tarifa=tarifa,
            imagen=imagen
        )
        
        if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
            instalacion.sincronizarCalles(numero_calles)

        agenda_json = request.POST.get("agenda", "[]")
        fechasEspeciales_json = request.POST.get("fechasEspeciales", "[]")

        agenda = json.loads(agenda_json)
        fechasEspeciales = json.loads(fechasEspeciales_json)

        for fecha in agenda:
            res = instalacion.controlarCambioHorario(
                fecha["dia"],
                fecha.get("apertura"),
                fecha.get("cierre"),
                fecha.get("abierto", True)
            )

            if not res:
                raise Exception("El cambio de horario no está permitido")

            res = instalacion.nuevoHorario(
                fecha["dia"],
                fecha.get("apertura"),
                fecha.get("cierre"),
                fecha.get("abierto", True)
            )

            if not res:
                raise Exception("Error al actualizar la agenda")

        for fecha in fechasEspeciales:
            res = instalacion.nuevoHorarioEspecial(
                fecha["fecha"],
            )

            if not res:
                raise Exception("Error al actualizar fechas especiales")

        sesiones = Sesion.objects.filter(actividad__instalacion=instalacion)

        sesiones_data = [{
            "dia": s.dia,
            "horaInicio": s.horaInicio.strftime("%H:%M"),
            "horaFin": s.horaFin.strftime("%H:%M"),
            "calle": s.calle
        } for s in sesiones]

        instalacion.actualizarMapa(sesiones_data)

        return Response(
            {"respuesta": "Instalación creada correctamente"},
            status=status.HTTP_201_CREATED
        )


class EditarInstalacionView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request, instalacion_id):
        try:
            instalacion = get_object_or_404(Instalacion, id=instalacion_id)

            # Datos de la instalacion
            instalacion_json = request.POST.get("instalacion", "{}")
            instalacion_data = json.loads(instalacion_json)

            imagen = request.FILES.get("imagen")

            pabellon_id = instalacion_data.pop("pabellon", None)
            if isinstance(pabellon_id, dict):
                pabellon_id = pabellon_id.get("id")

            tarifa_id = instalacion_data.pop("tarifa", None)
            numero_calles = instalacion_data.pop("numeroCalles", None)

            pabellon = get_object_or_404(Pabellon, id=pabellon_id)
            tarifa = get_object_or_404(TarifaInstalacion, id=tarifa_id)

            if not instalacion.comprobarAforo(instalacion_data["aforoMaximo"], numero_calles):
                return Response({"respuesta": "La instalación tiene una actividad con unas plazas máximas mayores que el aforo creado", "tipo": "aforo"}, status=status.HTTP_400_BAD_REQUEST)

            # Manejar la agenda y fechas especiales
            agenda_json = request.POST.get("agenda", "[]")
            fechasEspeciales_json = request.POST.get("fechasEspeciales", "[]")

            agenda = json.loads(agenda_json)
            fechasEspeciales = json.loads(fechasEspeciales_json)

            # AGENDA SEMANAL
            agendas_existentes = {
                a.dia.lower(): a
                for a in Agenda.objects.filter(
                    instalacion=instalacion,
                    fecha__isnull=True
                )
            }

            dias_recibidos = set()

            for item in agenda:
                dia = item["dia"].lower()
                dias_recibidos.add(dia)

                apertura = item.get("horaApertura")
                cierre = item.get("horaCierre")
                abierto = item.get("abierto", True)

                agenda_existente = agendas_existentes.get(dia)

                if agenda_existente:
                    # Validamos el conflicto
                    if not instalacion.controlarCambioHorario(dia, apertura, cierre, abierto):
                        return Response(
                            {"respuesta": f"No se puede modificar el día {dia} por conflictos existentes", "tipo": "sesiones"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    agenda_existente.horaApertura = apertura
                    agenda_existente.horaCierre = cierre
                    agenda_existente.abierto = abierto
                    agenda_existente.save()

                    instalacion.sincronizarMapaReservas(agenda_existente)
                else:
                    if not instalacion.nuevoHorario(dia, apertura, cierre, abierto):
                        return Response(
                            {"respuesta": f"Error creando horario para {dia}", "tipo": "otro"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

           # FECHAS ESPECIALES
            especiales_existentes = {
                str(a.fecha): a
                for a in Agenda.objects.filter(
                    instalacion=instalacion,
                    fecha__isnull=False
                )
            }

            fechas_recibidas = set()

            for item in fechasEspeciales:
                fecha = item["fecha"]
                fechas_recibidas.add(str(fecha))

                if str(fecha) not in especiales_existentes:
                    res = instalacion.nuevoHorarioEspecial(fecha)

                    if not res:
                        return Response(
                            {"respuesta": f"Error creando día cerrado {fecha}", "tipo": "otro"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Eliminar las que ya no existen
            for fecha, agenda in especiales_existentes.items():
                if fecha not in fechas_recibidas:
                    agenda.delete()

            instalacion.modificarInformacion(instalacion_data, pabellon, tarifa, imagen)
            if numero_calles is not None:
                instalacion.sincronizarCalles(numero_calles)

            sesiones = Sesion.objects.filter(actividad__instalacion=instalacion)

            sesiones_data = [{
                "dia": s.dia,
                "horaInicio": s.horaInicio.strftime("%H:%M"),
                "horaFin": s.horaFin.strftime("%H:%M"),
                "calle": s.calle
            } for s in sesiones]

            instalacion.actualizarMapa(sesiones_data)
            
            return Response({"respuesta": "Exito al asignar la agenda a la instalacion"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"respuesta": str(e), "tipo": "otro"}, status=status.HTTP_400_BAD_REQUEST)


class NuevaActividadView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request):
        actividad_json = request.data.get("actividad", "{}")
        actividad_data = json.loads(actividad_json)
        imagen = request.FILES.get("imagen")

        tarifa_id = actividad_data.pop("tarifa", None)
        instalacion_id = actividad_data.pop("instalacion", None)
        monitor_id = actividad_data.pop("monitor", None)

        tarifa = get_object_or_404(TarifaActividad, id=tarifa_id)
        instalacion = get_object_or_404(Instalacion, id=instalacion_id)
        monitor = get_object_or_404(Monitor, id=monitor_id)

        sesiones_json = request.data.get("sesiones", "[]")
        periodo = request.data.get("periodo")
        sesiones = json.loads(sesiones_json)

        if not monitor.comprobarDisponibilidad(sesiones, periodo):
            return Response(
                {"respuesta": "El monitor ya tiene una sesion en uno de los periodos propuestos", "tipo": "monitor"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar horarios primero
        for sesion in sesiones:
            dia = sesion.get('dia')
            horaInicio = sesion.get('horaInicio')

            horaFin = sesion.get('horaFin')
            calleNum = sesion.get('calle')

            calle = None
            if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
                calle = instalacion.calles.filter(id=calleNum).first()

                if not calle:
                    return Response({"respuesta": "Calle no válida", "tipo": "calle"}, status=status.HTTP_400_BAD_REQUEST)

            if not instalacion.controlarHorarioActividad(dia, horaInicio, horaFin, periodo, calle=calle):
                return Response(
                    {"respuesta": "Una o más sesiones no se pueden realizar en esta instalación", "tipo": "sesiones"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Crear actividad
        actividad = Actividad.objects.create(
            **actividad_data,
            tarifa=tarifa,
            instalacion=instalacion,
            monitor=monitor,
            imagen=imagen
        )

        instalacion.revisarAlquileres(sesiones, periodo, True)

        ListaEspera.objects.create(actividad=actividad)

        # Crear sesiones
        for sesion in sesiones:
            calleNum = sesion.get('calle')

            calle = None
            if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
                calle = instalacion.calles.filter(id=calleNum).first()

            actividad.nuevaSesion(
                sesion.get('dia'),
                sesion.get('horaInicio'),
                sesion.get('horaFin'),
                calle
            )

        # Deporte
        nombre_json = request.POST.get("deportes", "[]")
        nombre = json.loads(nombre_json).strip()

        titulo = nombre.lower().replace(" ", "_")

        deporte, _ = Deporte.objects.get_or_create(titulo=titulo)

        actividad.deportes = deporte
        actividad.save()

        instalacion.actualizarMapa(sesiones)
        Notificacion.notificarNuevaActividad(actividad)

        return Response({
            "respuesta": "Actividad creada correctamente",
            "actividad_id": actividad.id
        }, status=status.HTTP_201_CREATED)


class EditarActividadView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request, actividad_id):
        try:
            actividad = get_object_or_404(Actividad, id=actividad_id)

            actividad_json = request.POST.get("actividad", "{}")
            actividad_data = json.loads(actividad_json)
            imagen = request.FILES.get("imagen")

            tarifa_id = actividad_data.pop("tarifa", None)
            instalacion_id = actividad_data.pop("instalacion", None)
            monitor_id = actividad_data.pop("monitor", None)

            tarifa = get_object_or_404(TarifaActividad, id=tarifa_id)
            instalacion = get_object_or_404(Instalacion, id=instalacion_id)
            monitor = get_object_or_404(Monitor, id=monitor_id)

            sesiones_json = request.POST.get("sesiones", "[]")
            sesiones_recibidas = json.loads(sesiones_json)
            periodo = request.data.get("periodo")
    
            sesiones_bd = actividad.sesiones.all()
            ids_recibidos = []

            if not monitor.comprobarDisponibilidad(sesiones_recibidas, periodo, actividad_data["id"]):
                return Response(
                    {"respuesta": "El monitor ya tiene una sesion en uno de los periodos propuestos", "tipo": "monitor"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cambios = False
            for sesion_data in sesiones_recibidas:
                dia = sesion_data.get('dia')
                horaInicio = sesion_data.get('horaInicio')
                horaFin = sesion_data.get('horaFin')
                sesion_id = sesion_data.get('id')
                calleNum = sesion_data.get('calle')
                
                calle = None
                if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
                    calle = instalacion.calles.filter(id=calleNum).first()

                respuesta = instalacion.controlarHorarioActividad(dia, horaInicio, horaFin, periodo, sesion_id, calle)

                if not respuesta:
                    return Response(
                        {"respuesta": "Una o más sesiones no se pueden realizar en esta instalación en el horario elegido", "tipo": "sesiones"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if not sesion_id or sesion_id == -1:
                    nueva = actividad.nuevaSesion(dia, horaInicio, horaFin, calle)
                    ids_recibidos.append(nueva.id)
                    cambios = True
                else:
                    sesion_existente = sesiones_bd.filter(id=sesion_id).first()

                    if sesion_existente:
                        sesion_existente.dia = dia
                        sesion_existente.horaInicio = horaInicio
                        sesion_existente.horaFin = horaFin
                        sesion_existente.calle = calle
                        sesion_existente.save()

                        ids_recibidos.append(sesion_existente.id)
                        cambios = True

            for sesion in sesiones_bd:
                if sesion.id not in ids_recibidos:
                    sesion.delete()
                    cambios = True

            # Nombre del deporte
            nombre_json = request.POST.get("deportes", "[]")
            nombre = json.loads(nombre_json)

            nombre = nombre.strip()
            titulo = nombre.lower().replace(" ", "_")

            deporte, _ = Deporte.objects.get_or_create(titulo=titulo)
            if actividad.deportes != deporte:
                actividad.deportes = deporte

            resultado = actividad.modificarInformacion(actividad_data, tarifa, instalacion, monitor, imagen)
            if not resultado:
                return Response({"respuesta": "Error al tratar de modificar la informacion", "tipo": "actividad"}, status=status.HTTP_400_BAD_REQUEST)

            instalacion.revisarAlquileres(sesiones_recibidas, periodo, True)

            if cambios:
                instalacion.actualizarMapa(sesiones_recibidas)
                Notificacion.notificarCambioSesiones(actividad)

            return Response({"respuesta": "Deporte asignado correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"respuesta": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ComprobarAlquileresView(APIView):
    permission_classes = [IsAdministradorEspacios]

    def post(self, request, instalacion_id):
        instalacion = get_object_or_404(Instalacion, id=instalacion_id)

        sesiones_json = request.data.get("sesiones", "[]")
        periodo = request.data.get("periodo")
        sesiones = json.loads(sesiones_json)

        resultado = instalacion.revisarAlquileres(sesiones, periodo, False)

        if not resultado or resultado["alquileres"] == 0:
            return Response({
                "conflicto": False,
                "mensaje": "No hay conflictos con alquileres"
            }, status=status.HTTP_200_OK)

        return Response({
            "conflicto": True,
            "alquileres_afectados": resultado["alquileres"],
            "usuarios_afectados": resultado["usuarios"],
            "dinero_a_devolver": resultado["dinero"]
        }, status=status.HTTP_200_OK)


class TarifaActividadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)
        usuarioFinal = request.user.usuario_final

        numeroSesiones = ReservaActividad.objects.filter(actividad=actividad, usuarioFinal=usuarioFinal).exclude(tipoSesion="consulta").count()

        precios = actividad.obtenerPrecios(numeroSesiones)
        data = {
            "tarifa": {
                "idActividad": actividad.id,
                "nombre": actividad.nombre,
                "numeroHoras": actividad.calcularHorasSemanales(),
                "horario": actividad.getHorario(),
                "tipo": actividad.tipoActividad,
                "numeroSesiones": numeroSesiones,
                "datos": precios
            },
            "descuento": {
                "porcentaje_total": 0,
                "aplicados": []
            }
        }

        descuentos = Descuento.obtenerDescuentos(actividad=actividad)
        if descuentos:
            data["descuento"]["porcentaje_total"] = descuentos["porcentaje_total"]
            for d in descuentos["descuentos"]:
                data["descuento"]["aplicados"].append({
                    "id": d.id,
                    "nombre": d.nombre,
                    "porcentaje": d.porcentaje
                })

        return Response(data)


class TarifaInstalacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, instalacion_id):
        instalacion = get_object_or_404(Instalacion, id=instalacion_id)

        precios = instalacion.obtenerPrecios()

        fecha_str = request.query_params.get('fecha')
        if fecha_str:
            fecha = parse_date(fecha_str)
        else:
            fecha = date.today()

        agenda_fecha = Agenda.objects.filter(fecha=fecha, instalacion=instalacion).first()

        # Obtenemos el día, directamente o derivandolo de la fecha dada
        if agenda_fecha:
            dia = None
        else:
            dia_semana = fecha.strftime("%A").upper()

            mapa_dias = {
                "MONDAY": Dia.LUNES,
                "TUESDAY": Dia.MARTES,
                "WEDNESDAY": Dia.MIERCOLES,
                "THURSDAY": Dia.JUEVES,
                "FRIDAY": Dia.VIERNES,
                "SATURDAY": Dia.SABADO,
                "SUNDAY": Dia.DOMINGO,
            }

            dia_modelo = mapa_dias[dia_semana]
            dia = Agenda.objects.filter(dia__iexact=dia_modelo, instalacion=instalacion).first()

        # Y después obtenemos las reservas para ese dia del mapa, si es una piscina lo hacemos para cada una de las calles
        if dia:
            if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
                calles = []

                for calle in instalacion.calles.all():
                    mapas = dia.mapa_reservas.filter(calle=calle)
                    reservas_serializer = MapaReservasSerializer(mapas, many=True)

                    calles.append({"id": calle.id, "numero": calle.numero, "reservas": reservas_serializer.data})

            else:
                reservas_serializer = MapaReservasSerializer(
                    dia.mapa_reservas.filter(calle__isnull=True),
                    many=True
                )

                calles = None
                reservas = reservas_serializer.data
            
            alquileres_serializer = AlquilerSimpleSerializer(Alquiler.objects.filter(fecha=fecha, instalacion=instalacion).exclude(estado=EstadoReserva.CANCELADO), many=True)
            alquileres = alquileres_serializer.data
            horaApertura = dia.horaApertura
            horaCierre = dia.horaCierre
            abierto = dia.abierto
        else:
            reservas = []
            calles = []
            alquileres = []
            horaApertura = ""
            horaCierre = ""
            abierto = False

        data = {
            "tarifa": {
                "idInstalacion": instalacion.id,
                "nombre": instalacion.nombre,
                "horaApertura": horaApertura,
                "horaCierre": horaCierre,
                "tieneLuz": instalacion.luz,
                "abierto": abierto,
                "datos": precios,
                "reservas": reservas if instalacion.tipoInstalacion != TipoInstalacion.PISCINA else [],
                "calles": calles if instalacion.tipoInstalacion == TipoInstalacion.PISCINA else [],
                "alquileres": alquileres,
                "numeroCalles": instalacion.numeroCalles
            },
            "descuento": {
                "porcentaje_total": 0,
                "aplicados": []
            }
        }

        descuentos = Descuento.obtenerDescuentos(instalacion=instalacion)
        if descuentos:
            data["descuento"]["porcentaje_total"] = descuentos["porcentaje_total"]
            for d in descuentos["descuentos"]:
                data["descuento"]["aplicados"].append({
                    "id": d.id,
                    "nombre": d.nombre,
                    "porcentaje": d.porcentaje
                })

        return Response(data)


class ReservasPorDiaView(APIView):
    permission_classes = [AllowAny]

    def esta_ocupado(self, intervalo, alquiler):
        return (
            intervalo.horaInicio >= alquiler.horaInicio and
            intervalo.horaFin <= alquiler.horaFin
        )

    def generar_slots(self, queryset_mapas, alquileres, calle=None):
        resultado = []

        for intervalo in queryset_mapas:
            estado = "Libre"
            pagada = False

            for alquiler in alquileres:
                if calle and alquiler.calle != calle:
                    continue

                if self.esta_ocupado(intervalo, alquiler):
                    estado = "Reservado"
                    pagada = alquiler.estado == EstadoReserva.CONFIRMADA
                    break

            resultado.append({
                "horaInicio": intervalo.horaInicio.strftime("%H:%M"),
                "horaFin": intervalo.horaFin.strftime("%H:%M"),
                "estado": estado,
                "pagada": pagada
            })

        return resultado


    def get(self, request, instalacion_id):
        instalacion = get_object_or_404(Instalacion, id=instalacion_id)

        fecha_str = request.query_params.get('fecha')
        fecha = parse_date(fecha_str) if fecha_str else date.today()

        agenda_fecha = Agenda.objects.filter(
            fecha=fecha,
            instalacion=instalacion
        ).first()

        # Obtener agenda del día
        if agenda_fecha:
            dia = agenda_fecha
        else:
            dia_semana = fecha.strftime("%A").upper()

            mapa_dias = {
                "MONDAY": Dia.LUNES,
                "TUESDAY": Dia.MARTES,
                "WEDNESDAY": Dia.MIERCOLES,
                "THURSDAY": Dia.JUEVES,
                "FRIDAY": Dia.VIERNES,
                "SATURDAY": Dia.SABADO,
                "SUNDAY": Dia.DOMINGO,
            }

            dia_modelo = mapa_dias[dia_semana]

            dia = Agenda.objects.filter(
                dia__iexact=dia_modelo,
                instalacion=instalacion
            ).first()

        if not dia or not dia.abierto:
            return Response({
                "abierto": False,
                "slots": [],
                "calles": []
            })

        alquileres = Alquiler.objects.filter(
            fecha=fecha,
            instalacion=instalacion
        ).exclude(estado=EstadoReserva.CANCELADO)

        if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
            calles = []

            for calle in instalacion.calles.all():
                mapas = dia.mapa_reservas.filter(calle=calle)

                calles.append({
                    "id": calle.id,
                    "numero": calle.numero,
                    "slots": self.generar_slots(mapas, alquileres, calle)
                })

            data = {
                "abierto": True,
                "horaApertura": dia.horaApertura,
                "horaCierre": dia.horaCierre,
                "calles": calles,
                "numeroCalles": instalacion.numeroCalles
            }
        else:
            mapas = dia.mapa_reservas.filter(calle__isnull=True)

            data = {
                "abierto": True,
                "horaApertura": dia.horaApertura,
                "horaCierre": dia.horaCierre,
                "slots": self.generar_slots(mapas, alquileres),
                "numeroCalles": 0
            }

        return Response(data)


class GestionUsuariosView(APIView):
    permission_classes = [IsAdministradorUsuarios]

    def get(self, request):
        usuariosFinales = UsuarioFinal.objects.all().order_by('nombre')
        serializerUser = UsuarioFinalSimpleSerializer(usuariosFinales, many=True)

        monitores = Monitor.objects.all().order_by('nombre')
        serializerMonitores = MonitorSimpleSerializer(monitores, many=True)
        
        administradores = Administrador.objects.all().order_by('rol')
        serializerAdministradores = AdministradorSimpleSerializer(administradores, many=True)

        data = {
            "usuariosFinales": serializerUser.data,
            "monitores": serializerMonitores.data,
            "administradores": serializerAdministradores.data
        }

        return Response(data)


class GestionEspaciosView(APIView):
    permission_classes = [IsAdministradorEspacios]

    def get(self, request):
        pabellones = Pabellon.objects.all().order_by('nombre')
        serializerPabellon = PabellonSimpleSerializer(pabellones, many=True)

        instalaciones = Instalacion.objects.all().order_by('nombre')
        serializerInstalaciones = InstalacionSimpleSerializer(instalaciones, many=True)

        data = {
            "pabellones": serializerPabellon.data,
            "instalaciones": serializerInstalaciones.data
        }

        return Response(data)
    

class GestionTarifasView(APIView):
    permission_classes = [IsAdministradorTarifas]

    def get(self, request):
        tarifasInstalacion = TarifaInstalacion.objects.all().order_by('titulo')
        serializerTarInst = TarifaInstalacionSimpleSerializer(tarifasInstalacion, many=True)

        tarifasTDA = TarifaTDA.objects.all().order_by('titulo')
        serializerTarTDA = TarifaTDASimpleSerializer(tarifasTDA, many=True)
        
        tarifaActividadComun = ActividadComun.objects.all().order_by('titulo')
        serializerTarActCom = ActividadComunSimpleSerializer(tarifaActividadComun, many=True)
        
        tarifasGrupoReducido = GrupoReducido.objects.all().order_by('titulo')
        serializerTarGruRed = GrupoReducidoSimpleSerializer(tarifasGrupoReducido, many=True)

        tarifasFisio = Fisioterapia.objects.all().order_by('titulo')
        serializerTarFisio = FisioterapiaSimpleSerializer(tarifasFisio, many=True)

        data = {
            "tarifasInstalacion": serializerTarInst.data,
            "tarifasTDA": serializerTarTDA.data,
            "tarifasActividadComun": serializerTarActCom.data,
            "tarifasActividadComun": serializerTarActCom.data,
            "tarifasGrupoReducido": serializerTarGruRed.data,
            "tarifasFisioterapia": serializerTarFisio.data
        }

        return Response(data)

# Obtener configuracion del sistema
class ObtenerConfiguracionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        configuracion = Configuracion.objects.first()
        serializer = ConfiguracionSerializer(configuracion)
        return Response(serializer.data)

    def patch(self, request):
        configuracion = Configuracion.objects.first()

        resultado = configuracion.editar(request.data)
    
        if resultado:
            return Response({"respuesta": "Resultados cambiados correctamente"}, status=status.HTTP_200_OK)
        
        return Response({"respuesta": "Error al modificar la configuracion"}, status=status.HTTP_400_BAD_REQUEST)


class PasarListaEsperaView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)

        posicion = actividad.pasarAEspera(request.user.usuario_final)

        if not posicion:
            return Response({"respuesta": "El usuario ya esta inscrito en la lista de espera"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"respuesta": "Entrada correcta en la lista de espera", "posicion": posicion}, status=status.HTTP_200_OK)
    
    def delete(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)

        print(actividad)
        respuesta = actividad.salirListaEspera(request.user.usuario_final)

        if not respuesta:
            return Response({"respuesta": "Error, no se ha podido salir de la lista"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"respuesta": "Salida correcta de la lista de espera"}, status=status.HTTP_200_OK)


class BonosUsuarioFinalView(APIView):
    permission_classes = [IsAdministradorRaiz | IsAdministradorUsuarios]

    def get(self, request, usuario_id):
        usuarioFinal = get_object_or_404(UsuarioFinal, id=usuario_id)

        bonos = CompraBono.objects.filter(usuarioFinal=usuarioFinal, estado=EstadoReserva.CONFIRMADA)

        return Response(CompraBonoSerializer(bonos, many=True).data)
    
    def post(self, request, usuario_id):
        usuarioFinal = get_object_or_404(UsuarioFinal, id=usuario_id)
        id = request.data.get("bono_id")
        cantidad = int(request.data.get("cantidad"))

        bono = get_object_or_404(CompraBono, id=id, usuarioFinal=usuarioFinal, estado=EstadoReserva.CONFIRMADA)
        if not bono.activo:
            bono.estado = EstadoReserva.CANCELADO
            bono.save()

        bono.vecesUsado += cantidad
        bono.save()

        if bono.usosRestantes <= 0:
            bono.estado = EstadoReserva.CANCELADO
            bono.save()

        return Response({"respuesta": "Operacion exitosa"}, status=status.HTTP_200_OK)


class ReservarActividadView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)
        complementos = request.data.get('complementos')

        formaPago = complementos.get("forma")
        if formaPago == TipoPago.UNICO:
            forma = TipoPago.UNICO
        elif formaPago == TipoPago.MENSUAL:
            forma = TipoPago.MENSUAL
        elif formaPago == TipoPago.CUATRIMESTRAL:
            forma = TipoPago.CUATRIMESTRAL
        else:
            return Response({"respuesta": "No se puede reservar la actividad de esta forma"}, status=status.HTTP_400_BAD_REQUEST)

        res = ReservaActividad.nuevaReserva(request.user.usuario_final, actividad, complementos)
        if not res:
            return Response({"respuesta": "Error al reservar la actividad"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago("Pago por reserva de la actividad", request.user.usuario_final, forma, res, complementos)

        if res and pago:
            return Response({"idPago": pago.id})

        return Response({"respuesta": "Error al reservar"}, status=status.HTTP_400_BAD_REQUEST)


class ReservaInstalacionView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, instalacion_id):
        instalacion = get_object_or_404(Instalacion, id=instalacion_id)
        config = Configuracion.objects.first()

        complementos = request.data.get('complementos')
        fecha_str = complementos.get("fecha")
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        horas = complementos.get("horas")
        calle = complementos.get("calle")
        luz = complementos.get("luz")

        calle_obj = None
        if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
            if not calle:
                return Response({"respuesta": "Debe seleccionar una calle"}, status=status.HTTP_400_BAD_REQUEST)

            calle_obj = instalacion.calles.filter(id=calle).first()
            if not calle_obj:
                return Response({"respuesta": "Calle inválida"}, status=status.HTTP_400_BAD_REQUEST)

        if not horas or len(horas) == 0:
            return Response({"respuesta": "Debe seleccionar horas"}, status=status.HTTP_400_BAD_REQUEST)

        if fecha < timezone.localdate() or fecha > (fecha + timedelta(days=config.dias_maximo_alquiler)):
            return Response({"respuesta": "No se puede reservar en esta fecha"}, status=status.HTTP_400_BAD_REQUEST)

        horas.sort()
        
        if len(horas) > config.horas_alquiler_consecutivas:
            return Response({"respuesta": f'Solo se pueden reservar máximo {config.horas_alquiler_consecutivas} horas'}, status=status.HTTP_400_BAD_REQUEST)

        for i in range(len(horas) - 1):
            h1 = datetime.strptime(horas[i], "%H:%M:%S")
            h2 = datetime.strptime(horas[i+1], "%H:%M:%S")

            if (h2 - h1) != timedelta(hours=1):
                return Response({"respuesta": "Las horas deben ser consecutivas"}, status=status.HTTP_400_BAD_REQUEST)

        horaInicio = datetime.strptime(horas[0], "%H:%M:%S").time()
        ultima = datetime.strptime(horas[-1], "%H:%M:%S")
        horaFin = (ultima + timedelta(hours=1)).time()

        if fecha == timezone.localdate() and horaInicio <= timezone.localtime().time():
            return Response({"respuesta": "No se puede reservar en horas anteriores a la actual"}, status=status.HTTP_400_BAD_REQUEST)

        res = Alquiler.nuevaReserva(request.user.usuario_final, instalacion, fecha, horaInicio, horaFin, luz, calle_obj)
        if not res:
            return Response({"respuesta": "Error al alquilar, la instalacion esta ocupada"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago("Pago por el alquiler de una instalación", request.user.usuario_final, TipoPago.UNICO, res)

        if res and pago:
            return Response({"idPago": pago.id})

        return Response({"respuesta": "Error al alquilar"}, status=status.HTTP_400_BAD_REQUEST)


# Comprar un abono
class ComprarAbonoView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def post(self, request, abono_id):
        tipoAbono = request.data.get('tipoAbono')
        complementos = request.data.get('complementos')

        if tipoAbono == "abono_deportivo":
            abono = get_object_or_404(AbonoDeportivo, id=abono_id)
        elif tipoAbono == "abono_verano":
            abono = get_object_or_404(AbonoVerano, id=abono_id)

        formaPago = complementos.get("forma")
        familiar = complementos.get("familiar", False)
        if formaPago == TipoPago.UNICO or familiar:
            forma = TipoPago.UNICO
        elif formaPago == TipoPago.MENSUAL:
            forma = TipoPago.MENSUAL
        else:
            return Response({"respuesta": "No se puede comprar el abono de esta forma"}, status=status.HTTP_400_BAD_REQUEST)

        compra = CompraAbono.compraAbono(abono, request.user.usuario_final, tipoAbono)
        if not compra:
            return Response({"respuesta": "Error al comprar el abono"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago(f'Pago por nuevo {tipoAbono}', request.user.usuario_final, forma, compra, complementos)

        if compra and pago:
            return Response({"idPago": pago.id})

        return Response({"respuesta": "Error al comprar el abono"}, status=status.HTTP_400_BAD_REQUEST)
        

# Comprar un bono
class ComprarBonoView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def post(self, request, bono_id):
        bono = get_object_or_404(Bono, id=bono_id)

        compra = CompraBono.compraBono(bono, request.user.usuario_final)
        if not compra:
            return Response({"respuesta": "Error al comprar el bono"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago(f'Pago por nuevo bono', request.user.usuario_final, TipoPago.UNICO, compra)

        if compra and pago:
            return Response({"idPago": pago.id})

        return Response({"respuesta": "Error al comprar el bono"}, status=status.HTTP_400_BAD_REQUEST)


# Comprar una tda
class ComprarTDAView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def post(self, request):
        compra = TDA.compraTDA(request.user.usuario_final)
        if not compra:
            return Response({"respuesta": "Error al comprar la TDA"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago(f'Pago por nueva TDA', request.user.usuario_final, TipoPago.UNICO, compra)
        if compra and pago:
            return Response({"idPago": pago.id})

        return Response({"respuesta": "Error al realizar la compra de la TDA"}, status=status.HTTP_400_BAD_REQUEST)


class ResumenPagoView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def get(self, request, tipo, pago_id):
        # Obtenemos el pago
        pago = get_object_or_404(Pago, id=pago_id, usuarioFinal=request.user.usuario_final)
        objeto = pago.objeto

        if tipo == "reserva_actividad":
            reserva = objeto  # objeto es una ReservaActividad
            return Response({
                "id": reserva.id,
                "estado": reserva.estado,
                "nombre": reserva.actividad.nombre,
                "tipo": "mensual",
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
                    "descripcionPorcentajes": pago.descripcionPorcentajes,
                    "fecha": pago.fecha,
                    "estadoPago": pago.estadoPago
                }
            })

        elif tipo == "alquiler_instalacion":
            alquiler = objeto  # objeto es un alquiler
            return Response({
                "id": alquiler.id,
                "estado": alquiler.estado,
                "nombre": alquiler.instalacion.nombre,
                "tipo": "unico",
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
                    "descripcionPorcentajes": pago.descripcionPorcentajes,
                    "fecha": pago.fecha,
                    "estadoPago": pago.estadoPago
                }
            })

        elif tipo == "comprar_abono":
            compra = objeto  # objeto es una CompraAbono
            abono = compra.abonoDeportivo or compra.abonoVerano
            return Response({
                "id": compra.id,
                "estado": compra.estado,
                "nombre": abono.nombre,
                "tipo": "mensual",
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
                    "descripcionPorcentajes": pago.descripcionPorcentajes,
                    "fecha": pago.fecha,
                    "estadoPago": pago.estadoPago
                }
            })

        elif tipo == "comprar_bono":
            compra = objeto  # objeto es una CompraBono
            return Response({
                "id": compra.id,
                "estado": compra.estado,

                "nombre": f'Bono para {compra.bono.instalacion.nombre}',
                "tipo": "unico",
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
                    "descripcionPorcentajes": pago.descripcionPorcentajes,
                    "fecha": pago.fecha,
                    "estadoPago": pago.estadoPago
                }
            })
        
        elif tipo == "comprar_tda":
            compra = objeto  # objeto es una TDA
            return Response({
                "id": compra.id,
                "estado": compra.estado,
                "nombre": f'TDA',
                "tipo": "anual",
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
                    "descripcionPorcentajes": pago.descripcionPorcentajes,
                    "fecha": pago.fecha,
                    "estadoPago": pago.estadoPago
                }
            })

        else:
            return Response({"respuesta": "Tipo no soportado"}, status=status.HTTP_400_BAD_REQUEST)


stripe.api_key = settings.STRIPE_SECRET_KEY

# Realizar un intento de pago
class CrearIntentoPagoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, pago_id):
        pago = get_object_or_404(Pago, id=pago_id)

        if pago.estadoPago != EstadoPago.PENDIENTE:
            return Response({"respuesta": "Pago incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

        if pago.tipoPago == TipoPago.UNICO:
            intent = pago.aplicarPagoUnico(request.user.usuario_final)

            client_secret = intent.client_secret
        else:
            usuario = request.user.usuario_final
            subscription = pago.aplicarSubscripcion(usuario)

            if not subscription:
                return Response({"respuesta": "Tipo de subscripcion invalida"}, status=status.HTTP_400_BAD_REQUEST)

            client_secret = subscription.latest_invoice.confirmation_secret.client_secret

        return Response({
            "client_secret": client_secret
        })


# Confirmar un pago
class ConfirmarPagoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, pago_id):
        pago = get_object_or_404(Pago, id=pago_id)

        estado = pago.comprobarPago()
        if estado:
            pago.confirmarPago()
            return Response({"respuesta": "Pago completado con exito"}, status=status.HTTP_200_OK)
        else:
            pago.cancelarPago()
            return Response({"respuesta": "Error al pagar"}, status=status.HTTP_400_BAD_REQUEST)


# Cancelar un pago
class CancelarPagoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, pago_id):
        pago = get_object_or_404(Pago, id=pago_id)

        if pago.estadoPago != EstadoPago.CANCELADO:
            pago.cancelarPago("")

        return Response({"respuesta": "Pago cancelado correctamente"}, status=status.HTTP_200_OK)


from django.contrib.contenttypes.models import ContentType
# Cancelar una reserva de actividad
class CancelarReservaActividadView(APIView):
    permission_classes = [IsUsuarioFinal]

    def delete(self, request, reserva_id):
        reserva = get_object_or_404(ReservaActividad, id=reserva_id, usuarioFinal=request.user.usuario_final)

        reserva_ct = ContentType.objects.get_for_model(ReservaActividad)
        pago = Pago.objects.get(content_type=reserva_ct, object_id=reserva.id)

        configuracion = Configuracion.objects.first()

        hoy = timezone.now()

        if hoy.month == 12:
            siguiente_mes = datetime(hoy.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            siguiente_mes = datetime(hoy.year, hoy.month + 1, 1, tzinfo=timezone.utc)

        fecha_limite = siguiente_mes - timedelta(days=configuracion.dias_minimo_cancelacion)

        if hoy < fecha_limite:
            return Response(
                {"respuesta": "El plazo de cancelación para el próximo mes ha finalizado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pago.cancelarPago("subscripcion")
        reserva.delete()

        return Response({"respuesta": "Reserva cancelada correctamente"}, status=200)


# Cancelar un alquiler
class CancelarAlquilerView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def delete(self, request, alquiler_id):
        alquiler = get_object_or_404(Alquiler, id=alquiler_id)

        alquiler_ct = ContentType.objects.get_for_model(Alquiler)
        pago = Pago.objects.get(content_type=alquiler_ct, object_id=alquiler.id)

        ahora = timezone.localtime()

        fecha_alquiler = alquiler.fecha
        horaInicio = alquiler.horaInicio

        inicio_alquiler = datetime.combine(fecha_alquiler, horaInicio)
        inicio_alquiler = timezone.make_aware(inicio_alquiler)

        if inicio_alquiler <= ahora:
            return Response({"respuesta": "No se puede cancelar un alquiler ya iniciado"}, status=status.HTTP_400_BAD_REQUEST)

        if pago.estadoPago == EstadoPago.PAGADO:
            try:
                pago.cancelarPago("unico")
                alquiler.delete()
            except stripe.error.StripeError as e:
                print("Error en el refund:", str(e))
                return Response(
                    {"error": "No se pudo procesar el reembolso"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response({"respuesta": "Alquiler eliminado"}, status=status.HTTP_200_OK)


# Cancelar un abono
class CancelarAbonoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def delete(self, request, compra_id):
        compra = get_object_or_404(CompraAbono, id=compra_id)
        
        compra_ct = ContentType.objects.get_for_model(CompraAbono)
        pago = Pago.objects.get(content_type=compra_ct, object_id=compra.id)

        pago.cancelarPago("subscripcion")
        compra.delete()

        return Response({"respuesta": "Compra de abono eliminada"}, status=200)


# Cancelar un abono
class CancelarBonoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def delete(self, request, compra_id):
        compra = get_object_or_404(CompraBono, id=compra_id)

        compra_ct = ContentType.objects.get_for_model(CompraBono)
        pago = Pago.objects.get(content_type=compra_ct, object_id=compra.id)

        if pago.estadoPago == EstadoPago.PAGADO and compra.vecesUsado == 0:
            pago.cancelarPago("unico")
            compra.delete()

        return Response({"respuesta": "Compra de bono eliminada"}, status=status.HTTP_200_OK)


class StripeWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'invoice.payment_failed':
            invoice = event['data']['object']
            subscription_id = invoice['subscription']
            try:
                pago = Pago.objects.get(stripe_subscription_id=subscription_id)
                Notificacion.notificarProblemasPago(pago.usuarioFinal)

                pago.cancelarPago("subscripcion")
            except Pago.DoesNotExist:
                pass

        return Response(status=status.HTTP_200_OK)

# Obtener estadisticas para el admin
class ObtenerEstadisticasAdministradorView(APIView):
    permission_classes = [IsAdministrador]

    def get(self, request):
        hoy = now()

        mes = request.query_params.get("mes")
        anio = request.query_params.get("anio")
        actividad_id = request.query_params.get("actividad_id")

        mes = int(mes) if mes else hoy.month
        anio = int(anio) if anio else hoy.year

        reservas_qs = ReservaActividad.objects.filter(
            created_at__year=anio,
            created_at__month=mes,
            estado=EstadoReserva.CONFIRMADA
        )

        alquiler_qs = Alquiler.objects.filter(
            created_at__year=anio,
            created_at__month=mes
        )

        pagos_qs = Pago.objects.filter(
            fecha__year=anio,
            fecha__month=mes,
            estadoPago=EstadoPago.PAGADO
        )

        if actividad_id:
            reservas_qs = reservas_qs.filter(actividad_id=actividad_id)
            reservas_ids = ReservaActividad.objects.filter(actividad_id=actividad_id).values_list("id", flat=True)
            ct_reserva = ContentType.objects.get_for_model(ReservaActividad)
            pagos_qs = pagos_qs.filter(content_type=ct_reserva, object_id__in=reservas_ids)

        reservas_mes = alquiler_qs.count()
        inscripciones = reservas_qs.count()

        ingresos_mes = pagos_qs.aggregate(
            total=Sum("costeFinal")
        )["total"] or 0

        content_types_map = {
            ct.id: ct.model
            for ct in ContentType.objects.all()
        }

        MAPEO_TIPOS = {
            "reservaactividad": "actividad",
            "alquiler": "instalacion",
            "compraabono": "abono",
            "comprabono": "bono",
            "tda": "tda",
        }

        ingresos_por_tipo = pagos_qs.values("content_type").annotate(
            total=Sum("costeFinal")
        )

        ingresos_detallados = {}
        for item in ingresos_por_tipo:
            ct_id = item["content_type"]
            total = item["total"] or 0

            modelo = content_types_map.get(ct_id)
            tipo = MAPEO_TIPOS.get(modelo, "otros")

            ingresos_detallados[tipo] = ingresos_detallados.get(tipo, 0) + total

        reservas_12_meses = (
            ReservaActividad.objects
            .filter(created_at__gte=hoy - timedelta(days=365))
            .filter(estado=EstadoReserva.CONFIRMADA)
            .annotate(mes=TruncMonth("created_at"))
            .values("mes")
            .annotate(total=Count("id"))
            .order_by("mes")
        )

        reservas_por_mes = [
            {
                "mes": r["mes"].strftime("%Y-%m"),
                "total": r["total"]
            }
            for r in reservas_12_meses
        ]

        actividades_top = (
            reservas_qs
            .values("actividad__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )

        actividades_mas_reservadas = [
            {
                "actividad": a["actividad__nombre"],
                "total": a["total"]
            }
            for a in actividades_top
        ]

        uso_pabellones = []
        for inst in Instalacion.objects.all():
            horas = Alquiler.objects.filter(instalacion=inst).count()
            horas_disponibles = 30 * 24
            ocupacion = min(round((horas / horas_disponibles) * 100, 1), 100)

            uso_pabellones.append({
                "nombre": inst.nombre,
                "horas": horas,
                "ocupacion": ocupacion
            })

        # Número de inscripciones activas por actividad
        inscripciones_actividad = (
            reservas_qs
            .values("actividad__nombre")
            .annotate(inscritos=Count("usuarioFinal", distinct=True))
            .order_by("-inscritos")
        )

        inscripciones_por_actividad = [
            {
                "actividad": i["actividad__nombre"],
                "inscritos": i["inscritos"]
            }
            for i in inscripciones_actividad
        ]

        data = {
            "instalaciones": Instalacion.contar(),
            "actividades": Actividad.contar(),
            "sesiones": Sesion.contar(),
            "pabellones": Pabellon.contar(),
            "deportes": Deporte.contar(),
            "usuarios": UsuarioFinal.contar(),
            "monitores": Monitor.contar(),

            "inscripciones": inscripciones,
            "reservas_mes": reservas_mes,
            "ingresos_mes": ingresos_mes,

            "ingresos_detallados": ingresos_detallados,
            "reservas_12_meses": reservas_por_mes,
            "actividades_top": actividades_mas_reservadas,
            "uso_pabellones": uso_pabellones,
            "inscripciones_por_actividad": inscripciones_por_actividad,
        }

        return Response(data)


class ObtenerEstadisticasUsuarioFinalView(APIView):
    permission_classes = [IsUsuarioFinal]

    def get(self, request):
        usuario = request.user.usuario_final
        hoy = now()

        # RESERVAS TOTALES
        reservas_totales = ReservaActividad.objects.filter(
            usuarioFinal=usuario
        ).exclude(estado=EstadoReserva.CANCELADO).count()

        # RESERVAS ESTE MES
        reservas_mes = ReservaActividad.objects.filter(
            usuarioFinal=usuario,
            created_at__year=hoy.year,
            created_at__month=hoy.month
        ).exclude(estado=EstadoReserva.CANCELADO).count()

        # CANCELACIONES
        cancelaciones = ReservaActividad.objects.filter(
            usuarioFinal=usuario,
            estado=EstadoReserva.CANCELADO
        ).count()

        # DINERO GASTADO
        dinero_total = Pago.objects.filter(
            usuarioFinal=usuario,
            estadoPago=EstadoPago.PAGADO
        ).aggregate(total=Sum("costeFinal"))["total"] or 0


        # RESERVAS POR MES (12 MESES)
        reservas_12_meses = (
            ReservaActividad.objects
            .filter(
                usuarioFinal=usuario,
                created_at__gte=hoy - timedelta(days=365),
                estado=EstadoReserva.CONFIRMADA
            )
            .annotate(mes=TruncMonth("created_at"))
            .values("mes")
            .annotate(total=Count("id"))
            .order_by("mes")
        )

        reservas_labels = []
        reservas_data = []

        for r in reservas_12_meses:
            reservas_labels.append(r["mes"].strftime("%b"))
            reservas_data.append(r["total"])


        # ACTIVIDADES MÁS RESERVADAS POR EL USUARIO
        actividades_top = (
            ReservaActividad.objects
            .filter(usuarioFinal=usuario, estado=EstadoReserva.CONFIRMADA)
            .values("actividad__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )

        actividades_labels = []
        actividades_data = []

        for a in actividades_top:
            actividades_labels.append(a["actividad__nombre"])
            actividades_data.append(a["total"])


        # ACTIVIDAD FAVORITA
        actividad_favorita = (
            ReservaActividad.objects
            .filter(usuarioFinal=usuario, estado=EstadoReserva.CONFIRMADA)
            .values("actividad__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )

        actividad_favorita = actividad_favorita["actividad__nombre"] if actividad_favorita else "-"


        # INSTALACION FAVORITA
        instalacion_favorita = (
            ReservaActividad.objects
            .filter(usuarioFinal=usuario, estado=EstadoReserva.CONFIRMADA)
            .values("actividad__instalacion__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )

        instalacion_favorita = instalacion_favorita["actividad__instalacion__nombre"] if instalacion_favorita else "-"


        # RESERVAS POR DÍA DE LA SEMANA
        reservas_por_dia_qs = (
            ReservaActividad.objects
            .filter(usuarioFinal=usuario, estado=EstadoReserva.CONFIRMADA)
            .annotate(dia=ExtractWeekDay("created_at"))
            .values("dia")
            .annotate(total=Count("id"))
        )

        dias_labels = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
        dias_data = [0] * 7

        for r in reservas_por_dia_qs:
            dia = r["dia"]

            # Forzamos a lunes, martes, ..., domingo
            if dia == 1:
                indice = 6
            else:
                indice = dia - 2

            dias_data[indice] = r["total"]

        data = {
            "reservas_totales": reservas_totales,
            "reservas_mes": reservas_mes,
            "cancelaciones": cancelaciones,
            "dinero_total": dinero_total,

            "actividad_favorita": actividad_favorita,
            "instalacion_favorita": instalacion_favorita,

            "reservas_por_mes": {
                "labels": reservas_labels,
                "data": reservas_data
            },

            "actividades_usuario": {
                "labels": actividades_labels,
                "data": actividades_data
            },

            "reservas_por_dia": {
                "labels": dias_labels,
                "data": dias_data
            }
        }

        return Response(data)


class DescargarHorarioView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, instalacion_id):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="horarios_instalacion_{instalacion_id}.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()

        elements.append(Paragraph("Horarios de la instalación", styles['Title']))
        elements.append(Spacer(1, 12))

        agendas = Agenda.objects.filter(instalacion_id=instalacion_id).annotate(
            orden_dia=Case(
                When(dia='Lunes', then=1),
                When(dia='Martes', then=2),
                When(dia='Miercoles', then=3),
                When(dia='Jueves', then=4),
                When(dia='Viernes', then=5),
                When(dia='Sabado', then=6),
                When(dia='Domingo', then=7),
                default=8,
                output_field=IntegerField()
            )
            ).order_by('orden_dia', 'fecha')

        data = [["Día / Fecha", "Estado", "Apertura", "Cierre"]]

        for agenda in agendas:
            if agenda.dia:
                nombre = agenda.dia
            else:
                nombre = str(agenda.fecha)

            estado = "Abierto" if agenda.abierto else "Cerrado"

            apertura = agenda.horaApertura.strftime("%H:%M") if agenda.abierto else "-"
            cierre = agenda.horaCierre.strftime("%H:%M") if agenda.abierto else "-"

            data.append([nombre, estado, apertura, cierre])

        table = Table(data)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)

        doc.build(elements)
        return response
    

class DescargarHorarioSesionesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, actividad_id):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="horarios_actividad_{actividad_id}.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()

        elements.append(Paragraph("Horario de la actividad", styles['Title']))
        elements.append(Spacer(1, 12))

        actividad = get_object_or_404(Actividad, id=actividad_id)
        sesiones = actividad.sesiones.all()

        data = [["Día", "Hora inicio", "Hora fin"]]

        for sesion in sesiones:
            nombre = sesion.dia

            horaInicio = sesion.horaInicio.strftime("%H:%M")
            horaFin = sesion.horaFin.strftime("%H:%M")

            data.append([nombre, horaInicio, horaFin])

        table = Table(data)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)

        doc.build(elements)
        return response