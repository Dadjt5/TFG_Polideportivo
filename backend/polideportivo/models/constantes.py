from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoInstalacion(models.TextChoices):
    """
    Clase para enumerar los tipos de instalacion

    Tipos de instalaciones:
    - PISTA_PADEL, PISTA_TENIS, PISTA_BALONCESTO, CAMPO_FUTBOL_7, CAMPO_FUTBOL_11, CAMPO_RUGBY, PISTA_SQUASH, RECTA_ATLETISMO, PISTA_VOLEY_PLAYA,
    PISTA_POLIDEPORTIVA, SALA_MULTIUSOS, SALA_MUSCULACION, PISCINA.
    """

    PISTA_PADEL = 'PISTA_PADEL', 'Pista de pádel'
    PISTA_TENIS = 'PISTA_TENIS', 'Pista de tenis'
    PISTA_BALONCESTO = 'PISTA_BALONCESTO', 'Pista de baloncesto'
    CAMPO_FUTBOL_7 = 'CAMPO_FUTBOL_7', 'Campo de futbol 7'
    CAMPO_FUTBOL_11 = 'CAMPO_FUTBOL_11', 'Campon de futbol 11'
    PISTA_SQUASH = 'PISTA_SQUASH', 'Pista de squash'
    RECTA_ATLETISMO = 'RECTA_ATLETISMO', 'Recta de atletismo'
    PISTA_VOLEY_PLAYA = 'PISTA_VOLEY_PLAYA', 'Pista de voley playa'
    PISTA_POLIDEPORTIVA = 'PISTA_POLIDEPORTIVA', 'Pista polideportiva'
    SALA_MULTIUSOS = 'SALA_MULTIUSOS', 'Sala multiusos'
    SALA_MUSCULACION = 'SALA_MUSCULACION', 'Sala de musculación'
    PISCINA = 'PISCINA', 'Piscina'


class TipoActividad(models.TextChoices):
    """
    Clase para enumerar los tipos de actividad

    Tipos de actividades:
    - FISIOTERAPIA, GRUPOS_REDUCIDOS, OTROS
    """
    
    FISIOTERAPIA = 'FISIOTERAPIA', 'Fisioterapia'
    GRUPOS_REDUCIDOS = 'GRUPOS_REDUCIDOS', 'Grupos reducidos'
    OTROS = 'OTROS', 'Otros'


class Terreno(models.TextChoices):
    """
    Clase para enumerar los tipos de terreno donde se desarrollan las actividades

    Tipos de terreno:
    - AGUA, TIERRA, PISTA
    """
    
    AGUA = 'AGUA', 'Piscinas'
    TIERRA = 'TIERRA', 'Campos de tierra'
    PISTA = 'PISTA', 'Terreno de pista'


class Periodo(models.TextChoices):
    """
    Clase para enumerar los tipos periodos en los que se realizan las actividades

    Tipos de periodo:
    - PRIMER_CUATRIMESTRE, SEGUNDO_CUATRIMESTRE, ANUAL
    """
    
    PRIMER_CUATRIMESTRE = 'PRIMER_CUATRIMESTRE', 'Desde septiembre hasta enero'
    SEGUNDO_CUATRIMESTRE = 'SEGUNDO_CUATRIMESTRE', 'Desde febrero hasta mayo'
    ANUAL = 'ANUAL', 'Todo el año'


class FormaReserva(models.TextChoices):
    """
    Clase para enumerar las formas de reserva posibles

    Formas de reserva:
    - ONLINE, PRESENCIAL, AMBAS, NINGUNA
    """
    
    ONLINE = 'ONLINE', 'Permite la reserva solo online'
    PRESENCIAL = 'PRESENCIAL', 'Permite la reserva solo presencial'
    AMBAS = 'AMBAS', 'Permite ambos tipos de reserva'
    NINGUNA = 'NINGUNA', 'No permite ningún tipo de reserva'


