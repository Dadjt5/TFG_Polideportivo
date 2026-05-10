from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction
from datetime import time
from django.db.models import Q

from .constantes import EstadoReserva
from .descuento import Descuento
from .actividad import Actividad
from .notificacion import Notificacion
from .constantes import FormaReserva, TipoInstalacion


class Reserva(models.Model):
    """Modelo para representar una reserva"""

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE, related_name="+")
    descuentos = models.ManyToManyField('Descuento', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

    class Meta:
        abstract = True
    
    # Función para calcular el descuento aplicado a la reserva
    def calcularDescuento(self):
        resultado = {}

        for descuento in self.descuentos.all():
            resultado[descuento.nombre] = descuento.porcentaje

        return resultado


class ReservaActividad(Reserva):
    """Modelo para representar una reserva en una actividad"""

    numeroHorasSemana = models.IntegerField(default=1)
    numeroPersonas = models.IntegerField(default=1)
    tipoPago = models.CharField(default="total")
    tipoSesion = models.CharField(default="consulta")

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE, related_name="reservas_actividad")
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.actividad}'

    # Función para calcular el precio de la actividad
    def calcularPrecio(self, numeroSesiones):
        """Calcula el precio final de la reserva usando la actividad"""
        return self.actividad._calcular_precio_base(
            usuario=self.usuarioFinal,
            numeroHorasSemana=self.numeroHorasSemana,
            numeroPersonas=self.numeroPersonas,
            tipoPago=self.tipoPago,
            tipoSesion=self.tipoSesion,
            numeroSesiones=numeroSesiones
        )
    
    # Función para confirmar la reserva de la actividad
    def confirmarCompra(self):
        if self.estado != EstadoReserva.CONFIRMADA:
            self.usuarioFinal.actividadesRealizadas += 1
            self.usuarioFinal.save()

            self.estado = EstadoReserva.CONFIRMADA
            self.save()

    # Función para cancelar una reserva de una actividad y notificar al siguiente usuario de la lista de espera
    def cancelarCompra(self):
        with transaction.atomic():
            actividad = Actividad.objects.select_for_update().get(id=self.actividad.id)

            if self.estado == EstadoReserva.CONFIRMADA:
                if self.usuarioFinal.actividadesRealizadas > 0:
                    self.usuarioFinal.actividadesRealizadas -= 1
    
                actividad.eliminarAsistencia(self.usuarioFinal)
                self.usuarioFinal.save()

            if actividad.plazasReservadas > 0:
                actividad.plazasReservadas -= 1
                actividad.save()

            self.estado = EstadoReserva.CANCELADO
            self.save()

            try:
                lista_espera = actividad.lista_espera
                while actividad.plazasReservadas < actividad.plazasMaximas:
                    entrada = lista_espera.siguienteUsuario()
                    if not entrada:
                        break

                    actividad.plazasReservadas += 1
                    actividad.save()

                    Notificacion.notificarSalidaListaDeEspera(entrada.usuarioFinal, actividad)
            except:
                pass

    # Función para contar el número de reservas de actividades en el sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para crear una nueva reserva de una actividad    
    @classmethod
    def nuevaReserva(cls, usuario, actividad, complementos, lista=False):
        if actividad.tipoReserva == FormaReserva.PRESENCIAL or actividad.tipoReserva == FormaReserva.NINGUNA:
            return None

        with transaction.atomic():
            actividad.refresh_from_db()

            descuentos = Descuento.obtenerDescuentos(actividad=actividad)

            if cls.objects.filter(usuarioFinal=usuario, actividad=actividad, estado=EstadoReserva.CONFIRMADA).exists():
                return None

            # Lista de espera
            if actividad.plazasReservadas >= actividad.plazasMaximas and not lista:
                return None

            reservasPrevias = cls.objects.filter(usuarioFinal=usuario, actividad=actividad, estado=EstadoReserva.PENDIENTE)

            for r in reservasPrevias:
                r.cancelarCompra()

            reserva = cls.objects.create(
                usuarioFinal=usuario,
                numeroHorasSemana=actividad.calcularHorasSemanales(),
                numeroPersonas=complementos["personas"],
                tipoSesion=complementos["tipoSesion"],
                tipoPago=complementos["forma"],
                actividad=actividad,
                estado=EstadoReserva.PENDIENTE
            )

            if descuentos:
                reserva.descuentos.set(descuentos["descuentos"])

            actividad.plazasReservadas += 1
            actividad.save()

            actividad.activarAsistencia(usuario)

            return reserva


class Alquiler(Reserva):
    """Modelo para representar un alquiler en una instalacion"""
    fecha = models.DateField(default=timezone.now)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    numeroHoras = models.FloatField(default=0.0)
    luz = models.BooleanField(default=False)

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE, related_name="alquileres")
    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE, related_name="reservas")
    calle = models.ForeignKey('Calle', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Alquiler de {self.instalacion}, en {self.fecha} de {self.horaInicio} a {self.horaFin}'

    # Función para calcular el precio del alquiler
    def calcularPrecio(self):
        """Calcula el precio final de la reserva usando la instalacion"""
        precio = 0.0

        if (self.horaFin > time(20, 0) or self.horaInicio < time(8,0)) and self.instalacion.luz:
            self.luz = True
            precio += self.instalacion.tarifa.costeIluminacion

        precio += self.instalacion._calcular_precio_base(usuario=self.usuarioFinal)*self.numeroHoras
        return precio

    # FUnción para confirmar el alquiler
    def confirmarCompra(self):
        self.estado = EstadoReserva.CONFIRMADA
        self.save()

    # Función para cancelar el alquiler
    def cancelarCompra(self):
        self.estado = EstadoReserva.CANCELADO
        self.save()

    # Función para contar el número de alquileres en el sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para crear un nuevo alquiler en la instalación indicada    
    @classmethod
    def nuevaReserva(cls, usuario, instalacion, fecha, horaInicio, horaFin, luz, calle=None):
        with transaction.atomic():
            instalacion.refresh_from_db()

            descuentos = Descuento.obtenerDescuentos(instalacion=instalacion)
            conflictos = cls.objects.filter(
                instalacion=instalacion,
                fecha=fecha,
                estado=EstadoReserva.CONFIRMADA,
                horaInicio__lt=horaFin,
                horaFin__gt=horaInicio
            )

            if instalacion.tipoInstalacion == TipoInstalacion.PISCINA:
                conflictos = conflictos.filter(calle=calle)

            if conflictos.exists():
                return None

            if not instalacion.controlarAlquiler(fecha, horaInicio, horaFin, calle):
                return None

            reservasPrevias = cls.objects.filter(usuarioFinal=usuario, instalacion=instalacion, estado=EstadoReserva.PENDIENTE)

            for r in reservasPrevias:
                r.cancelarCompra()

            reserva = cls.objects.create(
                usuarioFinal=usuario,
                instalacion=instalacion,
                calle=calle,
                fecha=fecha,
                horaInicio=horaInicio,
                horaFin=horaFin,
                luz=luz,
                estado=EstadoReserva.PENDIENTE
            )

            if descuentos:
                reserva.descuentos.set(descuentos["descuentos"])

            return reserva

    # Función para sobreescribir el guardado para guardar el número de horas
    def save(self, *args, **kwargs):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        horas = (t2-t1)/3600
        self.numeroHoras = horas
        
        super().save(*args, **kwargs)