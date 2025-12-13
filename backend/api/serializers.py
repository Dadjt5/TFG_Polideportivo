from rest_framework import serializers
from django.contrib.auth import get_user_model

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Horario, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler
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


# --------------------
# Actividades
# --------------------

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
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

class InstalacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instalacion
        fields = '__all__'


class PabellonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabellon
        fields = '__all__'


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
