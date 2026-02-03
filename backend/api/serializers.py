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
    Mensaje, MapaReservas
)


User = get_user_model()


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
        fields = ['id', 'first_name', 'last_name']
        
class UsuarioFinalSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioFinal
        fields = ('id', 'nombre', 'tieneAbono', 'tieneTDA', 'esUAM')


class UsuarioFinalSerializer(serializers.ModelSerializer):
    # La contraseña no se pasa cuando se hace un get, solo para modificarla
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    deportesFavoritos = DeporteSerializer(many=True, read_only=True)
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
            "fechaNacimiento",
            "telefono",
            "provincia",
            "municipio",
            "localidad",
            "codigoPostal",
            "cuentaBancaria",
            "actividadesRealizadas",
            "deportesFavoritos",
            "deportes_ids",
            "sexo",
            "rol",
            "user",
            "actividadesFavoritas",
            "instalacionesFavoritas",
            "password",
        )

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
        password = validated_data.pop("password", None)
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
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Monitor
        fields = (
            "id",
            "nombre",
            "apellidos",
            "DNI",
            "user",
            "email",
            "password"
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


class MonitorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ("id", "nombre")


class AdministradorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('id', 'nombre', 'rol')


class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'


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

    class Meta:
        model = CompraBono
        fields = (
            "id",
            "fecha",
            "fechaExpiracion",
            "valido",
            "diasRestantes"
            "abonoDeportivo",
            "abonoVerano",
            "pago"
        )


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

class PabellonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabellon
        fields = '__all__'


class InstalacionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instalacion
        fields = ("id", "nombre")


class InstalacionSerializer(serializers.ModelSerializer):
    pabellon = PabellonSerializer(read_only=True)
    horaApertura = serializers.SerializerMethodField()
    horaCierre = serializers.SerializerMethodField()
    imagenURL = serializers.SerializerMethodField()

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
            "horaApertura",
            "horaCierre",
        )

    def get_horaApertura(self, obj):
        hoy = timezone.localdate()
        
        # Controlamos solo mandar instalaciones que esten abiertas
        agenda = obj.agenda.filter(fecha=hoy, abierto=True).first()

        if agenda:
            return agenda.horaApertura
        
        return None

    def get_horaCierre(self, obj):
        hoy = timezone.localdate()
        
        # Controlamos solo mandar instalaciones que esten abiertas
        agenda = obj.agenda.filter(fecha=hoy, abierto=True).first()

        if agenda:
            return agenda.horaCierre
        
        return None
    
    def get_imagenURL(self, obj):
        if not obj.imagenURL:
            return []

        try:
            data = json.loads(obj.imagenURL)
            if isinstance(data, list):
                return data
        except Exception:
            pass

        return [obj.imagenURL]

# --------------------
# Actividades
# --------------------

