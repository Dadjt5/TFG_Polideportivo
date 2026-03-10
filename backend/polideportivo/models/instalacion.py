from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import time, datetime, timedelta
from django.db.models import Q

from .agenda import Agenda
from .actividad import Sesion
from .constantes import TipoInstalacion, Dia


class Pabellon(models.Model):
    """Modelo para representar un pabellon"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=1024, blank=True)
    imagenURL = models.ImageField(upload_to="pabellones/", blank=True, null=True)
    direccion = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.nombre}, localizado en {self.direccion}'
    
    @classmethod
    def contar(cls):
        return cls.objects.count()


class Instalacion(models.Model):
    """Modelo para representar una instalacion"""

    nombre = models.CharField(max_length=256, blank=True)
    imagenURL = models.ImageField(upload_to="instalaciones/", blank=True, null=True)
    aforoMaximo = models.PositiveIntegerField(default=50)
    luz = models.BooleanField(default=False)
    porcentajeTDA = models.FloatField(default=0.0)
    numeroCalles = models.PositiveIntegerField(default=0)

    pabellon = models.ForeignKey(Pabellon, on_delete=models.RESTRICT)
    tarifa = models.ForeignKey('TarifaInstalacion', on_delete=models.PROTECT, blank=True, null=True)

    tipoInstalacion = models.CharField(default=TipoInstalacion.SALA_MULTIUSOS, choices=TipoInstalacion.choices)

    def __str__(self):
        return f'{self.nombre}, ubicado en el {self.pabellon}'
    
    def crear_calles(self):
        if self.tipoInstalacion != TipoInstalacion.PISCINA:
            return

        for i in range(1, self.numeroCalles + 1):
            Calle.objects.create(instalacion=self, numero=i)
    
    def obtener_precios(self):
        return {
            "precioAbonado": self.tarifa.precioAbonado,
            "precioUAM": self.tarifa.precioUAM,
            "precioTDA": self.tarifa.precioTDA,
            "precioOtros": self.tarifa.precioOtros
        }

    def _calcular_precio_base(self, usuario):
        precio = self.tarifa.precioOtros
        if usuario.tieneAbono:
            precio = self.tarifa.precioAbonado
        elif usuario.esUAM:
            precio = self.tarifa.precioUAM
        elif usuario.tieneTDA:
            precio = self.tarifa.precioTDA

        return precio

    def modificarInformacion(self, instlacion_data, pabellon, tarifa, imagen):
        campos_simples = [
            "nombre",
            "aforoMaximo",
            "luz",
            "porcentajeTDA",
        ]

        for campo in campos_simples:
            if campo in instlacion_data:
                setattr(self, campo, instlacion_data[campo])

        self.tarifa = tarifa
        self.pabellon = pabellon
        self.imagenURL = imagen

        self.save()
        return True
    
    def sincronizarMapaReservas(self, agenda, minutos=60):
        if not agenda.abierto:
            agenda.mapa_reservas.all().delete()
            return True

        inicio = datetime.combine(datetime.today(), agenda.horaApertura)
        fin = datetime.combine(datetime.today(), agenda.horaCierre)
        slots_necesarios = []
        while inicio < fin:
            siguiente = inicio + timedelta(minutes=minutos)
            slots_necesarios.append((inicio.time(), siguiente.time()))
            inicio = siguiente

        slots_existentes = agenda.mapa_reservas.all()

        for reserva in slots_existentes:
            if reserva.horaInicio < agenda.horaApertura or reserva.horaFin > agenda.horaCierre:
                reserva.delete()

        if self.tipoInstalacion != TipoInstalacion.PISCINA:
            for inicio, fin in slots_necesarios:
                if not slots_existentes.filter(horaInicio=inicio, horaFin=fin, calle__isnull=True).exists():
                    agenda.mapa_reservas.create(horaInicio=inicio, horaFin=fin)
        else:
            for calle in self.calles.all():
                for inicio, fin in slots_necesarios:
                    if not slots_existentes.filter(horaInicio=inicio, horaFin=fin, calle=calle).exists():
                        agenda.mapa_reservas.create(horaInicio=inicio, horaFin=fin, calle=calle)

        return True

    def sincronizarCalles(self, numero_calles):
        if self.tipoInstalacion != TipoInstalacion.PISCINA:
            self.calles.all().delete()
            return

        actuales = self.calles.count()

        if numero_calles > actuales:
            for i in range(actuales + 1, numero_calles + 1):
                Calle.objects.create(instalacion=self, numero=i)

        elif numero_calles < actuales:
            self.calles.filter(numero__gt=numero_calles).delete()

    def controlarHorarioActividad(self, dia, hora_inicio, hora_fin, sesion_id=None, calle=None):
        if isinstance(hora_inicio, str):
            h, m = map(int, hora_inicio.split(":"))
            hora_inicio = time(h, m)

        if isinstance(hora_fin, str):
            h, m = map(int, hora_fin.split(":"))
            hora_fin = time(h, m)

        agenda = self.agenda.filter(dia__iexact=dia).first()

        if not agenda or not agenda.abierto:
            return False

        if agenda.horaApertura > hora_inicio or agenda.horaCierre < hora_fin:
            return False

        conflictos = Sesion.objects.filter(
            actividad__instalacion=self,
            dia__iexact=dia,
            horaInicio__lt=hora_fin,
            horaFin__gt=hora_inicio
        )

        if self.tipoInstalacion == TipoInstalacion.PISCINA:
            conflictos = conflictos.filter(calle=calle)

        if sesion_id and sesion_id != -1:
            conflictos = conflictos.exclude(id=sesion_id)

        if conflictos.exists():
            return False

        return True
    
    def controlarCambioHorario(self, dia, horaInicio, horaFin, abierto):
        if not abierto:
            return not self.actividad.filter(sesiones__dia__iexact=dia).exists()

        conflictos = Sesion.objects.filter(
            actividad__instalacion=self,
            dia__iexact=dia
        ).filter(
            Q(horaInicio__lt=horaInicio) | Q(horaFin__gt=horaFin)
        )

        return not conflictos.exists()

    def controlarAlquiler(self, dia, horaInicio, horaFin, calle=None):
        agenda = self.agenda.filter(fecha=dia).first()

        if not agenda:
            dia_semana = dia.strftime("%A").upper()

            mapa_dias = {
                "MONDAY": Dia.LUNES,
                "TUESDAY": Dia.MARTES,
                "WEDNESDAY": Dia.MIERCOLES,
                "THURSDAY": Dia.JUEVES,
                "FRIDAY": Dia.VIERNES,
                "SATURDAY": Dia.SABADO,
                "SUNDAY": Dia.DOMINGO,
            }

            dia_modelo = mapa_dias[dia_semana]

            agenda = Agenda.objects.filter(instalacion=self, dia__iexact=dia_modelo).first()

        if not agenda:
            return False

        if agenda.estaOcupado(horaInicio, horaFin, calle):
            return False

        return True

    def nuevoHorario(self, dia, horaApertura, horaCierre, abierto):
        if isinstance(horaApertura, str):
            h, m = map(int, horaApertura.split(":")[:2])
            horaApertura = time(h, m)

        if isinstance(horaCierre, str):
            h, m = map(int, horaCierre.split(":")[:2])
            horaCierre = time(h, m)

        agenda = Agenda.objects.filter(instalacion=self, dia=dia, fecha__isnull=True).first()

        if not abierto:
            if agenda:
                agenda.abierto = False
                agenda.horaApertura = None
                agenda.horaCierre = None
                agenda.save()
            else:
                Agenda.objects.create(instalacion=self, dia=dia, abierto=False)
            return True

        if not horaApertura or not horaCierre or horaCierre <= horaApertura:
            return False

        if agenda:
            agenda.abierto = True
            agenda.horaApertura = horaApertura
            agenda.horaCierre = horaCierre
            agenda.save()
        else:
            agenda = Agenda.objects.create(
                instalacion=self,
                dia=dia,
                horaApertura=horaApertura,
                horaCierre=horaCierre,
                abierto=True
            )

        self.sincronizarMapaReservas(agenda, minutos=60)
        return True

    def nuevoHorarioEspecial(self, fecha, horaApertura, horaCierre, abierto):
        if isinstance(horaApertura, str):
            h, m = map(int, horaApertura.split(":")[:2])
            horaApertura = time(h, m)

        if isinstance(horaCierre, str):
            h, m = map(int, horaCierre.split(":")[:2])
            horaCierre = time(h, m)

        if not abierto:
            Agenda.objects.create(instalacion=self, fecha=fecha, abierto=False)
            return True

        if not horaApertura or not horaCierre or horaCierre <= horaApertura:
            return False

        agenda = Agenda.objects.create(instalacion=self, fecha=fecha, horaApertura=horaApertura, horaCierre=horaCierre)
        self.sincronizarMapaReservas(agenda, minutos=60)

        return True

    def get_horario(self, fecha):
        agenda = Agenda.objects.filter(instalacion=self, fecha=fecha).first()

        if agenda and agenda.abierto:
            return agenda.horaApertura, agenda.horaCierre

        return None, None


    def get_reservas(self, fecha):
        agenda = Agenda.objects.filter(instalacion=self, fecha=fecha, abierto=True).first()

        if not agenda:
            return []

        if self.tipoInstalacion != TipoInstalacion.PISCINA:
            reservas = []
            for mapa in agenda.mapa_reservas.filter(calle__isnull=True):
                reservas.append({
                    "horaInicio": mapa.horaInicio.strftime("%H:%M"),
                    "horaFin": mapa.horaFin.strftime("%H:%M"),
                    "estado": mapa.estado
                })

            return reservas
        else:
            calles = []
            for calle in self.calles.all():
                reservas = []

                mapas = agenda.mapa_reservas.filter(calle=calle)
                for mapa in mapas:
                    reservas.append({
                        "horaInicio": mapa.horaInicio.strftime("%H:%M"),
                        "horaFin": mapa.horaFin.strftime("%H:%M"),
                        "estado": mapa.estado
                    })

                calles.append({
                    "calle": calle.numero,
                    "reservas": reservas
                })

            return calles

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def buscar(cls, nombre=None, tipo=None, horaInicio=None, horaFin=None):
        res = cls.objects.all()

        if nombre:
            res = res.filter(nombre__icontains=nombre)

        if tipo:
            res = res.filter(tipoInstalacion__in=tipo)

        if horaInicio:
            res = res.filter(agenda__horaApertura__lte=horaInicio)

        if horaFin:
            res = res.filter(agenda__horaCierre__gte=horaFin)

        return res.distinct()


class Calle(models.Model):
    numero = models.PositiveIntegerField()

    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE, related_name="calles")

    def __str__(self):
        return f"Calle {self.numero} - {self.instalacion.nombre}"