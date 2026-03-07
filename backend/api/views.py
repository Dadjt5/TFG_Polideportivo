from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework import status
import stripe
from django.utils.dateparse import parse_date
from datetime import date
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models.deletion import RestrictedError
from django.conf import settings
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.db.models.functions import TruncMonth, ExtractWeekDay
from datetime import timedelta, datetime
from django.utils import timezone

from .permissions import IsAdministradorRaiz, IsAdministradorEspacios, IsAdministradorTarifas, IsAdministradorUsuarios, IsMonitor, IsUsuarioFinal, IsAdministrador, IsSuperUser

from .serializers import (
    AbonoDeportivoSerializer, AbonoVeranoSerializer, BonoSerializer,
    ActividadSerializer, AsistenciaSerializer, AgendaSerializer,
    ConfiguracionSerializer, DeporteSerializer, DescuentoSerializer,
    FavoritoSerializer, ForoSerializer, CanalUsuarioFinalSerializer,
    HorarioSerializer, InstalacionSerializer, PabellonSerializer, ListaEsperaSerializer,
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
    AlquilerSimpleSerializer, FeedbackSerializer
)

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, User, CompraBono, CompraAbono,
    Mensaje, Sesion, MapaReservas, TipoActividad, TipoInstalacion, FormaReserva,
    Terreno, Estado, Dia, ActividadComun, GrupoReducido, Fisioterapia, EstadoPago,
    EstadoReserva, Periodo, Feedback
)


# ----------------
# Feedback
# ----------------

class FeedbackViewSet(viewsets.ModelViewSet):

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsSuperUser]
        elif self.action == "create":
            return [IsAuthenticated]
        else:
            return [IsSuperUser]

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
    
    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

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
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return Favorito.objects.filter(usuarioFinal__user=self.request.user)


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
    authentication_classes = []


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
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return TDA.objects.filter(usuarioFinal__user=self.request.user)


# ----------------
# Usuarios finales
# ----------------

class UsuarioFinalViewSet(viewsets.ModelViewSet):
    queryset = UsuarioFinal.objects.all()
    serializer_class = UsuarioFinalSerializer
    permission_classes = [IsAuthenticated]

# ----------------
# Administradores
# ----------------

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]


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
            "is_monitor": user.is_monitor,
            "is_usuario_final": user.is_usuario_final,
            "is_administrador": user.is_administrador,
            "is_superuser": user.is_superuser
        }

        if user.is_usuario_final:
            data["usuario_final_id"] = user.usuario_final.id
        else:
            data["usuario_final_id"] = None

        if user.is_monitor:
            data["monitor_id"] = user.monitor.id
        else:
            data["monitor_id"] = None

        if user.is_administrador:
            data["administrador_id"] = user.administrador.id
            data["rol"] = user.administrador.rol
        else:
            data["administrador_id"] = None

        return Response(data)


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
            "tiposActividad": TipoActividad.choices,
            "tiposInstalacion": TipoInstalacion.choices,
            "tiposDeporte": deportes
        }

        return Response(data)


