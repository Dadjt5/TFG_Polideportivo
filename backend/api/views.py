from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework import status
from django.shortcuts import get_object_or_404

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
    CompraBonoSerializer, CompraAbonoSerializer, MensajeSerializer, SesionSerializer
)

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, User, CompraBono, CompraAbono,
    Mensaje, Sesion
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
        return CompraAbono.objects.filter(usuarioFinal__user=self.request.user)


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
        return CompraBono.objects.filter(usuarioFinal__user=self.request.user)

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
    
    def get_queryset(self):
        return Deporte.objects.filter(usuariosFinales__user=self.request.user)


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

    def get_queryset(self):
        return UsuarioCanal.objects.filter(usuarioFinal__user=self.request.user)


class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [IsAuthenticated]


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
    serializer_class = MonitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Monitor.objects.filter(user=self.request.user)

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
    permission_classes = [IsAdministrador]



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
                
        deportes = list(Deporte.objects.values("id", "titulo"))

        data = {
            "instalaciones": Instalacion.contar(),
            "actividades": Actividad.contar(),
            "pabellones": Pabellon.contar(),
            "deportes": Deporte.contar(),
            "usuarios": UsuarioFinal.contar(),
            "tiposActividad": tiposActividad,
            "tiposInstalacion": tiposInstalacion,
            "tiposDeporte": deportes
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
            sta = status.HTTP_400_BAD_REQUEST
        else:
            sta = status.HTTP_201_CREATED

        return Response(
            {"mensaje": respuesta["respuesta"]},
            status=sta
        )


# Registrar monitor
class RegistroMonitorView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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
            sta = status.HTTP_400_BAD_REQUEST
        else:
            sta = status.HTTP_201_CREATED

        return Response(
            {"mensaje": respuesta["respuesta"]},
            status=sta
        )


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

        return Response({"status": "ok"})


# Asignar la TDA al usuario
class ValidarTDAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        codigo = request.data.get("codigo")

        tdas_libres = TDA.objects.filter(usuarioFinal__isnull=True)

        for tda in tdas_libres:
            if tda.comprobar_codigo_secreto(codigo) or tda.codigo_secreto == codigo:
                tda.asignar_usuario(request.user.usuario_final)
                return Response({"status": "ok"})

        return Response({"status": "error"})


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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reservas = []

        alquileres = Alquiler.objects.filter(usuarioFinal__user=user)
        actividades = ReservaActividad.objects.filter(usuarioFinal__user=user)

        for alquiler in alquileres:
            reservas.append({
                "id": alquiler.id,
                "tipo": "alquiler",
                "fechaInicio": alquiler.horario.fecha_inicio,
                "id_obj": alquiler.instalacion.id,
                "titulo": alquiler.instalacion.nombre,
                "horario": f"{alquiler.horario.horaInicio} - {alquiler.horario.horaFin}",
                "dias": "",
                "pago": {
                    "coste": alquiler.pago.coste,
                    "estadoPago": alquiler.pago.estadoPago,
                }
            })

        for reserva in actividades:
            reservas.append({
                "id": reserva.id,
                "tipo": "actividad",
                "fechaInicio": reserva.actividad.fecha_inicio,
                "id_obj": reserva.actividad.id,
                "titulo": reserva.actividad.nombre,
                "horario": reserva.actividad.horasSemanales,
                "dias": reserva.actividad.dias,
                "pago": {
                    "coste": reserva.pago.coste,
                    "estadoPago": reserva.pago.estadoPago,
                }
            })

        reservas.sort(key=lambda r: r["fechaInicio"])

        return Response(reservas)


# Mostrar el foro y los canales, pero sin los mensajes
class ForoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        foro = Foro.objects.all().first()

        if user.is_usuario_final:
            canales = []
            
            for canal in foro.canal.all():
                usuarioCanal = UsuarioCanal.objects.filter(canal=canal, usuarioFinal=user.usuario_final).first()
                if not canal.oculto and not usuarioCanal.expulsado:
                    canales.append({
                        "id": canal.id,
                        "titulo": canal.titulo,
                        "numeroParticipantes": canal.numeroParticipantes,
                        "tema": canal.tema,
                        "secreto": canal.secreto,
                        "silenciado": usuarioCanal.silenciado
                    })
                
            return Response(canales)
        elif user.id_administrador:
            return Response(foro)
    
        return Response("Usuario incorrecto")


# Mostrar los mensajes del un canal
class MensajesCanalView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, canal_id):
        canal = get_object_or_404(Canal, id=canal_id)

        mensajes = canal.getMensajes().order_by("fechaEnvio")
        
        serializer = MensajeSerializer(mensajes, many=True)

        return Response(serializer.data)
    
    def post(self, request, canal_id):
        canal = get_object_or_404(Canal, id=canal_id)

        resultado = canal.nuevoMensaje(request.user.usuario_final, request.data.get("texto", ""))

        if resultado:
            return Response({"respuesta": "Mensaje enviado"}, status=status.HTTP_201_CREATED)

        return Response({"respuesta": "No puedes escribir en este canal"}, status=status.HTTP_403_FORBIDDEN)


# Mostrar las sesiones del monitor
class SesionesMonitorView(APIView):
    permission_classes = [IsAuthenticated]

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
                        "horaInicio": sesion.horario.horaInicio,
                        "horaFin": sesion.horario.horaFin
                    })

        return Response(sesiones)


# Mostrar informacion en detalle de una sesion para el monitor
class DetalleSesionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, actividad_id, sesion_id):
        data = []

        actividad = get_object_or_404(Actividad, id=actividad_id)
        sesion = get_object_or_404(Sesion, id=sesion_id, actividad=actividad)

        data = {
            "dia": sesion.dia,
            "horaInicio": sesion.horario.horaInicio,
            "horaFin": sesion.horario.horaFin,
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
    permission_classes = [IsAuthenticated]

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
    
    
class TarifaActividadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id)

        precios = actividad.obtener_precios()
        data = {
            "tarifa": {
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
        data = {
            "tarifa": {
                "datos": precios
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