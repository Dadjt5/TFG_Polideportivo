from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
import json

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, CompraBono, CompraAbono, Sesion,
    Mensaje, MapaReservas, GrupoReducido, ActividadComun, Fisioterapia, TipoInstalacion,
    Feedback, Calle
)


User = get_user_model()


# --------------------
# Feedback
# --------------------

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


# --------------------
# Deportes
# --------------------

class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deporte
        fields = ("id", "titulo")


# --------------------
# Usuarios
# --------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'codigo_usuario')
        
class UsuarioFinalSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioFinal
        fields = ('id', 'DNI', 'nombre', 'tieneAbono', 'tieneTDA', 'esUAM')


class UsuarioFinalSerializer(serializers.ModelSerializer):
    # La contraseña no se pasa cuando se hace un get, solo para modificarla
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    deportesFavoritos = DeporteSerializer(many=True, read_only=True)
    email = serializers.SerializerMethodField()
    codigo_usuario = serializers.SerializerMethodField()
    deportes_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Deporte.objects.all(),
        write_only=True,
        source="deportesFavoritos"
    )
    actividadesFavoritas = serializers.SerializerMethodField()
    instalacionesFavoritas = serializers.SerializerMethodField()
    
    class Meta:
        model = UsuarioFinal
        fields = (
            "id",
            "nombre",
            "apellidos",
            "DNI",
            "codigo_usuario",
            "tieneAbono",
            "tieneTDA",
            "esUAM",
            "fechaNacimiento",
            "telefono",
            "provincia",
            "municipio",
            "localidad",
            "codigoPostal",
            "actividadesRealizadas",
            "deportesFavoritos",
            "deportes_ids",
            "sexo",
            "rol",
            "user",
            "email",
            "actividadesFavoritas",
            "instalacionesFavoritas",
            "password",
        )
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_codigo_usuario(self, obj):
        return obj.user.codigo_usuario

    def get_actividadesFavoritas(self, obj):
        return list(
            obj.favoritos
            .filter(actividad__isnull=False)
            .values_list("actividad_id", flat=True)
        )

    def get_instalacionesFavoritas(self, obj):
        return list(
            obj.favoritos
            .filter(instalacion__isnull=False)
            .values_list("instalacion_id", flat=True)
        )
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        if 'email' in user_data:
            instance.user.email = user_data['email']

        password = validated_data.pop('password', None)
        if password:
            instance.user.set_password(password)

        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MonitorSerializer(serializers.ModelSerializer):
    # La contraseña no se pasa cuando se hace un get, solo para modificarla
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    email = serializers.SerializerMethodField()
    codigo_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Monitor
        fields = (
            "id",
            "nombre",
            "apellidos",
            "DNI",
            "codigo_usuario",
            "user",
            "email",
            "password"
        )
        
    def get_email(self, obj):
        return obj.user.email
    
    def get_codigo_usuario(self, obj):
        return obj.user.codigo_usuario
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        if 'email' in user_data:
            instance.user.email = user_data['email']

        password = validated_data.pop('password', None)
        if password:
            instance.user.set_password(password)

        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MonitorSimpleSerializer(serializers.ModelSerializer):
    carga = serializers.SerializerMethodField()

    class Meta:
        model = Monitor
        fields = ("id", 'DNI', "nombre", "carga")
        
    def get_carga(self, obj):
        return sum(act.calcularHorasSemanales() for act in obj.actividades.all())


class AdministradorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('id', 'DNI', 'nombre', 'rol')


class AdministradorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    email = serializers.SerializerMethodField()
    codigo_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Administrador
        fields = ('id', 'DNI', 'nombre', 'user', 'email', 'rol', 'codigo_usuario', 'password')

    def get_email(self, obj):
        return obj.user.email

    def get_codigo_usuario(self, obj):
        return obj.user.codigo_usuario

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        if 'email' in user_data:
            instance.user.email = user_data['email']

        password = validated_data.pop('password', None)
        if password:
            instance.user.set_password(password)

        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

# --------------------
# Abonos
# --------------------

class AbonoDeportivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbonoDeportivo
        fields = '__all__'


class AbonoVeranoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbonoVerano
        fields = '__all__'


