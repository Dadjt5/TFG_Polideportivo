from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoInstalacion(models.TextChoices):
    """
    Clase para enumerar los tipos de instalacion

    Tipos de instalaciones:
    - PISTA_PADEL, PISTA_TENIS, PISTA_BALONCESTO, CAMPO_FUTBOL_7, CAMPO_FUTBOL_11, CAMPO_RUGBY, PISTA_SQUASH, RECTA_ATLETISMO, PISTA_VOLEY_PLAYA,
    PISTA_POLIDEPORTIVA, SALA_MULTIUSOS, SALA_MUSCULACION.
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


class TipoActividad(models.TextChoices):
    """
    Clase para enumerar los tipos de actividad

    Tipos de actividades:
    - FISIOTERAPIA, GRUPOS_REDUCIDOS, OTROS
    """
    
    FISIOTERAPIA = 'Fisioterapia'

    GRUPOS_REDUCIDOS = 'Actividades para grupos reducidos'

    OTROS = 'Otros tipos de actividad'


class Terreno(models.TextChoices):
    """
    Clase para enumerar los tipos de terreno donde se desarrollan las actividades

    Tipos de terreno:
    - AGUA, TIERRA, PISTA
    """
    
    AGUA = 'Piscinas'

    TIERRA = 'Campos de tierra'

    PISTA = 'Terreno de pista'


class Periodo(models.TextChoices):
    """
    Clase para enumerar los tipos periodos en los que se realizan las actividades

    Tipos de periodo:
    - PRIMER_CUATRIMESTRE, SEGUNDO_CUATRIMESTRE, ANUAL
    """
    
    PRIMER_CUATRIMESTRE = 'Desde septiembre hasta enero'

    SEGUNDO_CUATRIMESTRE = 'Desde febrero hasta mayo'

    ANUAL = 'Todo el año'


class TipoReserva(models.TextChoices):
    """
    Clase para enumerar los tipos de reserva posibles a realizar

    Tipos de reserva:
    - ONLINE, PRESENCIAL, AMBAS, NINGUNA
    """
    
    ONLINE = 'Permite la reserva solo online'

    PRESENCIAL = 'Permite la reserva solo presencial'

    AMBAS = 'Permite ambos tipos de reserva'
    
    NINGUNA = 'No permite ningún tipo de reserva'


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
    
    LUNES = 'lunes'

    MARTES = 'martes'

    MIERCOLES = 'miercoles'
    
    JUEVES = 'jueves'
    
    VIERNES = 'viernes'
    
    SABADO = 'sabado'
    
    DOMINGO = 'domingo'


class Sexo(models.TextChoices):
    """
    Clase para enumerar el sexo a escoger

    Tipos de sexo:
    - MUJER, HOMBRE, NINGUNO
    """
    
    MUJER = 'Mujer'

    HOMBRE = 'Hombre'

    NINGUNO = 'Prefiero decirlo'


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


class TipoBono(models.TextChoices):
    """
    Clase para enumerar los tipos de bono

    Tipos de bono:
    - PADEL, TENIS, SALA_MUSCULACION, PISCINA
    """
    
    PADEL = 'Bono para padel'

    TENIS = 'Bono para tenis'

    SALA_MUSCULACION = 'Bono para la sala de musculacion'
    
    PISCINA = 'Bono para piscina'


class EstadoPago(models.TextChoices):
    """
    Clase para enumerar los estados de pago

    Estado del pago:
    - PENDIENTE, PAGADA, CANCELADA
    """
    
    PENDIENTE = 'Pendiente de pago'

    PAGADA = 'Pagado'

    CANCELADA = 'Pago cancelado'


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