# Informacion con los tipos de cada grupo necesario: reservas, actividades, terrenos, etc
class TiposViews(APIView):
    permission_classes = [IsAdministrador]

    def get(self, request):
        data = {
            "tiposActividad": TipoActividad.choices,
            "tiposInstalacion": TipoInstalacion.choices,
            "tiposReserva": FormaReserva.choices,
            "terrenos": Terreno.choices,
            "estados": Estado.choices,
            "dias": Dia.choices,
            "periodos": Periodo.choices
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

        instalaciones = Instalacion.buscar(nombre,tiposInstalacion,horaApertura,horaCierre)
        actividades = Actividad.buscar(nombre,tiposActividad,horaInicioSesion,horaFinSesion,dias)

        data = {
            "instalaciones": InstalacionSerializer(instalaciones, many=True).data,
            "actividades": ActividadSerializer(actividades, many=True).data,
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
        cuentaBancaria = request.data.get('cuentaBancaria')

        respuesta = UsuarioFinal.registrar_usuario(
            nombre=nombre, apellidos=apellidos, sexo=sexo, fechaNacimiento=fechaNacimiento,
            dni=dni, telefono=telefono, email=email, provincia=provincia,
            municipio=municipio, localidad=localidad, codigoPostal=codigoPostal,
            password=password, cuentaBancaria=cuentaBancaria
        )

        if respuesta["error"]:
            return Response({"mensaje": respuesta["respuesta"]}, status=status.HTTP_400_BAD_REQUEST)

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

        respuesta = Monitor.registrar_monitor(
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

        respuesta = Administrador.registrar_administrador(
            nombre=nombre, rol=rol, dni=dni, 
            email=email, password=password
        )

        if respuesta["error"]:
            sta = status.HTTP_400_BAD_REQUEST
        else:
            sta = status.HTTP_201_CREATED

        return Response(
            {"respuesta": respuesta["respuesta"]},
            status=sta
        )


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


# Guardar informacion de notificaciones
class GuardarNotificacionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notificaciones = request.data.get('notificaciones', [])

        for n in notificaciones:
            Notificacion.cambiar_estado(
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

        tdas_libres = TDA.objects.filter(usuarioFinal__isnull=True)

        for tda in tdas_libres:
            if tda.comprobar_codigo_secreto(codigo) or tda.codigo_secreto == codigo:
                tda.asignar_usuario(request.user.usuario_final)
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
            hora_inicio = sesion.get('horaInicio')
            hora_fin = sesion.get('horaFin')
            
            respuesta = instalacion.controlarHorarioActividad(dia, hora_inicio, hora_fin)
            if not respuesta:
                return Response({"respuesta": "Una o más sesiones no se pueden realizar en esta instalación en el horario previsto"}, status=status.HTTP_400_BAD_REQUEST)

            respuesta = actividad.nuevaSesion(dia, hora_inicio, hora_fin)

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

        alquileres = Alquiler.objects.filter(usuarioFinal__user=user, estado=EstadoReserva.CONFIRMADA)
        actividades = ReservaActividad.objects.filter(usuarioFinal__user=user, estado=EstadoReserva.CONFIRMADA)

        for alquiler in alquileres:
            serializer = AlquilerSerializer(alquiler)
            reservas.append(serializer.data)

        for reserva in actividades:
            serializer = ReservaActividadSerializer(reserva)
            reservas.append(serializer.data)

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
            if actividad.activa:
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
            "actividad": {
                "nombre": actividad.nombre,
                "periodo": actividad.periodo,
                "estado": actividad.estado,
                "instalacion": {
                    "id": actividad.instalacion.id,
                    "nombre": actividad.instalacion.nombre
                },
                "nivel": actividad.nivel
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
        try:
            # Datos de la instalacion
            instalacion_data = request.data.get("instalacion", {})

            pabellon_id = instalacion_data.pop("pabellon", None)
            tarifa_id = instalacion_data.pop("tarifa", None)

            pabellon = get_object_or_404(Pabellon, id=pabellon_id)
            tarifa = get_object_or_404(TarifaInstalacion, id=tarifa_id)

            instalacion = Instalacion.objects.create(**instalacion_data, pabellon=pabellon, tarifa=tarifa)

            # Crear y manejar la agenda y fechas especiales
            agenda = request.data.get('agenda', [])
            fechasEspeciales = request.data.get('fechasEspeciales', [])

            for fecha in agenda:
                res = instalacion.controlarCambioHorario(fecha["dia"], fecha.get("apertura"), fecha.get("cierre"))
                if not res:
                    return Response({"respuesta": "Error, el cambio no esta permitido debido a que hay sesiones en esas horas"}, status=status.HTTP_400_BAD_REQUEST)

                res = instalacion.nuevoHorario(fecha["dia"], fecha.get("apertura"), fecha.get("cierre"), fecha.get("abierto", True))
                if not res:
                    return Response({"respuesta": "Error al actualizar la agenda de los dias de la semana"}, status=status.HTTP_400_BAD_REQUEST)

            for fecha in fechasEspeciales:
                instalacion.nuevoHorarioEspecial(fecha["fecha"], fecha.get("apertura"), fecha.get("cierre"), fecha.get("abierto", True))

                if not res:
                    return Response({"respuesta": "Error al actualizar la agenda de los dias especiales"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"respuesta": "Exito al asignar la agenda a la instalacion"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"respuesta": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class EditarInstalacionView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request, instalacion_id):
        try:
            instalacion = get_object_or_404(Instalacion, id=instalacion_id)

            # Datos de la instalacion
            instalacion_data = request.data.get("instalacion", {})

            pabellon_id = instalacion_data.pop("pabellon", None)            
            tarifa_id = instalacion_data.pop("tarifa", None)            

            pabellon = get_object_or_404(Pabellon, id=pabellon_id)
            tarifa = get_object_or_404(TarifaInstalacion, id=tarifa_id)

            # Manejar la agenda y fechas especiales
            agenda = request.data.get('agenda', [])
            fechasEspeciales = request.data.get('fechasEspeciales', [])

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

                apertura = item.get("apertura")
                cierre = item.get("cierre")
                abierto = item.get("abierto", True)

                agenda_existente = agendas_existentes.get(dia)

                if agenda_existente:
                    # Validar conflicto antes
                    if not instalacion.controlarCambioHorario(dia, apertura, cierre, abierto):
                        return Response(
                            {"respuesta": f"No se puede modificar el día {dia} por conflictos existentes"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    agenda_existente.horaApertura = apertura
                    agenda_existente.horaCierre = cierre
                    agenda_existente.abierto = abierto
                    agenda_existente.save()
                else:
                    if not instalacion.nuevoHorario(dia, apertura, cierre, abierto):
                        return Response(
                            {"respuesta": f"Error creando horario para {dia}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Eliminar los que ya no vienen
            for dia, agenda in agendas_existentes.items():
                if dia not in dias_recibidos:
                    agenda.delete()

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

                apertura = item.get("apertura")
                cierre = item.get("cierre")
                abierto = item.get("abierto", True)

                especial_existente = especiales_existentes.get(str(fecha))

                if especial_existente:
                    if not instalacion.controlarCambioHorario(fecha, apertura, cierre, abierto):
                        return Response(
                            {"respuesta": f"No se puede modificar la fecha {fecha} por conflictos existentes"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    especial_existente.horaApertura = apertura
                    especial_existente.horaCierre = cierre
                    especial_existente.abierto = abierto
                    especial_existente.save()
                else:
                    if not instalacion.nuevoHorarioEspecial(fecha, apertura, cierre, abierto):
                        return Response(
                            {"respuesta": f"Error creando horario especial {fecha}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Eliminar especiales que ya no vienen
            for fecha, agenda in especiales_existentes.items():
                if fecha not in fechas_recibidas:
                    agenda.delete()

            instalacion.modificarInformacion(instalacion_data, pabellon, tarifa)
            return Response({"respuesta": "Exito al asignar la agenda a la instalacion"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"respuesta": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NuevaActividadView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request):
        try:
            # Datos de la actividad
            actividad_data = request.data.get("actividad", {})
            
            tarifa_id = actividad_data.pop("tarifa", None)
            instalacion_id = actividad_data.pop("instalacion", None)
            monitor_id = actividad_data.pop("monitor", None)
            
            tarifa = get_object_or_404(TarifaActividad, id=tarifa_id)
            instalacion = get_object_or_404(Instalacion, id=instalacion_id)
            monitor = get_object_or_404(Monitor, id=monitor_id)

            actividad = Actividad.objects.create(**actividad_data, tarifa=tarifa, instalacion=instalacion, monitor=monitor)
            ListaEspera.objects.create(actividad=actividad)

            # Sesiones de la actividad
            sesiones = request.data.get("sesiones", [])

            for sesion in sesiones:
                dia = sesion.get('dia')
                hora_inicio = sesion.get('horaInicio')
                hora_fin = sesion.get('horaFin')

                respuesta = instalacion.controlarHorarioActividad(dia, hora_inicio, hora_fin)
                if not respuesta:
                    return Response({"respuesta": "Una o más sesiones no se pueden realizar en esta instalación en el horario elegido"}, status=status.HTTP_400_BAD_REQUEST)

                respuesta = actividad.nuevaSesion(dia, hora_inicio, hora_fin)

                if not respuesta:
                    return Response({"respuesta": "No se ha podido crear ninguna sesión"}, status=status.HTTP_400_BAD_REQUEST)

            # Deporte de la actividad
            nombre = request.data.get("deportes")
            nombre = nombre.strip()
            titulo = nombre.lower().replace(" ", "_")

            deporte, _ = Deporte.objects.get_or_create(titulo=titulo)
            actividad.deportes = deporte
            actividad.save()
            
            Notificacion.notificarNuevaActividad(actividad)

            return Response({"respuesta": "Deporte asignado correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"respuesta": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EditarActividadView(APIView):
    permission_classes = [IsAdministradorEspacios]

    @transaction.atomic
    def post(self, request, actividad_id):
        try:
            actividad = get_object_or_404(Actividad, id=actividad_id)

            actividad_data = request.data.get("actividad", {})

            tarifa_id = actividad_data.pop("tarifa", None)
            instalacion_id = actividad_data.pop("instalacion", None)
            monitor_id = actividad_data.pop("monitor", None)

            tarifa = get_object_or_404(TarifaActividad, id=tarifa_id)
            instalacion = get_object_or_404(Instalacion, id=instalacion_id)
            monitor = get_object_or_404(Monitor, id=monitor_id)
            
            sesiones_recibidas = request.data.get("sesiones", [])

            sesiones_bd = actividad.sesiones.all()
            ids_recibidos = []

            for sesion_data in sesiones_recibidas:
                dia = sesion_data.get('dia')
                hora_inicio = sesion_data.get('horaInicio')
                hora_fin = sesion_data.get('horaFin')
                sesion_id = sesion_data.get('id')

                respuesta = instalacion.controlarHorarioActividad(
                    dia,
                    hora_inicio,
                    hora_fin,
                    sesion_id
                )

                if not respuesta:
                    return Response(
                        {"respuesta": "Una o más sesiones no se pueden realizar en esta instalación en el horario elegido"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if not sesion_id or sesion_id == -1:
                    nueva = actividad.nuevaSesion(dia, hora_inicio, hora_fin)
                    ids_recibidos.append(nueva.id)

                else:
                    sesion_existente = sesiones_bd.filter(id=sesion_id).first()

                    if sesion_existente:
                        sesion_existente.dia = dia
                        sesion_existente.horaInicio = hora_inicio
                        sesion_existente.horaFin = hora_fin
                        sesion_existente.save()

                        ids_recibidos.append(sesion_existente.id)

            for sesion in sesiones_bd:
                if sesion.id not in ids_recibidos:
                    sesion.delete()

            # Nombre del deporte
            nombre = request.data.get("deportes")
            nombre = nombre.strip()
            titulo = nombre.lower().replace(" ", "_")

            deporte, _ = Deporte.objects.get_or_create(titulo=titulo)
            if actividad.deportes != deporte:
                actividad.deportes = deporte

            actividad.modificarInformacion(actividad_data, tarifa, instalacion, monitor)

            return Response({"respuesta": "Deporte asignado correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"respuesta": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TarifaActividadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)

        precios = actividad.obtener_precios()
        data = {
            "tarifa": {
                "idActividad": actividad.id,
                "nombre": actividad.nombre,
                "numeroHoras": actividad.calcularHorasSemanales(),
                "horario": actividad.getHorario(),
                "tipo": actividad.tipoActividad,
                "datos": precios
            },
            "descuento": {
                "porcentaje_total": 0,
                "aplicados": []
            }
        }

        descuentos = Descuento.obtener_descuentos(actividad=actividad)
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

        precios = instalacion.obtener_precios()

        fecha_str = request.query_params.get('fecha')
        if fecha_str:
            fecha = parse_date(fecha_str)
        else:
            fecha = date.today()

        agenda_fecha = Agenda.objects.filter(fecha=fecha).first()

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
            dia = Agenda.objects.filter(dia__iexact=dia_modelo).first()

        if dia:
            reservas_serializer = MapaReservasSerializer(dia.mapa_reservas.all(), many=True)
            reservas = reservas_serializer.data
            alquileres_serializer = AlquilerSimpleSerializer(Alquiler.objects.filter(fecha=fecha), many=True)
            alquileres = alquileres_serializer.data
            horaApertura = dia.horaApertura
            horaCierre = dia.horaCierre
            abierto = dia.abierto
        else:
            reservas = []
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
                "abierto": abierto,
                "datos": precios,
                "reservas": reservas,
                "alquileres": alquileres
            },
            "descuento": {
                "porcentaje_total": 0,
                "aplicados": []
            }
        }

        descuentos = Descuento.obtener_descuentos(instalacion=instalacion)
        if descuentos:
            data["descuento"]["porcentaje_total"] = descuentos["porcentaje_total"]
            for d in descuentos["descuentos"]:
                data["descuento"]["aplicados"].append({
                    "id": d.id,
                    "nombre": d.nombre,
                    "porcentaje": d.porcentaje
                })

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
    permission_classes = [IsAdministradorRaiz]

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


class ReservarActividadView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)
        complementos = request.data.get('complementos')

        res = ReservaActividad.nuevaReserva(request.user.usuario_final, actividad)
        if not res:
            return Response({"respuesta": "Error al reservar la actividad"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago("Pago por reserva de la actividad", request.user.usuario_final, res, complementos)

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

        hora_inicio = datetime.strptime(horas[0], "%H:%M:%S").time()
        ultima = datetime.strptime(horas[-1], "%H:%M:%S")
        hora_fin = (ultima + timedelta(hours=1)).time()

        if fecha == timezone.localdate() and hora_inicio <= timezone.localtime().time():
            return Response({"respuesta": "No se puede reservar en horas anteriores a la actual"}, status=status.HTTP_400_BAD_REQUEST)

        res = Alquiler.nuevaReserva(request.user.usuario_final, instalacion, fecha, hora_inicio, hora_fin)
        if not res:
            return Response({"respuesta": "Error al alquilar, la instalacion esta ocupada"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago("Pago por el alquiler de una instalación", request.user.usuario_final, res)

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

        compra = CompraAbono.compraAbono(abono, request.user.usuario_final, tipoAbono)
        if not compra:
            return Response({"respuesta": "Error al comprar el abono"}, status=status.HTTP_400_BAD_REQUEST)

        pago = Pago.nuevoPago(f'Pago por nuevo {tipoAbono}', request.user.usuario_final, compra, complementos)

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

        pago = Pago.nuevoPago(f'Pago por nuevo bono', request.user.usuario_final, compra)

        if compra and pago:
            return Response({"idPago": pago.id})

        return Response({"respuesta": "Error al comprar el bono"}, status=status.HTTP_400_BAD_REQUEST)


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
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
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
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
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
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
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
                "pago": {
                    "concepto": pago.concepto,
                    "coste": pago.coste,
                    "costeFinal": pago.costeFinal,
                    "descuentoAplicado": pago.descuentoAplicado,
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

        intent = stripe.PaymentIntent.create(
            amount=int(pago.coste * 100), # En centimos
            currency="eur",
            metadata={
                "pago_id": pago.id,
                "usuario_id": request.user.id
            }
        )

        pago.stripe_payment_intent = intent.id
        pago.save()

        return Response({
            "client_secret": intent.client_secret
        })


# Confirmar un pago
class ConfirmarPagoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def post(self, request, pago_id):
        pago = get_object_or_404(Pago, id=pago_id)

        intent = stripe.PaymentIntent.retrieve(pago.stripe_payment_intent)

        if intent.status == "succeeded":
            pago.confirmarPago()
            return Response({"respuesta": "Pago completado con exito"}, status=status.HTTP_200_OK)
        else:
            pago.cancelarPago()
            return Response({"respuesta": "Error al pagar"}, status=status.HTTP_400_BAD_REQUEST)


# Cancelar una reserva de actividad
class CancelarReservaActividadView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def delete(self, request, reserva_id):
        reserva = get_object_or_404(ReservaActividad, id=reserva_id)
        
        reserva.cancelarCompra()
        reserva.delete()
        
        return Response({"respuesta": "Reserva eliminada"}, status=status.HTTP_200_OK)


# Cancelar un alquiler
class CancelarAlquilerView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def delete(self, request, alquiler_id):
        alquiler = get_object_or_404(Alquiler, id=alquiler_id)
        
        alquiler.cancelarCompra()
        alquiler.delete()
        
        return Response({"respuesta": "Alquiler eliminado"}, status=status.HTTP_200_OK)


# Cancelar un abono
class CancelarAbonoView(APIView):
    permission_classes = [IsUsuarioFinal]

    def delete(self, request, compra_id):
        compra = get_object_or_404(CompraAbono, id=compra_id)

        compra.cancelarCompra()
        compra.delete()
        
        return Response({"respuesta": "Compra de abono eliminado"}, status=status.HTTP_200_OK)


# Cancelar un abono
class CancelarBonoView(APIView):
    permission_classes = [IsUsuarioFinal]
    
    def delete(self, request, compra_id):
        compra = get_object_or_404(CompraBono, id=compra_id)
        
        compra.cancelarCompra()
        compra.delete()
        
        return Response({"respuesta": "Compra de bono eliminado"}, status=status.HTTP_200_OK)


# Obtener estadisticas para el admin
class ObtenerEstadisticasAdministradorView(APIView):
    permission_classes = [IsAdministrador]
    
    def get(self, request):
        hoy = now()
        reservas_mes = ReservaActividad.objects.filter(
            created_at__year=hoy.year,
            created_at__month=hoy.month
        ).count()
        
        alquiler_mes = Alquiler.objects.filter(
            created_at__year=hoy.year,
            created_at__month=hoy.month
        ).count()
        
        ingresos_mes = Pago.objects.filter(
            fecha__year=hoy.year,
            fecha__month=hoy.month,
            estadoPago=EstadoPago.PAGADO
        ).aggregate(total=Sum("costeFinal"))["total"] or 0
        
        reservas_12_meses = (
            ReservaActividad.objects
            .filter(created_at__gte=hoy - timedelta(days=365))
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
            ReservaActividad.objects
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
        for pab in Pabellon.objects.all():
            horas = Sesion.objects.filter(actividad__instalacion__pabellon=pab).count() * 1

            capacidad_total = 200
            ocupacion = min(int((horas / capacidad_total) * 100), 100)

            uso_pabellones.append({
                "nombre": pab.nombre,
                "horas": horas,
                "ocupacion": ocupacion
            })

        data = {
            "instalaciones": Instalacion.contar(),
            "actividades": Actividad.contar(),
            "sesiones": Sesion.contar(),
            "pabellones": Pabellon.contar(),
            "deportes": Deporte.contar(),
            "usuarios": UsuarioFinal.contar(),
            "monitores": Monitor.contar(),
            "dinero": Pago.contarDinero(),
            "reservas_mes": reservas_mes+alquiler_mes,
            "ingresos_mes": ingresos_mes,
            "reservas_12_meses": reservas_por_mes,
            "actividades_top": actividades_mas_reservadas,
            "uso_pabellones": uso_pabellones,
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
        ).count()

        # RESERVAS ESTE MES
        reservas_mes = ReservaActividad.objects.filter(
            usuarioFinal=usuario,
            created_at__year=hoy.year,
            created_at__month=hoy.month
        ).count()

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
                created_at__gte=hoy - timedelta(days=365)
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
            .filter(usuarioFinal=usuario)
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
            .filter(usuarioFinal=usuario)
            .values("actividad__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )

        actividad_favorita = actividad_favorita["actividad__nombre"] if actividad_favorita else "-"


        # PABELLÓN FAVORITO
        pabellon_favorito = (
            ReservaActividad.objects
            .filter(usuarioFinal=usuario)
            .values("actividad__instalacion__pabellon__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )

        pabellon_favorito = pabellon_favorito["actividad__instalacion__pabellon__nombre"] if pabellon_favorito else "-"


        # RESERVAS POR DÍA DE LA SEMANA
        reservas_por_dia_qs = (
            ReservaActividad.objects
            .filter(usuarioFinal=usuario)
            .annotate(dia=ExtractWeekDay("created_at"))
            .values("dia")
            .annotate(total=Count("id"))
        )

        dias_labels = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
        dias_data = [0] * 7

        for r in reservas_por_dia_qs:
            indice = r["dia"] - 1
            dias_data[indice] = r["total"]


        data = {
            "reservas_totales": reservas_totales,
            "reservas_mes": reservas_mes,
            "cancelaciones": cancelaciones,
            "dinero_total": dinero_total,

            "actividad_favorita": actividad_favorita,
            "pabellon_favorito": pabellon_favorito,

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