class CompraAbonoSerializer(serializers.ModelSerializer):
    abonoDeportivo = AbonoDeportivoSerializer(read_only=True)
    abonoVerano = AbonoVeranoSerializer(read_only=True)

    class Meta:
        model = CompraAbono
        fields = (
            "id",
            "fecha",
            "estado",
            "abonoDeportivo",
            "abonoVerano",
        )


# --------------------
# Agenda
# --------------------

class MapaReservasSerializer(serializers.ModelSerializer):
    periodo = serializers.SerializerMethodField()

    class Meta:
        model = MapaReservas
        fields = ("id", "horaInicio", "horaFin", "estado", "periodo")
    
    def get_periodo(self, obj):
        sesion = Sesion.objects.filter(
            horaInicio__lte=obj.horaInicio,
            horaFin__gt=obj.horaInicio
        ).first()

        if sesion and sesion.actividad:
            return sesion.actividad.periodo
        return None


class AgendaSerializer(serializers.ModelSerializer):
    mapa_reservas = MapaReservasSerializer(many=True, read_only=True)

    class Meta:
        model = Agenda
        fields = ("id", "fecha", "dia", "horaApertura", "horaCierre", "abierto", "mapa_reservas")

# --------------------
# Horarios
# --------------------

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'


# --------------------
# Instalaciones
# --------------------

class CalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calle
        fields = '__all__'

class PabellonSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabellon
        fields = ('id', 'nombre', 'direccion')


class PabellonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabellon
        fields = '__all__'


class InstalacionSimpleSerializer(serializers.ModelSerializer):
    agenda = AgendaSerializer(many=True, read_only=True)
    calles = CalleSerializer(many=True, read_only=True)

    class Meta:
        model = Instalacion
        fields = ("id", "nombre", "agenda", "calles", "numeroCalles", "tipoInstalacion")


class InstalacionSerializer(serializers.ModelSerializer):
    agenda = AgendaSerializer(many=True, read_only=True)
    calles = CalleSerializer(many=True, read_only=True)
    pabellon = PabellonSimpleSerializer(read_only=True)

    class Meta:
        model = Instalacion
        fields = (
            "id",
            "nombre",
            "tipoInstalacion",
            "aforoMaximo",
            "luz",
            "imagenURL",
            "porcentajeTDA",
            "pabellon",
            "agenda",
            "tarifa",
            "numeroCalles",
            "calles"
        )

# --------------------
# Actividades
# --------------------

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = (
            "id",
            "dia",
            "horaInicio",
            "horaFin"
        )


class ActividadSimpleSerializer(serializers.ModelSerializer):
    horasSemanales = serializers.SerializerMethodField()
    dias = serializers.SerializerMethodField()

    class Meta:
        model = Actividad
        fields = (
            "id",
            "nombre",
            "horasSemanales",
            "dias",
            "estado"
        )
    
    def get_horasSemanales(self, obj):
        return obj.calcularHorasSemanales()

    def get_dias(self, obj):
        return obj.getDias()


class ActividadSerializer(serializers.ModelSerializer):
    sesiones = SesionSerializer(many=True, read_only=True)

    horasSemanales = serializers.SerializerMethodField()
    dias = serializers.SerializerMethodField()
    nombreDeporte = serializers.SerializerMethodField()
    nombreInstalacion = serializers.SerializerMethodField()
    nombreMonitor = serializers.SerializerMethodField()

    class Meta:
        model = Actividad
        fields = (
            "id",
            "nombre",
            "descripcion",
            "tipoActividad",
            "imagenURL",
            "plazasMaximas",
            "plazasReservadas",
            "edadMinima",
            "año",
            "numeroCreditos",
            "nivel",
            "material",
            "exterior",
            "tipoReserva",
            "terreno",
            "periodo",
            "estado",
            "horasSemanales",
            "dias",
            "tarifa",
            "inscripcion",
            "instalacion",
            "deportes",
            "monitor",
            "sesiones",
            "nombreDeporte",
            "nombreMonitor",
            "nombreInstalacion"
        )

    def get_horasSemanales(self, obj):
        return obj.calcularHorasSemanales()

    def get_nombreDeporte(self, obj):
        return obj.deportes.titulo if obj.deportes else None

    def get_nombreMonitor(self, obj):
        return obj.monitor.nombre if obj.monitor else None

    def get_nombreInstalacion(self, obj):
        return obj.instalacion.nombre if obj.instalacion else None

    def get_dias(self, obj):
        return [sesion.dia for sesion in obj.sesiones.all()]


