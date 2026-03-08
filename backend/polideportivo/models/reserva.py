from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction

from .constantes import EstadoReserva
from .descuento import Descuento
from .lista_espera import ListaEspera, EntradaListaEspera
from .notificacion import Notificacion
from .constantes import FormaReserva


class Reserva(models.Model):
    """Modelo para representar una reserva"""

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    descuentos = models.ManyToManyField('Descuento', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

    class Meta:
        abstract = True
        
    def calcularDescuento(self):
        porcentaje = 0.0

        for descuento in self.descuentos.all():
            porcentaje += descuento.porcentaje

        return porcentaje


class ReservaActividad(Reserva):
    """Modelo para representar una reserva en una actividad"""

    numeroHorasSemana = models.IntegerField(default=0)
    numeroPersonas = models.IntegerField(default=1)
    tipoPago = models.CharField(default="total")
    tipoSesion = models.CharField(default="consulta")

    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.actividad}'
    
    def calcular_precio(self):
        """Calcula el precio final de la reserva usando la actividad"""
        return self.actividad._calcular_precio_base(
            usuario=self.usuarioFinal,
            numeroHorasSemana=self.numeroHorasSemana,
            numeroPersonas=self.numeroPersonas,
            tipoPago=self.tipoPago,
            tipoSesion=self.tipoSesion
        )
    
    def confirmarCompra(self):
        if self.estado != EstadoReserva.CONFIRMADA:
            self.usuarioFinal.actividadesRealizadas += 1
            self.usuarioFinal.save()

            self.estado = EstadoReserva.CONFIRMADA
            self.save()

    def cancelarCompra(self):
        self.actividad.lista_espera.salirLista(self.usuarioFinal)

        self.actividad.plazasReservadas -= 1
        self.estado = EstadoReserva.CANCELADO
        self.save()

        if self.estado == EstadoReserva.CONFIRMADA:
            self.usuarioFinal.actividadesRealizadas -= 1
            self.usuarioFinal.save()

        lista_espera = self.actividad.lista_espera
        while self.actividad.plazasReservadas < self.actividad.plazasMaximas:
            entrada = lista_espera.siguienteUsuario()
            if not entrada:
                break

            descuentos = Descuento.obtener_descuentos(actividad=self.actividad)
            if descuentos:
                self.descuentos.set(descuentos["descuento"]["aplicados"])

            ReservaActividad.objects.get_or_create(
                usuarioFinal=entrada.usuarioFinal,
                actividad=self.actividad,
                estado=EstadoReserva.PENDIENTE
            )

            Notificacion.notificarSalidaListaDeEspera(entrada.usuarioFinal, self.actividad)

            entrada.delete()

            self.actividad.plazasReservadas += 1
            self.actividad.save()

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def nuevaReserva(cls, usuario, actividad):
        if actividad.tipoReserva == FormaReserva.PRESENCIAL or actividad.tipoReserva == FormaReserva.NINGUNA:
            return None

        with transaction.atomic():
            actividad.refresh_from_db()

            descuentos = Descuento.obtener_descuentos(actividad=actividad)

            if cls.objects.filter(usuarioFinal=usuario, actividad=actividad, estado=EstadoReserva.CONFIRMADA).exists():
                return None

            # Lista de espera
            if actividad.plazasReservadas >= actividad.plazasMaximas:
                lista = ListaEspera.objects.filter(actividad=actividad).first()
                EntradaListaEspera.objects.create(usuarioFinal=usuario, listaEspera=lista)

            reservasPrevias = cls.objects.filter(usuarioFinal=usuario, actividad=actividad, estado=EstadoReserva.PENDIENTE)

            for r in reservasPrevias:
                r.cancelarCompra()

            reserva = cls.objects.create(
                usuarioFinal=usuario,
                actividad=actividad,
                estado=EstadoReserva.PENDIENTE
            )

            if descuentos:
                reserva.descuentos.set(descuentos["descuento"]["aplicados"])

            actividad.plazasReservadas = cls.objects.filter(actividad=actividad, estado__in=[EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]).count()
            actividad.save()

            return reserva


class Alquiler(Reserva):
    """Modelo para representar un alquiler en una instalacion"""

    fecha = models.DateField(default=timezone.now)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    numeroHoras = models.FloatField(default=0.0)

    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE)

    def __str__(self):
        return f'Alquiler de {self.instalacion}, en {self.fecha} de {self.horaInicio} a {self.horaFin}'
    
    def calcular_precio(self):
        """Calcula el precio final de la reserva usando la instalacion"""
        return self.instalacion._calcular_precio_base(usuario=self.usuarioFinal)

    def confirmarCompra(self):
        self.estado = EstadoReserva.CONFIRMADA
        self.save()

    def cancelarCompra(self):
        self.estado = EstadoReserva.CANCELADO
        self.save()

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def nuevaReserva(cls, usuario, instalacion, fecha, horaInicio, horaFin):
        with transaction.atomic():
            instalacion.refresh_from_db()

            descuentos = Descuento.obtener_descuentos(instalacion=instalacion)
            
            if cls.objects.filter(fecha=fecha, horaInicio=horaInicio, estado=EstadoReserva.CONFIRMADA).exists() or cls.objects.filter(fecha=fecha, horaFin=horaFin, estado=EstadoReserva.CONFIRMADA).exists():
                return None

            if not instalacion.controlarAlquiler(fecha, horaInicio, horaFin):
                return None

            reservasPrevias = cls.objects.filter(usuarioFinal=usuario, instalacion=instalacion, estado=EstadoReserva.PENDIENTE)

            for r in reservasPrevias:
                r.cancelarCompra()

            reserva = cls.objects.create(
                usuarioFinal=usuario,
                instalacion=instalacion,
                fecha=fecha,
                horaInicio=horaInicio,
                horaFin=horaFin,
                estado=EstadoReserva.PENDIENTE
            )

            if descuentos:
                reserva.descuentos.set(descuentos["descuento"]["aplicados"])

            return reserva

    def save(self, *args, **kwargs):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        horas = (t2-t1)/3600
        self.numeroHoras = horas
        
        super().save(*args, **kwargs)

    @property
    def valido(self):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        
        horas = (t1-t2)/3600
        if horas > 2.0:
            return False

        return True