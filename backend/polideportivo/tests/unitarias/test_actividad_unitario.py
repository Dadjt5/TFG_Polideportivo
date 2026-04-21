from datetime import time, date
from django.test import TestCase
from unittest.mock import patch
from django.http import Http404
from django.contrib.auth import get_user_model

from ...models import (
    Actividad, Sesion, Dia, Periodo, Pabellon, Instalacion,
    Monitor, TipoActividad, ActividadComun, GrupoReducido,
    Fisioterapia, UsuarioFinal
)

User = get_user_model()

class ActividadUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="monitor_test",
            password="1234"
        )

        self.user2 = User.objects.create_user(
            username="user_test",
            password="1234"
        )

        self.monitor = Monitor.objects.create(
            user=self.user,
            nombre="Monitor prueba"
        )
    
        self.usuario = UsuarioFinal.objects.create(
            user=self.user,
            fechaNacimiento=date(2001,1,1),
            nombre="Usuario prueba"
        )

        self.pabellon = Pabellon.objects.create(
            nombre="Pabellón central"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Pista tenis",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            plazasMaximas=20,
            instalacion=self.instalacion,
            monitor=self.monitor
        )

    def test_str(self):
        self.assertIn("Yoga", str(self.actividad))

    def test_contar(self):
        self.assertEqual(Actividad.contar(), 1)

    def test_calcular_horas_semanales(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 30)
        )

        self.assertEqual(
            self.actividad.calcularHorasSemanales(),
            2
        )

    def test_get_dias(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        dias = self.actividad.getDias()

        self.assertIn(Dia.LUNES, dias[0])

    def test_get_horario(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        horario = self.actividad.getHorario()
        self.assertEqual(horario[0]["horaInicio"], "10:00")
    
    def test_obtener_precios_otros(self):
        self.actividad.tipoActividad = TipoActividad.OTROS
        tarifa = ActividadComun.objects.create(precioUAM=10, precioOtros=20, numeroHorasSemana=2)
        self.actividad.tarifa = tarifa

        self.usuario.esUAM = True

        precios = self.actividad.obtenerPrecios()
        self.assertEqual(precios["precioUAM"], 10)
    
        resultado = self.actividad._calcular_precio_base(self.usuario)
        self.assertIsInstance(resultado, float)
    
    def test_obtener_precios_otros_fallo(self):
        self.actividad.tipoActividad = TipoActividad.OTROS
        tarifa = ActividadComun.objects.create(precioUAM=10, precioOtros=20, numeroHorasSemana=0)
        self.actividad.tarifa = tarifa
    
        with self.assertRaises(ValueError):
            self.actividad._calcular_precio_base(self.usuario)

    def test_obtener_precios_grupos_reducidos(self):
        self.actividad.tipoActividad = TipoActividad.GRUPOS_REDUCIDOS
        tarifa = GrupoReducido.objects.create(numeroHoras=2, numeroPersonas=2, precio=100, precioCuatrimestre=80, precioMensual=50)
        self.actividad.tarifa = tarifa

        precios = self.actividad.obtenerPrecios()
        self.assertEqual(precios["precio"], 100)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoPago="cuatrimestral")
        self.assertIsInstance(resultado, float)

    def test_obtener_precios_grupos_reducidos_mensual(self):
        self.actividad.tipoActividad = TipoActividad.GRUPOS_REDUCIDOS
        tarifa = GrupoReducido.objects.create(numeroHoras=2, numeroPersonas=2, precio=100, precioCuatrimestre=80, precioMensual=50)
        self.actividad.tarifa = tarifa

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoPago="mensual")
        self.assertIsInstance(resultado, float)

    def test_obtener_precios_grupos_reducidos_error(self):
        self.actividad.tipoActividad = TipoActividad.GRUPOS_REDUCIDOS
        tarifa = GrupoReducido.objects.create(numeroHoras=0, numeroPersonas=0, precio=100, precioCuatrimestre=80, precioMensual=50)
        self.actividad.tarifa = tarifa

        with self.assertRaises(ValueError):
            self.actividad._calcular_precio_base(self.usuario)
    
    def test_obtener_precios_fisioterapia(self):
        self.actividad.tipoActividad = TipoActividad.FISIOTERAPIA
        tarifa = Fisioterapia.objects.create(
            precioConsultaTDA=1,
            precioConsultaUAM=2,
            precioConsultaOtros=3,
            precioSesiones1_5TDA=4,
            precioSesiones1_5UAM=5,
            precioSesiones1_5Otros=6,
            precioSesiones6TDA=7,
            precioSesiones6UAM=8,
            precioSesiones6Otros=9
        )
        self.actividad.tarifa = tarifa

        self.usuario.tieneTDA = True
        self.usuario.esUAM = False

        precios = self.actividad.obtenerPrecios()
        self.assertEqual(precios["precioConsultaTDA"], 1)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="consulta")
        self.assertEqual(resultado, 1)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="sesiones1_5")
        self.assertEqual(resultado, 4)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="sesiones6")
        self.assertEqual(resultado, 7)
    
    def test_obtener_precios_fisioterapia_ninguno(self):
        self.actividad.tipoActividad = TipoActividad.FISIOTERAPIA
        tarifa = Fisioterapia.objects.create(
            precioConsultaTDA=1,
            precioConsultaUAM=2,
            precioConsultaOtros=3,
            precioSesiones1_5TDA=4,
            precioSesiones1_5UAM=5,
            precioSesiones1_5Otros=6,
            precioSesiones6TDA=7,
            precioSesiones6UAM=8,
            precioSesiones6Otros=9
        )
        self.actividad.tarifa = tarifa

        self.usuario.tieneTDA = False
        self.usuario.esUAM = False

        precios = self.actividad.obtenerPrecios()
        self.assertEqual(precios["precioConsultaTDA"], 1)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="consulta")
        self.assertEqual(resultado, 3)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="sesiones1_5")
        self.assertEqual(resultado, 6)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="sesiones6")
        self.assertEqual(resultado, 9)
    
    def test_obtener_precios_fisioterapia_fallo(self):
        self.actividad.tipoActividad = "invalido"
        tarifa = Fisioterapia.objects.create(
            precioConsultaTDA=1,
            precioConsultaUAM=2,
            precioConsultaOtros=3,
            precioSesiones1_5TDA=4,
            precioSesiones1_5UAM=5,
            precioSesiones1_5Otros=6,
            precioSesiones6TDA=7,
            precioSesiones6UAM=8,
            precioSesiones6Otros=9
        )

        self.actividad.tarifa = tarifa

        with self.assertRaises(ValueError):
            self.actividad._calcular_precio_base(self.usuario)
    
    def test_obtener_precios_fisioterapia_uam(self):
        self.actividad.tipoActividad = TipoActividad.FISIOTERAPIA
        tarifa = Fisioterapia.objects.create(
            precioConsultaTDA=1,
            precioConsultaUAM=2,
            precioConsultaOtros=3,
            precioSesiones1_5TDA=4,
            precioSesiones1_5UAM=5,
            precioSesiones1_5Otros=6,
            precioSesiones6TDA=7,
            precioSesiones6UAM=8,
            precioSesiones6Otros=9
        )

        self.actividad.tarifa = tarifa
        self.usuario.esUAM = True

        precios = self.actividad.obtenerPrecios()
        self.assertEqual(precios["precioConsultaTDA"], 1)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="consulta")
        self.assertEqual(resultado, 2)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="sesiones1_5")
        self.assertEqual(resultado, 5)

        resultado = self.actividad._calcular_precio_base(self.usuario, tipoSesion="sesiones6")
        self.assertEqual(resultado, 8)

    def test_obtener_precios_tipo_invalido(self):
        self.actividad.tipoActividad = "INVALIDO"
        self.actividad.tarifa = None

        with self.assertRaises(Http404):
            self.actividad.obtenerPrecios()
        
    def test_buscar_por_nombre(self):
        Actividad.objects.create(
            nombre="Futbol",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        res = Actividad.buscar(nombre="Fut")

        self.assertTrue(res.exists())
    
    def test_buscar_por_dia(self):
        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.MARTES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        res = Actividad.buscar(dias=[Dia.MARTES])

        self.assertTrue(res.exists())
    
    def test_buscar_sin_filtros(self):
        res = Actividad.buscar()

        self.assertTrue(res.exists())

    def test_buscar_por_nombre(self):
        Actividad.objects.create(
            nombre="Futbol sala",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        res = Actividad.buscar(nombre="Futbol")

        self.assertTrue(res.exists())
    
    def test_buscar_por_tipo(self):
        self.actividad.tipoActividad = TipoActividad.OTROS
        self.actividad.save()

        res = Actividad.buscar(tipo=[TipoActividad.OTROS])

        self.assertTrue(res.exists())

    def test_buscar_por_hora_inicio(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(9, 0),
            horaFin=time(10, 0)
        )

        res = Actividad.buscar(horaInicio=time(10, 0))

        self.assertTrue(res.exists())
    
    def test_buscar_por_hora_fin(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(12, 0)
        )

        res = Actividad.buscar(horaFin=time(11, 0))

        self.assertTrue(res.exists())


class SesionUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="monitor_test",
            password="1234"
        )

        self.monitor = Monitor.objects.create(
            user=self.user,
            nombre="Monitor prueba"
        )

        self.pabellon = Pabellon.objects.create(
            nombre="Pabellón central"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Pista tenis",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Pilates",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

    def test_str(self):
        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertIn("Sesion", str(sesion))

    def test_comprobar_periodo(self):
        self.actividad.periodo = Periodo.PRIMER_CUATRIMESTRE
        self.actividad.save()

        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertTrue(sesion.comprobarPeriodo(10))
        self.assertFalse(sesion.comprobarPeriodo(6))
    
    def test_comprobar_periodo_segundo(self):
        self.actividad.periodo = Periodo.SEGUNDO_CUATRIMESTRE
        self.actividad.save()

        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertTrue(sesion.comprobarPeriodo(4))
        self.assertFalse(sesion.comprobarPeriodo(6))

    def test_comprobar_periodo_tercero(self):
        self.actividad.periodo = Periodo.TERCER_CUATRIMESTRE
        self.actividad.save()

        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertTrue(sesion.comprobarPeriodo(7))
        self.assertFalse(sesion.comprobarPeriodo(2))

    def test_save_calcula_numero_horas(self):
        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 30)
        )

        self.assertEqual(sesion.numeroHoras, 1.5)

    def test_save_hora_invalida(self):
        with self.assertRaises(ValueError):
            Sesion.objects.create(
                actividad=self.actividad,
                dia=Dia.LUNES,
                horaInicio=time(12, 0),
                horaFin=time(11, 0)
            )
    
    def test_modificar_informacion_ok(self):
        data = {
            "nombre": "Nuevo nombre",
            "plazasMaximas": 30,
            "plazasReservadas": 10
        }

        result = self.actividad.modificarInformacion(
            actividad_data=data,
            tarifa=self.actividad.tarifa,
            instalacion=self.instalacion,
            monitor=self.monitor,
            imagen=None
        )

        self.assertTrue(result)
        self.actividad.refresh_from_db()
        self.assertEqual(self.actividad.nombre, "Nuevo nombre")
    
    def test_modificar_informacion_error_plazas(self):
        data = {
            "plazasMaximas": 5,
            "plazasReservadas": 10
        }

        result = self.actividad.modificarInformacion(
            actividad_data=data,
            tarifa=self.actividad.tarifa,
            instalacion=self.instalacion,
            monitor=self.monitor,
            imagen=None
        )

        self.assertFalse(result)
    
    def test_modificar_informacion_error_plazas_max_vs_reservadas(self):
        self.actividad.plazasReservadas = 10
        self.actividad.save()

        data = {
            "plazasMaximas": 5,
            "plazasReservadas": 5
        }

        result = self.actividad.modificarInformacion(
            actividad_data=data,
            tarifa=self.actividad.tarifa,
            instalacion=self.instalacion,
            monitor=self.monitor,
            imagen=None
        )

        self.assertFalse(result)

    def test_get_dias_formato(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        dias = self.actividad.getDias()

        self.assertIsInstance(dias, tuple)

    def test_cambiar_falta_usuario_no_existe(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        resultado = self.actividad.sesiones.first().cambiarFalta(
            usuarioFinal=self.user,
            falta=False
        )

        self.assertFalse(resultado)
    
    def test_save_con_string(self):
        sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio="10:00",
            horaFin="11:00"
        )

        self.assertEqual(sesion.numeroHoras, 1.0)
    
    def test_contar_multiples_sesiones(self):
        Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.MARTES,
            horaInicio=time(12, 0),
            horaFin=time(13, 0)
        )

        self.assertEqual(Sesion.contar(), 1)