class AsistenciaSerializer(serializers.ModelSerializer):
    nombreUsuario = serializers.SerializerMethodField()

    class Meta:
        model = Asistencia
        fields = (
            "id",
            "sesion",
            "presente",
            "usuarioFinal",
            "nombreUsuario"
        )

    def get_nombreUsuario(self, obj):
        usuarioFinal = obj.usuarioFinal

        if usuarioFinal:
            return usuarioFinal.nombre
        return None 

# --------------------
# Bonos
# --------------------

class BonoSerializer(serializers.ModelSerializer):
    nombreInstalacion = serializers.SerializerMethodField()
    precioFinal = serializers.SerializerMethodField()
    textoPrecio = serializers.SerializerMethodField()

    class Meta:
        model = Bono
        fields = (
            "id",
            "validez",
            "usos",
            "precioTDA",
            "precioUAM",
            "precioAbono",
            "precioOtros",
            "precioFinal",
            "textoPrecio",
            "instalacion",
            "nombreInstalacion"
        )
    
    def get_precioFinal(self, obj):
        user = self.context.get('user')
        precio = obj.precioOtros

        if user and user.is_usuario_final:
            usuario = user.usuario_final

            if usuario.tieneTDA and precio > obj.precioTDA:
                precio = obj.precioTDA

            if usuario.esUAM and precio > obj.precioUAM:
                precio = obj.precioUAM

            if usuario.tieneAbono and precio > obj.precioAbono:
                precio = obj.precioAbono

        return precio
    
    def get_textoPrecio(self, obj):
        user = self.context.get('user')
        precio = obj.precioOtros
        cadena = ""

        if user and user.is_usuario_final:
            usuario = user.usuario_final

            if usuario.tieneTDA and precio > obj.precioTDA:
                precio = obj.precioTDA
                cadena = "Descuento por TDA"

            if usuario.esUAM and precio > obj.precioUAM:
                precio = obj.precioUAM
                cadena = "Descuento comunidad UAM"

            if usuario.tieneAbono and precio > obj.precioAbono:
                precio = obj.precioAbono
                cadena = "Descuento por abono"

        return cadena
    
    def get_nombreInstalacion(self, obj):
        if obj.instalacion:
            return obj.instalacion.nombre
        return ""


class CompraBonoSerializer(serializers.ModelSerializer):
    bono = BonoSerializer(read_only=True)

    class Meta:
        model = CompraBono
        fields = (
            "id",
            "fecha",
            "fechaExpiracion",
            "vecesUsado",
            "bono",
            "estado"
        )

# --------------------
# Configuración
# --------------------

class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'


# --------------------
# Descuentos
# --------------------

class DescuentoSerializer(serializers.ModelSerializer):
    tiposInstalacion = serializers.ListField(child=serializers.ChoiceField(choices=TipoInstalacion.choices))

    class Meta:
        model = Descuento
        fields = '__all__'
        

class DescuentoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = ('nombre', 'porcentaje')

# --------------------
# Favoritos
# --------------------

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = '__all__'


# --------------------
# Foro
# --------------------


class CanalUsuarioFinalSerializer(serializers.ModelSerializer):
    silenciado = serializers.SerializerMethodField()

    class Meta:
        model = Canal
        fields = (
            "id", 
            "titulo", 
            "numeroParticipantes", 
            "tema", 
            "secreto",
            "silenciado"
        )
        
    def get_silenciado(self, obj):
        user = self.context["request"].user.usuario_final
        usuario = UsuarioCanal.objects.filter(canal=obj, usuarioFinal=user).first()
        
        if usuario:
            return usuario.silenciado

        return False


class UsuarioCanalSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = UsuarioCanal
        fields = ("usuarioFinal", "nombre", "silenciado", "expulsado", "fechaEntrada")

    def get_nombre(self, obj):
        return obj.usuarioFinal.nombre


