from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, CompraBono, CompraAbono, Sesion
)


User = get_user_model()

# --------------------
# Usuarios
# --------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class UsuarioFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioFinal
        fields = '__all__'


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = '__all__'


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
    class Meta:
        model = CompraAbono
        fields = '__all__'


# --------------------
# Actividades
# --------------------

class ActividadSerializer(serializers.ModelSerializer):
    horasSemanales = serializers.SerializerMethodField()
    nombreMonitor = serializers.SerializerMethodField()
    dias = serializers.SerializerMethodField()


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
            "nombreMonitor",
            "dias"
        )

    def get_horasSemanales(self, obj):
        return obj.calcularHorasSemanales()

    def get_nombreMonitor(self, obj):
        monitor = obj.monitor

        if monitor:
            return monitor.nombre
        return None
    
    def get_dias(self, obj):
        return ",".join(sesion.dia for sesion in obj.sesion.all())
        

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'


# --------------------
# Agenda
# --------------------

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'


# --------------------
# Bonos
# --------------------

class BonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bono
        fields = '__all__'


class CompraBonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraBono
        fields = '__all__'


# --------------------
# Configuración
# --------------------

class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'


# --------------------
# Deportes
# --------------------

class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deporte
        fields = '__all__'


# --------------------
# Descuentos
# --------------------

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = '__all__'


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

class InstalacionSerializer(serializers.ModelSerializer):
    pabellon = PabellonSerializer(read_only=True)
    horaApertura = serializers.SerializerMethodField()
    horaCierre = serializers.SerializerMethodField()

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
# Reservas
# --------------------

class ReservaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaActividad
        fields = '__all__'


class AlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alquiler
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
# TDA
# --------------------

class TDASerializer(serializers.ModelSerializer):
    class Meta:
        model = TDA
        fields = '__all__'