class SesionSerializer(serializers.ModelSerializer):
    horario = HorarioSerializer(read_only=True)

    class Meta:
        model = Sesion
        fields = (
            "id",
            "dia",
            "horario"
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
    instalacion = InstalacionSimpleSerializer(read_only=True)
    monitor = MonitorSimpleSerializer(read_only=True)
    sesiones = SesionSerializer(many=True, read_only=True)
    horasSemanales = serializers.SerializerMethodField()
    dias = serializers.SerializerMethodField()
    imagenURL = serializers.SerializerMethodField()

    class Meta:
        model = Actividad
    
        fields = (
            "id",
            "nombre",
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
            "instalacion",
            "monitor",
            "sesiones"
        )

    def get_horasSemanales(self, obj):
        return obj.calcularHorasSemanales()

    def get_dias(self, obj):
        return ",".join(sesion.dia for sesion in obj.sesiones.all())

    def get_imagenURL(self, obj):
        if not obj.imagenURL:
            return []

        try:
            data = json.loads(obj.imagenURL)
            if isinstance(data, list):
                return data
        except Exception:
            pass

        return [obj.imagenURL]

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
# Agenda
# --------------------

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'


class MapaReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapaReservas
        fields = '__all__'


# --------------------
# Bonos
# --------------------

class BonoSerializer(serializers.ModelSerializer):
    nombreInstalacion = serializers.SerializerMethodField()
    nombreDeporte = serializers.SerializerMethodField()
    precioFinal = serializers.SerializerMethodField()
    textoPrecio = serializers.SerializerMethodField()

    class Meta:
        model = Bono
        fields = (
            "id",
            "validez",
            "usos",
            "precioFinal",
            "textoPrecio",
            "nombreInstalacion",
            "nombreDeporte"
        )
    
    def get_precioFinal(self, obj):
        user = self.context.get('user')
        precio = obj.precioOtros

        if user.is_usuario_final:
            if user.usuario_final.tda.first():
                if precio > obj.precioTDA:
                    precio = obj.precioTDA

            if user.usuario_final.rol and "externo" not in user.usuario_final.rol.lower():
                if precio > obj.precioUAM:
                    precio = obj.precioUAM

            if user.usuario_final.abono.first():
                if precio > obj.precioAbono:
                    precio = obj.precioAbono

        return precio
    
    def get_textoPrecio(self, obj):
        user = self.context.get('user')
        cadena = ""
        precio = obj.precioOtros
        
        if user.is_usuario_final:
            if user.usuario_final.tda.first():
                if precio > obj.precioTDA:
                    precio = obj.precioTDA
                    cadena = "Descuento por TDA"

            if user.usuario_final.rol and "externo" not in user.usuario_final.rol.lower():
                if precio > obj.precioUAM:
                    precio = obj.precioUAM
                    cadena = "Descuento comunidad UAM"

            if user.usuario_final.abono.first():
                if precio > obj.precioAbono:
                    precio = obj.precioAbono
                    cadena = "Descuento por abono"

        return cadena
    
    def get_nombreInstalacion(self, obj):
        instalacion = obj.instalacion

        if instalacion:
            return instalacion.nombre
        return None
    
    def get_nombreDeporte(self, obj):
        deporte = obj.deporte

        if deporte:
            return deporte.titulo
        return None


class CompraBonoSerializer(serializers.ModelSerializer):
    bono = BonoSerializer(read_only=True)
    usosRestantes = serializers.ReadOnlyField()
    valido = serializers.ReadOnlyField()

    class Meta:
        model = CompraBono
        fields = (
            "id",
            "fecha",
            "fechaExpiracion",
            "vecesUsado",
            "valido",
            "usosRestantes",
            "bono",
            "pago"
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

class ForoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foro
        fields = '__all__'


class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = '__all__'


class UsuarioCanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioCanal
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    nombreUsuario = serializers.SerializerMethodField()
    class Meta:
        model = Mensaje
        fields = (
            "id",
            "texto",
            "fechaEnvio",
            "nombreUsuario"
        )

    def get_nombreUsuario(self, obj):
        usuarioFinal = obj.usuarioFinal

        if usuarioFinal:
            return usuarioFinal.nombre
        return None


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
    class Meta:
        model = Notificacion
        fields = '__all__'

# --------------------
# Pagos
# --------------------

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


# --------------------
# Tarifas
# --------------------

class TarifaTDASerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaTDA
        fields = '__all__'


class TarifaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaActividad
        fields = '__all__'


class TarifaInstalacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaInstalacion
        fields = '__all__'


# --------------------
# Reservas
# --------------------

class ReservaActividadSerializer(serializers.ModelSerializer):
    actividad = ActividadSimpleSerializer(read_only=True)
    descuento = DescuentoSimpleSerializer(read_only=True)
    pago = PagoSerializer(read_only=True)
    tarifa = TarifaActividadSerializer(read_only=True)

    class Meta:
        model = ReservaActividad
        fields = (
            "id",
            "tarifa",
            "pago",
            "descuento",
            "actividad"
        )


class AlquilerSerializer(serializers.ModelSerializer):
    instalacion = InstalacionSimpleSerializer(read_only=True)
    horario = HorarioSerializer(read_only=True)
    descuento = DescuentoSerializer(read_only=True)
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Alquiler
        fields = (
            "id",
            "fecha",
            "tarifa",
            "pago",
            "instalacion",
            "horario",
            "descuento",
        )


# --------------------
# TDA
# --------------------

class TDASerializer(serializers.ModelSerializer):
    class Meta:
        model = TDA
        fields = '__all__'