class CanalAdministradorSerializer(serializers.ModelSerializer):
    usuarios = UsuarioCanalSerializer(source="usuarioFinal", many=True, read_only=True)

    class Meta:
        model = Canal
        fields = ("id", "titulo", "numeroParticipantes", "tema", "secreto", "oculto", "usuarios")


class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = '__all__'


class CanalSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = ("id", "titulo")


class ForoSerializer(serializers.ModelSerializer):
    canales = CanalSimpleSerializer(source="canal", many=True)

    class Meta:
        model = Foro
        fields = ("id", "numeroParticipantes", "canales")



class MensajeSerializer(serializers.ModelSerializer):
    es_admin = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = Mensaje
        fields = (
            "id",
            "texto",
            "fechaEnvio",
            "nombre",
            "es_admin"
        )
        
    def get_es_admin(self, obj):
        if obj.usuario.is_administrador:
            return True
        return False

    def get_nombre(self, obj):
        if obj.usuario.is_administrador:
            return "Administrador"
        return obj.usuario.usuario_final.nombre


# --------------------
# Lista de espera
# --------------------

class ListaEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaEspera
        fields = '__all__'


class EntradaListaEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaListaEspera
        fields = '__all__'


# --------------------
# Notificaciones
# --------------------

class NotificacionSerializer(serializers.ModelSerializer):
    actividad = ActividadSimpleSerializer(read_only=True)
    instalacion = InstalacionSimpleSerializer(read_only=True)
    pabellon = PabellonSimpleSerializer(read_only=True)

    class Meta:
        model = Notificacion
        fields = (
            "id",
            "titulo",
            "descripcion",
            "fecha",
            "hora",
            "leido",
            "fijado",
            "actividad",
            "instalacion",
            "pabellon"
        )

# --------------------
# Pagos
# --------------------

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = (
            "concepto",
            "coste",
            "costeFinal",
            "descuentoAplicado",
            "fecha",
            "estadoPago"
        )


# --------------------
# Tarifas
# --------------------

class TarifaTDASerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaTDA
        fields = '__all__'

class TarifaTDASimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaTDA
        fields = ('id', 'titulo')


class TarifaInstalacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaInstalacion
        fields = '__all__'
        
class TarifaInstalacionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaInstalacion
        fields = ('id', 'titulo')


class TarifaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaActividad
        fields = '__all__'


class ActividadComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadComun
        fields = '__all__'

class ActividadComunSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadComun
        fields = ('id', 'titulo')


class GrupoReducidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoReducido
        fields = '__all__'

class GrupoReducidoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoReducido
        fields = ('id', 'titulo')


class FisioterapiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisioterapia
        fields = '__all__'

class FisioterapiaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisioterapia
        fields = ('id', 'titulo')


# --------------------
# Reservas
# --------------------

class ReservaActividadSimpleSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = ReservaActividad
        fields = (
            "id",
            "estado",
            "pago",
            "nombre"
        )

    def get_nombre(self, obj):
        return obj.actividad.nombre


class ReservaActividadSerializer(serializers.ModelSerializer):
    actividad = ActividadSimpleSerializer(read_only=True)
    pago = PagoSerializer(read_only=True)
    tarifa = TarifaActividadSerializer(read_only=True)

    class Meta:
        model = ReservaActividad
        fields = (
            "id",
            "estado",
            "tarifa",
            "pago",
            "descuentos",
            "actividad"
        )


class AlquilerSerializer(serializers.ModelSerializer):
    instalacion = InstalacionSimpleSerializer(read_only=True)
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Alquiler
        fields = (
            "id",
            "fecha",
            "pago",
            "instalacion",
        )


class AlquilerSimpleSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Alquiler
        fields = (
            "id",
            "fecha",
            "horaInicio",
            "horaFin",
            "numeroHoras",
            "pago",
            "nombre"
        )

    def get_nombre(self, obj):
        return obj.instalacion.nombre


# --------------------
# TDA
# --------------------

class TDASerializer(serializers.ModelSerializer):
    class Meta:
        model = TDA
        fields = '__all__'