class TipoReserva(models.TextChoices):
    """
    Clase para enumerar los tipos de reserva

    Tipos de reserva:
    - LIBRE, ACTIVIDAD, USUARIO
    """
    
    LIBRE = 'LIBRE', 'Libre'
    ACTIVIDAD = 'ACTIVIDAD', 'Reserva actividad'
    USUARIO = 'USUARIO', 'Reserva usuario'


class Estado(models.TextChoices):
    """
    Clase para enumerar el estado de la actividad

    Tipos de estado:
    - FINALIZADO, EN_PROGRESO, INDEFINIDO
    """
    
    FINALIZADO = 'FINALIZADO', 'La actividad ha acabado'
    EN_PROGRESO = 'EN_PROGRESO', 'La actividad se esta realizando'
    INDEFINIDO = 'INDEFINIDO', 'Estado indefinido'


class Dia(models.TextChoices):
    """
    Clase para enumerar los dias posibles para una sesión

    Días de la semana:
    - LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO
    """
    
    LUNES = 'LUNES', 'Lunes'
    MARTES = 'MARTES', 'Martes'
    MIERCOLES = 'MIERCOLES', 'Miercoles'
    JUEVES = 'JUEVES', 'Jueves'
    VIERNES = 'VIERNES', 'Viernes'
    SABADO = 'SABADO', 'Sabado'
    DOMINGO = 'DOMINGO', 'Domingo'


class Sexo(models.TextChoices):
    """
    Clase para enumerar el sexo a escoger

    Tipos de sexo:
    - MUJER, HOMBRE, NINGUNO
    """
    
    MUJER = 'MUJER', 'Mujer'
    HOMBRE = 'HOMBRE', 'Hombre'
    NINGUNO = 'NINGUNO', 'Prefiero decirlo'


class Rol(models.TextChoices):
    """
    Clase para enumerar los roles de usuario

    Tipos de rol:
    - ESTUDIANTE, PTGAS, PDI, EXTERNO
    """
    
    ESTUDIANTE = 'ESTUDIANTE', 'Estudiante de la UAM'
    PDI = 'PDI', 'Profesores y personal de investigación'
    PTGAS = 'PTGAS', 'Personal administrativo'
    EXTERNO = 'EXTERNO', 'Externo a la UAM'


class Tematica(models.TextChoices):
    """
    Clase para enumerar las tematicas de los canales

    Tematicas para los canales:
    - CHAT, SUGERENCIAS, NUEVAS_ACTIVIDADES
    """
    
    CHAT = 'CHAT', 'Chat comun sobre actividades'
    SUGERENCIAS = 'SUGERENCIAS', 'Buzon de sugerencias'
    NUEVAS_ACTIVIDADES = 'NUEVAS_ACTIVIDADES', 'Buzon de nuevas actividades'


class EstadoPago(models.TextChoices):
    """
    Clase para enumerar los estados de pago

    Estado del pago:
    - PENDIENTE, PAGADO, CANCELADO
    """
    
    PENDIENTE = 'PENDIENTE', 'Pendiente de pago'
    PAGADO = 'PAGADO', 'Pagado'
    CANCELADO = 'CANCELADO', 'Pago cancelado'


class EstadoReserva(models.TextChoices):
    """
    Clase para enumerar los estados de la reserva

    Estado de la reserva:
    - PENDIENTE, CONFIRMADA, CANCELADO
    """
    
    PENDIENTE = 'PENDIENTE', 'Pendiente de pago'
    CONFIRMADA = 'CONFIRMADA', 'Confirmada'
    CANCELADO = 'CANCELADO', 'Reserva cancelada'


class RolAdministrador(models.TextChoices):
    """
    Clase para enumerar los roles de los administradores

    Roles posibles:
    - RAIZ, ESPACIOS, USUARIOS, TARIFAS
    """
    
    RAIZ = 'RAIZ', 'Administrador raiz'
    ESPACIOS = 'ESPACIOS', 'Administrador de espacios'
    USUARIOS = 'USUARIOS', 'Administrador de usuarios'
    TARIFAS = 'TARIFAS', 'Administrador de tarifas'
