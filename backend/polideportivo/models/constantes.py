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

    Tipos de actividades:
    - AGUA, TIERRA, PISTA
    """
    
    AGUA = 'Piscinas'

    TIERRA = 'Campos de tierra'

    PISTA = 'Terreno de pista'


class Periodo(models.TextChoices):
    """
    Clase para enumerar los tipos periodos en los que se realizan las actividades

    Tipos de actividades:
    - PRIMER_CUATRIMESTRE, SEGUNDO_CUATRIMESTRE, ANUAL
    """
    
    PRIMER_CUATRIMESTRE = 'Desde septiembre hasta enero'

    SEGUNDO_CUATRIMESTRE = 'Desde febrero hasta mayo'

    ANUAL = 'Todo el año'


class TipoReserva(models.TextChoices):
    """
    Clase para enumerar los tipos de reserva posibles a realizar

    Tipos de actividades:
    - ONLINE, PRESENCIAL, AMBAS, NINGUNA
    """
    
    ONLINE = 'Permite la reserva solo online'

    PRESENCIAL = 'Permite la reserva solo presencial'

    AMBAS = 'Permite ambos tipos de reserva'
    
    NINGUNA = 'No permite ningún tipo de reserva'


class Estado(models.TextChoices):
    """
    Clase para enumerar el estado de la actividad

    Tipos de actividades:
    - FINALIZADO, EN_PROGRESO, INDEFINIDO
    """
    
    FINALIZADO = 'La actividad ha acabado'

    EN_PROGRESO = 'La actividad se esta realizando'

    INDEFINIDO = 'Estado indefinido'


class Dia(models.TextChoices):
    """
    Clase para enumerar los dias posibles para una sesión

    Tipos de actividades:
    - LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO
    """
    
    LUNES = 'lunes'

    MARTES = 'martes'

    MIERCOLES = 'miercoles'
    
    JUEVES = 'jueves'
    
    VIERNES = 'viernes'
    
    SABADO = 'sabado'
    
    DOMINGO = 'domingo'