from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import time, datetime, timedelta, date
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from .agenda import Agenda
from .actividad import Sesion
from .notificacion import Notificacion
from .usuario_final import UsuarioFinal
from .pago import Pago
from .constantes import TipoInstalacion, Dia, TipoReserva, Periodo, EstadoReserva

DIA_MAP = {
    "Lunes": 0,
    "Martes": 1,
    "Miercoles": 2,
    "Jueves": 3,
    "Viernes": 4,
    "Sabado": 5,
    "Domingo": 6
}

class Pabellon(models.Model):
    """Modelo para representar un pabellon"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=1024, blank=True)
    imagen = models.ImageField(upload_to="pabellones/", blank=True, null=True)
    direccion = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.nombre}, localizado en {self.direccion}'
    
    # Función para contar los pabellones del sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()


class Instalacion(models.Model):
    """Modelo para representar una instalacion"""

    nombre = models.CharField(max_length=256, blank=True)
    imagen = models.ImageField(upload_to="instalaciones/", blank=True, null=True)
    aforoMaximo = models.PositiveIntegerField(default=50)
    luz = models.BooleanField(default=False)
    porcentajeTDA = models.FloatField(default=0.0)
    numeroCalles = models.PositiveIntegerField(default=0)

    pabellon = models.ForeignKey(Pabellon, on_delete=models.RESTRICT)
    tarifa = models.ForeignKey('TarifaInstalacion', on_delete=models.RESTRICT, blank=True, null=True)

    tipoInstalacion = models.CharField(default=TipoInstalacion.SALA_MULTIUSOS, choices=TipoInstalacion.choices)

    def __str__(self):
        return f'{self.nombre}, ubicado en el {self.pabellon}'
    
    # Función para crear nuevas calles en la piscina
    def crearCalles(self):
        if self.tipoInstalacion != TipoInstalacion.PISCINA:
            return
    
        self.calles.all().delete()

        for i in range(1, self.numeroCalles + 1):
            Calle.objects.create(instalacion=self, numero=i)
    
    # Función para obtener los precios indicados por la tarifa de la isntalación
    def obtenerPrecios(self):
        return {
            "precioAbonado": self.tarifa.precioAbonado,
            "precioUAM": self.tarifa.precioUAM,
            "precioTDA": self.tarifa.precioTDA,
            "precioOtros": self.tarifa.precioOtros,
            "costeIluminacion": self.tarifa.costeIluminacion
        }

    # Función auxiliar para obtener el precio base para el alquiler de la instalación
    def _calcular_precio_base(self, usuario):
        precio = self.tarifa.precioOtros
        if usuario.tieneAbono:
            precio = self.tarifa.precioAbonado
        elif usuario.esUAM:
            precio = self.tarifa.precioUAM
        elif usuario.tieneTDA:
            precio = self.tarifa.precioTDA

        return precio

    # Función para comprobar el aforo de la instalacion frente a las plazas máximas de la actividad
    def comprobarAforo(self, instalacion_data):
        for act in self.actividad.all():
            if act.plazasMaximas > instalacion_data["aforoMaximo"]:
                return False

        return True

    # Función para modificar la información de la instalación
    def modificarInformacion(self, instalacion_data, pabellon, tarifa, imagen):
        campos_simples = [
            "nombre",
            "aforoMaximo",
            "luz",
            "porcentajeTDA",
            "numeroCalles"
        ]

        for campo in campos_simples:
            if campo in instalacion_data:
                setattr(self, campo, instalacion_data[campo])

        self.tarifa = tarifa
        self.pabellon = pabellon
        self.imagenURL = imagen

        self.save()
        return True

    # Función para actualizar el mapa de reservas para marcar los slots indicados por las sesiones como reservados por actividad
    def actualizarMapa(self, sesiones):
        for sesion in sesiones:
            dia = sesion.get('dia')
            hora_inicio = sesion.get('horaInicio')
            hora_fin = sesion.get('horaFin')
            calle_num = sesion.get('calle')

            calle = None
            if self.tipoInstalacion == TipoInstalacion.PISCINA:
                calle = self.calles.filter(numero=calle_num).first()

            agenda = Agenda.objects.filter(instalacion=self, dia__iexact=dia).first()

            if agenda:
                if isinstance(hora_inicio, str):
                    hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()

                if isinstance(hora_fin, str):
                    hora_fin = datetime.strptime(hora_fin, "%H:%M").time()

                hora_actual = datetime.combine(datetime.today(), hora_inicio)
                hora_fin_dt = datetime.combine(datetime.today(), hora_fin)

                while hora_actual < hora_fin_dt:
                    siguiente_hora = hora_actual + timedelta(hours=1)

                    mapa = agenda.mapa_reservas.filter(
                        horaInicio=hora_actual.time(),
                        horaFin=siguiente_hora.time(),
                        calle=calle
                    ).first()

                    if mapa:
                        mapa.estado = TipoReserva.ACTIVIDAD
                        mapa.save()

                    hora_actual = siguiente_hora

    # FUnción para actualizar el mapa de reservas de acuerdo a los nuevos horarios de la instalación
    def sincronizarMapaReservas(self, agenda, minutos=60):
        if not agenda.abierto:
            agenda.mapa_reservas.all().delete()
            return True

        horaApertura = agenda.horaApertura
        horaCierre = agenda.horaCierre

        if isinstance(horaApertura, str):
            horaApertura = time.fromisoformat(horaApertura)
        
        if isinstance(horaCierre, str):
            horaCierre = time.fromisoformat(horaCierre)

        inicio = datetime.combine(datetime.today(), horaApertura)
        fin = datetime.combine(datetime.today(), horaCierre)
        slots_necesarios = []
        while inicio < fin:
            siguiente = inicio + timedelta(minutes=minutos)
            slots_necesarios.append((inicio.time(), siguiente.time()))
            inicio = siguiente

        slots_existentes = agenda.mapa_reservas.all()

        for reserva in slots_existentes:
            if reserva.horaInicio < horaApertura or reserva.horaFin > horaCierre:
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

    # Función para actualizar el número de calles de una piscina
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
        
        self.numeroCalles = numero_calles
        self.save()

    # Función para revisar la lista de alquileres realizados que coinciden con ciertas sesiones de una actividad
    def revisarAlquileres(self, sesiones, periodo, confirmacion):
        usuarios_ids = set()
        alquileres_conflicto = set()
        alquileres_pendientes = set()

        alquileres = self.reservas.exclude(estado=EstadoReserva.CANCELADO)

        for sesion in sesiones:
            dia = sesion.get("dia")
            hora_inicio_sesion = sesion.get("horaInicio")
            hora_fin_sesion = sesion.get("horaFin")
            calle_num = sesion.get("calle")

            dia_sesion = DIA_MAP.get(dia)

            # Convertir horas
            if isinstance(hora_inicio_sesion, str):
                hora_inicio_sesion = time.fromisoformat(hora_inicio_sesion)
            if isinstance(hora_fin_sesion, str):
                hora_fin_sesion = time.fromisoformat(hora_fin_sesion)

            for alquiler in alquileres:
                if alquiler.calle != calle_num:
                    continue

                if alquiler.fecha.weekday() != dia_sesion:
                    continue

                # Comprobamos el periodo de la actividad en relacion al alquiler
                mes = alquiler.fecha.month
                if periodo == Periodo.PRIMER_CUATRIMESTRE:
                    if mes not in [9,10,11,12,1]:
                        return None
                elif periodo == Periodo.SEGUNDO_CUATRIMESTRE:
                    if mes not in [2,3,4,5]:
                        return None
                elif periodo == Periodo.TERCER_CUATRIMESTRE:
                    if mes not in [6,7,8]:
                        return None

                inicio = alquiler.horaInicio
                fin = alquiler.horaFin

                if not (hora_fin_sesion <= inicio or hora_inicio_sesion >= fin):
                    if alquiler.estado == EstadoReserva.CONFIRMADA:
                        usuarios_ids.add(alquiler.usuarioFinal.id)
                        alquileres_conflicto.add(alquiler)
                    elif alquiler.estado == EstadoReserva.PENDIENTE:
                        alquileres_pendientes.add(alquiler)

        if confirmacion:
            usuarios = UsuarioFinal.objects.filter(id__in=usuarios_ids)

            Notificacion.notificarCancelacionYDevolucionDinero(usuarios, self)

            for alquiler in alquileres_pendientes:
                alquiler.cancelarCompra()

            for alquiler in alquileres_conflicto:
                ct = ContentType.objects.get_for_model(alquiler)
                pago = Pago.objects.filter(content_type=ct, object_id=alquiler.id).first()
                if pago:
                    pago.cancelarPago("unico")

            return

        dinero = 0
        for alquiler in alquileres_conflicto:
            ct = ContentType.objects.get_for_model(alquiler)
            pago = Pago.objects.filter(content_type=ct, object_id=alquiler.id).first()
            if pago:
                dinero += pago.costeFinal

        return {
            "alquileres": len(alquileres_conflicto),
            "usuarios": len(usuarios_ids),
            "dinero": dinero
        }

    # Función para controlar los horarios de sesiones de una actividad para saber si coinciden con otras sesiones de otras actividades
    def controlarHorarioActividad(self, dia, horaInicio, horaFin, sesion_id=None, calle=None):
        if isinstance(horaInicio, str):
            h, m = map(int, horaInicio.split(":"))
            horaInicio = time(h, m)

        if isinstance(horaFin, str):
            h, m = map(int, horaFin.split(":"))
            horaFin = time(h, m)

        agenda = self.agenda.filter(dia__iexact=dia).first()

        if not agenda or not agenda.abierto:
            return False

        if agenda.horaApertura > horaInicio or agenda.horaCierre < horaFin:
            return False

        mes = date.today().month
        if 9 <= mes or mes == 1:
            periodo = Periodo.PRIMER_CUATRIMESTRE
        elif 2 <= mes <= 5:
            periodo = Periodo.SEGUNDO_CUATRIMESTRE
        else:
            periodo = Periodo.ANUAL
        
        if periodo == Periodo.ANUAL:
            periodos_a_revisar = [Periodo.PRIMER_CUATRIMESTRE, Periodo.SEGUNDO_CUATRIMESTRE, Periodo.ANUAL]
        else:
            periodos_a_revisar = [periodo, Periodo.ANUAL]

        conflictos = Sesion.objects.filter(
            actividad__instalacion=self,
            actividad__periodo__in=periodos_a_revisar,
            dia__iexact=dia,
            horaInicio__lt=horaFin,
            horaFin__gt=horaInicio
        )

        if self.tipoInstalacion == TipoInstalacion.PISCINA:
            conflictos = conflictos.filter(calle=calle)

        if sesion_id and sesion_id != -1:
            conflictos = conflictos.exclude(id=sesion_id)

        if conflictos.exists():
            return False

        return True

    # Función para controlar el cambio de horario de una sesion en la instalación
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

    # Función para controlar si se puede realizar un alquiler en el preiodo seleccionado
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

    # Función para cambiar el horario de la instalación siempre y cuando no haya actividades programadas
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

    # Función para cambiar el horario especial de la instalación siempre y cuando no haya actividades programadas
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

    # Función para devolver el horario de una isntalación en una fecha concreta
    def getHorario(self, fecha):
        agenda = Agenda.objects.filter(instalacion=self, fecha=fecha).first()

        if agenda and agenda.abierto:
            return agenda.horaApertura, agenda.horaCierre

        return None, None

    # Función para obtener las reservas de una instalación en una fecha concreta
    def getReservas(self, fecha):
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

    # FUnción para contar el número de instalaciones en el sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para buscar en el sistema instalaciones que cumplan con los filtros y el texto
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