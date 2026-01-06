from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework import status
from datetime import datetime

from .permissions import IsAdministrador, IsMonitor, IsUsuarioFinal

from .serializers import (
    AbonoDeportivoSerializer, AbonoVeranoSerializer, BonoSerializer,
    ActividadSerializer, AsistenciaSerializer, AgendaSerializer,
    ConfiguracionSerializer, DeporteSerializer, DescuentoSerializer,
    FavoritoSerializer, ForoSerializer, CanalSerializer, UsuarioCanalSerializer,
    HorarioSerializer, InstalacionSerializer, PabellonSerializer, ListaEsperaSerializer,
    EntradaListaEsperaSerializer, MonitorSerializer, NotificacionSerializer,
    PagoSerializer, ReservaActividadSerializer, AlquilerSerializer,
    TarifaTDASerializer, TarifaActividadSerializer, TarifaInstalacionSerializer,
    TDASerializer, UsuarioFinalSerializer, UserSerializer, AdministradorSerializer,
    CompraBonoSerializer, CompraAbonoSerializer
)

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, User, CompraBono, CompraAbono
)

# Estadisticas de home
class EstadisticasView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        tiposActividad = []
        tiposInstalacion = []

        for act in Actividad.objects.all():
            if act.tipoActividad not in tiposActividad:
                tiposActividad.append(act.tipoActividad)

        for inst in Instalacion.objects.all():
            if inst.tipoInstalacion not in tiposInstalacion:
                tiposInstalacion.append(inst.tipoInstalacion)

        data = {
            "instalaciones": Instalacion.contar(),
            "actividades": Actividad.contar(),
            "pabellones": Pabellon.contar(),
            "deportes": Deporte.contar(),
            "usuarios": UsuarioFinal.contar(),
            "tiposActividad": tiposActividad,
            "tiposInstalacion": tiposInstalacion
        }

        return Response(data)


# Busquedas
class BuscarView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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
    authentication_classes = []

    def post(self, request):
        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        sexo = request.data.get('sexo')
        fechaNacimiento = request.data.get('fechaNacimiento')
        dni = request.data.get('dni')
        telefono = request.data.get('telefono')
        correo = request.data.get('correo')
        provincia = request.data.get('provincia')
        municipio = request.data.get('municipio')
        localidad = request.data.get('localidad')
        codigoPostal = request.data.get('codigoPostal')
        password = request.data.get('password')
        cuentaBancaria = request.data.get('cuentaBancaria')
        
        respuesta = UsuarioFinal.registrar_usuario(
            nombre=nombre, apellidos=apellidos, sexo=sexo, fechaNacimiento=fechaNacimiento,
            dni=dni, telefono=telefono, correo=correo, provincia=provincia,
            municipio=municipio, localidad=localidad, codigoPostal=codigoPostal,
            password=password, cuentaBancaria=cuentaBancaria
        )

        if respuesta["error"]:
            sta = status.HTTP_400_BAD_REQUEST
        else:
            sta = status.HTTP_201_CREATED

        return Response(
            {"mensaje": respuesta["respuesta"]},
            status=sta
        )


# ----------------
# Abonos
# ----------------

class AbonoDeportivoViewSet(viewsets.ModelViewSet):
    serializer_class = AbonoDeportivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return AbonoDeportivo.objects.filter(compras_deportivo__usuarioFinal__user=user)


class AbonoVeranoViewSet(viewsets.ModelViewSet):
    serializer_class = AbonoVeranoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return AbonoVerano.objects.filter(compras_verano__usuarioFinal__user=user)


class CompraAbonoViewSet(viewsets.ModelViewSet):
    serializer_class = CompraAbonoSerializer
    permission_classes = [IsUsuarioFinal]

    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return CompraAbono.objects.all()


# ----------------
# Actividades
# ----------------

# Es necesario modificar algo get_queryset para mostrar las diferentes actividades
class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and getattr(user, "is_monitor", False):
            return Actividad.objects.filter(monitor__user=user)

        return Actividad.objects.all()


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


# ----------------
# Bonos
# ----------------
    
class BonoViewSet(viewsets.ModelViewSet):
    serializer_class = BonoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_usuario_final:
            return Bono.objects.filter(compras_bono__usuarioFinal__user=user)
        elif user.is_administrador:
            return Bono.objects.all()
        return []


class CompraBonoViewSet(viewsets.ModelViewSet):
    queryset = CompraBono.objects.all()
    serializer_class = CompraBonoSerializer
    permission_classes = [IsUsuarioFinal]

    def perform_create(self, serializer):
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)


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


# ----------------
# Descuentos
# ----------------

class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer
    permission_classes = [IsAdministrador]


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
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return UsuarioCanal.objects.filter(usuarioFinal__user=self.request.user)


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
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return EntradaListaEspera.objects.filter(usuarioFinal__user=self.request.user)


# ----------------
# Monitores
# ----------------

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    permission_classes = [IsAdministrador]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
        usuario_final = UsuarioFinal.objects.get(user=self.request.user)
        serializer.save(usuarioFinal=usuario_final)

    def get_queryset(self):
        return ReservaActividad.objects.filter(usuarioFinal_user=self.request.user)


class AlquilerViewSet(viewsets.ModelViewSet):
    serializer_class = AlquilerSerializer
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ----------------
# Administradores
# ----------------

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ----------------
# User (Django auth) modificado
# ----------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrador]


# Otros endpoints

class meAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        data = {
            "id": user.id,
            "is_monitor": user.is_monitor,
            "is_usuario_final": user.is_usuario_final,
            "is_administrador": user.is_administrador,
        }
        
        if user.is_administrador:
            data["rol"] = user.administrador.rol

        return Response(data)
