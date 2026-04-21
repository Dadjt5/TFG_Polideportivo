from django.test import TestCase
from datetime import time, date
from django.db import IntegrityError
from django.contrib.auth import get_user_model


from ..models import (
    Actividad, ActividadComun, Fisioterapia, GrupoReducido, 
    Sesion, TarifaActividad, TipoActividad, Asistencia, Periodo,
    Pabellon, Monitor, Instalacion, UsuarioFinal
)

User = get_user_model()


class ActividadTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="monitor1", password="1234")
        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(nombre="polideportivo", pabellon=self.pabellon)
        self.monitor = Monitor.objects.create(user=user)

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            año=2026,
            tipoActividad=TipoActividad.OTROS,
            instalacion=self.instalacion,
            monitor=self.monitor
        )

    # ---------------- CREACIÓN Y STR ----------------

    def test_creacion(self):
        self.assertEqual(self.actividad.nombre, "Yoga")

    def test_str(self):
        texto = str(self.actividad)

        self.assertIn("Yoga", texto)
        self.assertIn(self.instalacion.nombre, texto)


    # ---------------- CONTAR ----------------

    def test_contar(self):
        Actividad.objects.create(
            nombre="Pilates",
            año=2026,
            instalacion=self.instalacion,
            monitor=self.monitor        
        )

        self.assertEqual(Actividad.contar(), 2)


    # ---------------- TARIFA DE ACTIVIDAD COMÚN ----------------

    def test_obtener_precios_actividad_comun(self):
        tarifa = TarifaActividad.objects.create()
        actividad_comun = ActividadComun.objects.create(
            tarifaactividad_ptr=tarifa,
            precioUAM=10,
            precioOtros=20,
            numeroHorasSemana=2
        )

        actividad = Actividad.objects.create(
            nombre="Yoga",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor,
            tarifa=tarifa,
            tipoActividad=TipoActividad.OTROS
        )

        precios = actividad.obtenerPrecios()

        self.assertEqual(precios["precioUAM"], 10)
        self.assertEqual(precios["precioOtros"], 20)

    def test_calcular_precio_base_actividad_comun(self):
        tarifa = TarifaActividad.objects.create()
        ActividadComun.objects.create(
            tarifaactividad_ptr=tarifa,
            precioUAM=10,
            precioOtros=20,
            numeroHorasSemana=2
        )

        actividad = Actividad.objects.create(
            nombre="Yoga",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor,
            tarifa=tarifa,
            tipoActividad=TipoActividad.OTROS
        )

        # Simulamos 2 horas de sesiones
        actividad.calcularHorasSemanales = lambda: 2

        user = User.objects.create(username="user1", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1), esUAM=True)

        precio = actividad._calcular_precio_base(usuario)

        self.assertEqual(precio, 10)


    # ---------------- GRUPO REDUCIDO ----------------

    def test_calcular_precio_grupo_reducido(self):
        tarifa = TarifaActividad.objects.create()
        GrupoReducido.objects.create(
            tarifaactividad_ptr=tarifa,
            numeroHoras=2,
            numeroPersonas=2,
            precio=100,
            precioMensual=50,
            precioCuatrimestre=200
        )

        actividad = Actividad.objects.create(
            nombre="Padel",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor,
            tarifa=tarifa,
            tipoActividad=TipoActividad.GRUPOS_REDUCIDOS
        )

        user = User.objects.create(username="user1", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))

        precio = actividad._calcular_precio_base(
            usuario,
            numeroHorasSemana=2,
            numeroPersonas=2,
            tipoPago="mensual"
        )

        self.assertEqual(precio, 50)


    # ---------------- FISIOTERAPIA ----------------

    def test_calcular_precio_fisioterapia_uam(self):
        tarifa = TarifaActividad.objects.create()
        Fisioterapia.objects.create(
            tarifaactividad_ptr=tarifa,
            precioConsultaUAM=30,
            precioConsultaOtros=50
        )

        actividad = Actividad.objects.create(
            nombre="Fisios",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor,
            tarifa=tarifa,
            tipoActividad=TipoActividad.FISIOTERAPIA
        )

        user = User.objects.create(username="user1", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1), esUAM=True)

        precio = actividad._calcular_precio_base(
            usuario,
            tipoSesion="consulta"
        )

        self.assertEqual(precio, 30)

    def test_tipo_actividad_invalido(self):
        actividad = Actividad.objects.create(
            nombre="Test",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor,
            tipoActividad="INVALIDO"
        )

        user = User.objects.create(username="user1", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))

        with self.assertRaises(ValueError):
            actividad._calcular_precio_base(usuario)


    # ---------------- SESIONES ----------------

    def test_calcular_horas_semanales(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia="lunes",
            horaInicio=time(10, 0),
            horaFin=time(12, 0)
        )

        horas = self.actividad.calcularHorasSemanales()
        self.assertEqual(horas, 2)

    def test_get_horario(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia="lunes",
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        horario = self.actividad.getHorario()
        self.assertEqual(len(horario), 1)
        self.assertEqual(horario[0]["dia"], "lunes")

    def test_get_dias(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia="martes",
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        dias = self.actividad.getDias()
        self.assertIn("martes", dias[0])

    def test_nueva_sesion(self):
        sesion = self.actividad.nuevaSesion("lunes", "10:00", "11:00")

        self.assertEqual(sesion.horaInicio.hour, 10)
        self.assertEqual(sesion.horaFin.hour, 11)


    # ---------------- MODIFICAR INFORMACIÓN ----------------

    def test_modificar_informacion_correcto(self):
        data = {
            "nombre": "Yoga Avanzado",
            "plazasMaximas": 30,
            "plazasReservadas": 10
        }

        resultado = self.actividad.modificarInformacion(
            actividad_data=data,
            tarifa=None,
            instalacion=self.instalacion,
            monitor=self.monitor,
            imagen=None
        )

        self.assertTrue(resultado)
        self.assertEqual(self.actividad.nombre, "Yoga Avanzado")

    def test_modificar_informacion_error_plazas(self):
        data = {
            "plazasMaximas": 10,
            "plazasReservadas": 20
        }

        resultado = self.actividad.modificarInformacion(
            actividad_data=data,
            tarifa=None,
            instalacion=self.instalacion,
            monitor=self.monitor,
            imagen=None
        )

        self.assertFalse(resultado)


    # ---------------- BUSCADOR ----------------

    def test_buscar_por_nombre(self):
        Actividad.objects.create(
            nombre="Pilates",
            año=2026,
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        res = Actividad.buscar(nombre="Yoga")
        self.assertEqual(res.count(), 1)

    def test_buscar_por_tipo(self):
        res = Actividad.buscar(tipo=[TipoActividad.OTROS])
        self.assertEqual(res.count(), 1)




class SesionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="monitor1", password="1234")
        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(pabellon=self.pabellon)
        self.monitor = Monitor.objects.create(user=user)

        user = User.objects.create(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor
        )


    # ---------------- CONTAR ----------------

    def test_contar(self):
        Sesion.objects.create(
            actividad=self.actividad,
            horaInicio=time(10,0),
            horaFin=time(12,0)
        )

        self.assertEqual(Sesion.contar(), 1)


    # ---------------- SAVE ----------------

    def test_save_numero_horas_valido(self):
        sesion = Sesion(
            actividad=self.actividad,
            horaInicio=time(10,0),
            horaFin=time(12,0)
        )
        sesion.save()
        self.assertEqual(sesion.numeroHoras, 2)

    def test_save_hora_fin_menor(self):
        sesion = Sesion(
            actividad=self.actividad,
            horaInicio=time(12,0),
            horaFin=time(10,0)
        )
        with self.assertRaises(ValueError):
            sesion.save()


    # ---------------- COMPROBAR PERIODO ----------------

    def test_comprobar_periodo_primer_cuatrimestre(self):
        self.actividad.periodo = Periodo.PRIMER_CUATRIMESTRE
        self.assertTrue(self.actividad.sesiones.create(
            horaInicio=time(10,0), horaFin=time(11,0)
        ).comprobarPeriodo(10))
        self.assertFalse(self.actividad.sesiones.create(
            horaInicio=time(10,0), horaFin=time(11,0)
        ).comprobarPeriodo(6))


    # ---------------- FALTAS ----------------

    def test_cambiar_falta_existente(self):
        sesion = Sesion.objects.create(
            actividad=self.actividad,
            horaInicio=time(10,0),
            horaFin=time(12,0)
        )
        asistencia = Asistencia.objects.create(usuarioFinal=self.usuario, sesion=sesion, presente=False)

        result = sesion.cambiarFalta(self.usuario, True)
        asistencia.refresh_from_db()
        self.assertTrue(result)
        self.assertTrue(asistencia.presente)

    def test_cambiar_falta_no_existente(self):
        sesion = Sesion.objects.create(
            actividad=self.actividad,
            horaInicio=time(10,0),
            horaFin=time(12,0)
        )
        result = sesion.cambiarFalta(self.usuario, True)
        self.assertFalse(result)



class AsistenciaTestCase(TestCase):    
    def setUp(self):
        user = User.objects.create(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))

        user = User.objects.create(username="monitor2", password="1234")
        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(nombre="polideportivo", pabellon=self.pabellon)
        self.monitor = Monitor.objects.create(user=user)


        self.actividad = Actividad.objects.create(
            nombre="Pilates",
            año=2025,
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        self.sesion = Sesion.objects.create(
            actividad=self.actividad,
            horaInicio="10:00",
            horaFin="12:00"
        )


    # ---------------- CREACION ----------------

    def test_crear_asistencia_valida(self):
        asistencia = Asistencia.objects.create(
            usuarioFinal=self.usuario,
            sesion=self.sesion,
            presente=False
        )
        self.assertEqual(asistencia.presente, False)
        self.assertEqual(asistencia.usuarioFinal, self.usuario)
        self.assertEqual(asistencia.sesion, self.sesion)


    # ---------------- DUPLICADOS Y RELACION ----------------

    def test_unicidad_usuario_sesion(self):
        Asistencia.objects.create(usuarioFinal=self.usuario, sesion=self.sesion)
        with self.assertRaises(IntegrityError):
            # Intentamos crear un duplicado para comprobar el meta: usuarioFinal, Sesion
            Asistencia.objects.create(usuarioFinal=self.usuario, sesion=self.sesion)

    def test_relaciones_fk(self):
        asistencia = Asistencia.objects.create(usuarioFinal=self.usuario, sesion=self.sesion)
        self.assertIn(asistencia, self.usuario.asistencias.all())
        self.assertIn(asistencia, self.sesion.asistencias.all())