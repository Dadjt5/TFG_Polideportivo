from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoInstalacion(models.TextChoices):
    """
    Clase para enumerar los tipos de instalacion

    Tipos de instalaciones:
    - PISTA_PADEL, PISTA_TENIS, PISTA_BALONCESTO, CAMPO_FUTBOL_7, CAMPO_FUTBOL_11, CAMPO_RUGBY, PISTA_SQUASH, RECTA_ATLETISMO, PISTA_VOLEY_PLAYA,
    PISTA_POLIDEPORTIVA, SALA_MULTIUSOS, SALA_MUSCULACION, PISCINA.
    """

    PISTA_PADEL = 'Pista de pádel'
    PISTA_TENIS = 'Pista de tenis'
    PISTA_BALONCESTO = 'Pista de baloncesto'
    CAMPO_FUTBOL_7 = 'Campo de futbol 7'
    CAMPO_FUTBOL_11 = 'Campon de futbol 11'
    PISTA_SQUASH = 'Pista de squash'
    RECTA_ATLETISMO = 'Recta de atletismo'
    PISTA_VOLEY_PLAYA = 'Pista de voley playa'
    PISTA_POLIDEPORTIVA = 'Pista polideportiva'
    SALA_MULTIUSOS = 'Sala multiusos'
    SALA_MUSCULACION = 'Sala de musculación'
    PISCINA = 'Piscina'


class TipoActividad(models.TextChoices):
    """
    Clase para enumerar los tipos de actividad

    Tipos de actividades:
    - FISIOTERAPIA, GRUPOS_REDUCIDOS, OTROS
    """
    
    FISIOTERAPIA = 'Fisioterapia'
    GRUPOS_REDUCIDOS = 'Grupos reducidos'
    OTROS = 'Otros'


class Terreno(models.TextChoices):
    """
    Clase para enumerar los tipos de terreno donde se desarrollan las actividades

    Tipos de terreno:
    - AGUA, TIERRA, PISTA
    """
    
    AGUA = 'Piscinas'
    TIERRA = 'Campos de tierra'
    PISTA = 'Terreno de pista'
    ARENA = 'Terreno de arena'


class Periodo(models.TextChoices):
    """
    Clase para enumerar los tipos periodos en los que se realizan las actividades

    Tipos de periodo:
    - PRIMER_CUATRIMESTRE, SEGUNDO_CUATRIMESTRE, TERCER_CUATRIMESTRE, ANUAL
    """
    
    PRIMER_CUATRIMESTRE = 'Desde septiembre hasta enero'
    SEGUNDO_CUATRIMESTRE = 'Desde febrero hasta mayo'
    TERCER_CUATRIMESTRE = 'Meses de verano'
    ANUAL = 'Todo el año'


class FormaReserva(models.TextChoices):
    """
    Clase para enumerar las formas de reserva posibles

    Formas de reserva:
    - ONLINE, PRESENCIAL, AMBAS, NINGUNA
    """
    
    ONLINE = 'Permite la reserva solo online'
    PRESENCIAL = 'Permite la reserva solo presencial'
    AMBAS = 'Permite ambos tipos de reserva'
    NINGUNA = 'No permite ningún tipo de reserva'


class TipoReserva(models.TextChoices):
    """
    Clase para enumerar los tipos de reserva

    Tipos de reserva:
    - LIBRE, ACTIVIDAD, USUARIO
    """
    
    LIBRE = 'Libre'
    ACTIVIDAD = 'Reserva actividad'
    USUARIO = 'Reserva usuario'


class Estado(models.TextChoices):
    """
    Clase para enumerar el estado de la actividad

    Tipos de estado:
    - FINALIZADO, EN_PROGRESO, INDEFINIDO
    """
    
    FINALIZADO = 'La actividad ha acabado'
    EN_PROGRESO = 'La actividad se esta realizando'
    INDEFINIDO = 'Estado indefinido'


class Dia(models.TextChoices):
    """
    Clase para enumerar los dias posibles para una sesión

    Días de la semana:
    - LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO
    """
    
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miercoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SABADO = 'Sabado'
    DOMINGO = 'Domingo'


class Sexo(models.TextChoices):
    """
    Clase para enumerar el sexo a escoger

    Tipos de sexo:
    - MUJER, HOMBRE, NINGUNO
    """
    
    MUJER = 'Mujer'
    HOMBRE = 'Hombre'
    NINGUNO = 'Prefiero no decirlo'


class Rol(models.TextChoices):
    """
    Clase para enumerar los roles de usuario

    Tipos de rol:
    - ESTUDIANTE, PTGAS, PDI, EXTERNO
    """
    
    ESTUDIANTE = 'Estudiante de la UAM'
    PDI = 'Profesores y personal de investigación'
    PTGAS = 'Personal administrativo'
    EXTERNO = 'Externo a la UAM'


class Tematica(models.TextChoices):
    """
    Clase para enumerar las tematicas de los canales

    Tematicas para los canales:
    - CHAT, SUGERENCIAS, NUEVAS_ACTIVIDADES
    """
    
    CHAT = 'Chat comun sobre actividades'
    SUGERENCIAS = 'Buzon de sugerencias'
    NUEVAS_ACTIVIDADES = 'Buzon de nuevas actividades'


class EstadoPago(models.TextChoices):
    """
    Clase para enumerar los estados de pago

    Estado del pago:
    - PENDIENTE, PAGADO, CANCELADO
    """
    
    PENDIENTE = 'Pendiente de pago'
    PAGADO = 'Pagado'
    CANCELADO = 'Pago cancelado'


class TipoPago(models.TextChoices):
    """
    Clase para enumerar los tipos de pago

    Tipos de pago:
    - UNICO, MENSUAL, CUATRIMESTRAL, ANUAL
    """
    
    UNICO = 'Pago unico'
    MENSUAL = 'Pago mensual'
    CUATRIMESTRAL = 'Pago cuatrimestral'
    ANUAL = 'Pago anual'


class EstadoReserva(models.TextChoices):
    """
    Clase para enumerar los estados de la reserva

    Estado de la reserva:
    - PENDIENTE, CONFIRMADA, CANCELADO
    """
    
    PENDIENTE = 'Pendiente de pago'
    CONFIRMADA = 'Confirmada'
    CANCELADO = 'Reserva cancelada'


class RolAdministrador(models.TextChoices):
    """
    Clase para enumerar los roles de los administradores

    Roles posibles:
    - RAIZ, ESPACIOS, USUARIOS, TARIFAS
    """
    
    RAIZ = 'Administrador raiz'
    ESPACIOS = 'Administrador de espacios'
    USUARIOS = 'Administrador de usuarios'
    TARIFAS = 'Administrador de tarifas'
