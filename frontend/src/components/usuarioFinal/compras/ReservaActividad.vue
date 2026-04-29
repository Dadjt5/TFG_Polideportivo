<template>
  <div class="min-vh-100 d-flex justify-content-center position-relative overflow-hidden"
    style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <!-- Fondo decorativo -->
    <div class="position-absolute top-0 start-0 w-100 h-100 opacity-25"
      style="background:
        radial-gradient(circle at 20% 20%, #0072ff55, transparent 40%),
        radial-gradient(circle at 80% 70%, #ff7a0055, transparent 40%);">
    </div>

    <div class="container py-4">

      <!-- Título -->
      <div class="text-center mt-4 mb-4">
        <h2 class="fw-bold">{{ t.activityBookingTitle }}</h2>
        <p class="text-muted">{{ t.activityBookingSubtitle }}</p>
      </div>

      <!-- Información actividad -->
      <div class="card shadow-sm rounded-4 mb-4"
        style="backdrop-filter: blur(6px); background: rgba(255,255,255,0.85);">
        <div class="card-body">
          <h5 class="fw-bold mb-3 fs-3">{{ reserva.tarifa.nombre }}</h5>

          <div v-if="reserva.tarifa.horario.length">
            <div
              v-for="(h,index) in reserva.tarifa.horario"
              :key="index"
              class="d-flex justify-content-between border-bottom py-2">
              <span>{{ h.dia }}</span>
              <span class="text-primary">{{ h.horaInicio }} - {{ h.horaFin }}</span>
            </div>
          </div>

          <p v-else class="text-muted mb-0">
            {{ t.noSession }}
          </p>
        </div>
      </div>

      <!-- Tarifas -->
      <div class="card shadow-sm rounded-4"
        style="backdrop-filter: blur(6px); background: rgba(255,255,255,0.85);">
        <div class="card-body">

          <h5 class="fw-bold mb-3">{{ t.tariff }}</h5>

          <!-- OTROS -->
          <table v-if="reserva.tarifa.tipo === 'Otros'" class="table table-sm mb-4">
            <tbody>
              <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
                <td>UAM</td>
                <td class="text-end">{{ reserva.tarifa.datos.precioUAM }} € / {{ reserva.tarifa.datos.numeroHorasSemana }} {{ t.weekHours }}</td>
              </tr>
              <tr :class="{ 'table-primary': !usuarioFinalStore.isUAM }">
                <td>{{ t.others }}</td>
                <td class="text-end">{{ reserva.tarifa.datos.precioOtros }} € / {{ reserva.tarifa.datos.numeroHorasSemana }} {{ t.weekHours }}</td>
              </tr>
            </tbody>
          </table>

          <!-- GRUPOS REDUCIDOS -->
          <div v-else-if="reserva.tarifa.tipo === 'Grupos reducidos'">
            <div class="mb-3">
              <label class="form-label">{{ t.people }}</label>
              <input
                type="number"
                class="form-control"
                v-model.number="reserva.seleccion.personas"
                :min="1"
                :max="reserva.tarifa.datos.numeroPersonas"
              />
            </div>

            <div class="mb-3">
              <label class="form-label">{{ t.paymentMethod }}</label>
              <select class="form-select" v-model="reserva.seleccion.modalidad">
                <option value="Pago mensual">{{ t.monthly }}</option>
                <option value="Pago cuatrimestral">{{ t.quarterly }}</option>
                <option value="Pago unico">{{ t.fullPayment }}</option>
              </select>
            </div>

            <table class="table table-sm mb-4">
              <tbody>
                <tr>
                  <td>{{ t.monthly }}</td>
                  <td class="text-end">{{ reserva.tarifa.datos.precioMensual }} € / {{ reserva.tarifa.datos.numeroPersonas }} {{ t.people }} * {{ reserva.tarifa.datos.numeroHoras }} {{ t.weekHours }}</td>
                </tr>
                <tr>
                  <td>{{ t.quarterly }}</td>
                  <td class="text-end">{{ reserva.tarifa.datos.precioCuatrimestre }} € / {{ reserva.tarifa.datos.numeroPersonas }} {{ t.people }} * {{ reserva.tarifa.datos.numeroHoras }} {{ t.weekHours }}</td>
                </tr>
                <tr>
                  <td>{{ t.fullPayment }}</td>
                  <td class="text-end">{{ reserva.tarifa.datos.precio }} € / {{ reserva.tarifa.datos.numeroPersonas }} {{ t.people }} * {{ reserva.tarifa.datos.numeroHoras }} {{ t.weekHours }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- FISIOTERAPIA -->
          <div v-else-if="reserva.tarifa.tipo === 'Fisioterapia'">
            <div class="mb-3">
              <label class="form-label">{{ t.sessionType }}</label>
              <select class="form-select" v-model="reserva.seleccion.tipoSesion">
                <option value="consulta">{{ t.initialConsultation }}</option>
                <option value="sesiones">{{ t.sessions }}</option>
              </select>
            </div>

            <div
              v-if="reserva.seleccion.tipoSesion === 'sesiones'"
              class="alert alert-info py-2">
              {{ t.fisioSessionNotice }} {{ t.heldSessions }}: {{ reserva.tarifa.numeroSesiones }}
            </div>

            <table class="table table-sm mb-4">
              <tbody>
                <tr :class="{ 'table-primary': usuarioFinalStore.hasTda }">
                  <td>TDA</td>
                  <td class="text-end">{{ precioFisioTDA }} €</td>
                </tr>
                <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
                  <td>UAM</td>
                  <td class="text-end">{{ precioFisioUAM }} €</td>
                </tr>
                <tr :class="{ 'table-primary': !usuarioFinalStore.isUAM && !usuarioFinalStore.hasTda }">
                  <td>{{ t.others }}</td>
                  <td class="text-end">{{ precioFisioOtros }} €</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Descuentos -->
          <div v-if="reserva.descuento.aplicados.length" class="alert alert-success py-2">
            <div class="fw-bold mb-1">
              {{ t.discount }}: {{ reserva.descuento.porcentaje_total }}%
            </div>
            <ul class="mb-0 ps-3">
              <li v-for="descuento in reserva.descuento.aplicados" :key="descuento.id">
                {{ descuento.nombre }} ({{ descuento.porcentaje }}%)
              </li>
            </ul>
          </div>

          <!-- Total -->
          <div class="border-top pt-3 mt-3">
            <div class="d-flex justify-content-between">
              <span class="text-muted">{{ t.basePrice }}</span>
              <span>{{ precioBase.toFixed(2) }} €</span>
            </div>

            <div class="d-flex justify-content-between mt-2">
              <span class="fw-bold">{{ t.finalPrice }}</span>
              <span class="fw-bold text-success">{{ total.toFixed(2) }} €</span>
            </div>
          </div>

          <!-- Mensajes -->
          <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
            <div class="alert"
              :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
              {{ mensaje }}
            </div>
          </div>

          <!-- Acciones -->
          <div class="d-flex justify-content-end mt-4 gap-2">
            <button class="btn btn-outline-secondary" @click="cancelar">
              {{ t.cancel }}
            </button>
            <button class="btn btn-primary" @click="continuarPago">
              {{ t.payContinue }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, type Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { getTarifaDescuentoActividad, reservarActividad } from '@/services/reservaPagoService';

import { useUserStore } from '@/stores/usuarioFinal'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();
const mensaje = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const reserva = ref({
  tarifa: {
    idActividad: 0,
    nombre: '',
    numeroHoras: 0,
    numeroSesiones: 0,
    horario: [] as {
      dia: '',
      horaInicio: '',
      horaFin: ''
    }[],
    tipo: '',
    datos: {} as any
  },
  seleccion: {
    personas: 1,
    modalidad: 'Pago unico',
    tipoSesion: 'consulta'
  },
  descuento: {
    porcentaje_total: 0,
    aplicados: [] as {
      id: number
      nombre: string
      porcentaje: number
    }[]
  }
})

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function obtenerPrecioComun(precios: any) {
  let precio = precios.precioOtros;
  if (usuarioFinalStore.isUAM) {
    precio = precios.precioUAM;
  }

  const horas = reserva.value.tarifa.numeroHoras;
  const mult = horas / precios.numeroHorasSemana;

  return precio * mult;
}

function obtenerPrecioGrupo(precios: any, sel: any) {
  let precio = precios.precio;
  if (sel.modalidad == "Pago mensual") {
    precio = precios.precioMensual;
  } else if (sel.modalidad == "Pago cuatrimestral") {
    precio = precios.precioCuatrimestre
  }

  // Necesitamos calcular cuanto debe subir el precio o bajar en relacion a los parametros definidos en la tarifa
  const horas = reserva.value.tarifa.numeroHoras;
  const mult1 = horas / precios.numeroHoras;
  const mult2 = sel.personas / precios.numeroPersonas;

  return precio * mult1 * mult2;
}

const precioFisioUAM = ref(0)
const precioFisioTDA = ref(0)
const precioFisioOtros = ref(0)

function obtenerPrecioFisioterapia(precios: any, sel: any) {
  let precio = 0;

  if (sel.tipoSesion == "consulta") {
    precioFisioUAM.value = precios.precioConsultaUAM;
    precioFisioTDA.value = precios.precioConsultaTDA;
    precioFisioOtros.value = precios.precioConsultaOtros;

    precio = precios.precioConsultaOtros;
    if (usuarioFinalStore.hasTda) {
      precio = precios.precioConsultaTDA;
    } else if (usuarioFinalStore.isUAM) {
      precio = precios.precioConsultaUAM;
    }
  } else if (sel.tipoSesion == "sesiones") {
    precioFisioUAM.value = precios.precioSesionesUAM;
    precioFisioTDA.value = precios.precioSesionesTDA;
    precioFisioOtros.value = precios.precioSesionesOtros;

    precio = precios.precioSesionesOtros;
    if (usuarioFinalStore.hasTda) {
      precio = precios.precioSesionesTDA;
    } else if (usuarioFinalStore.isUAM) {
      precio = precios.precioSesionesUAM;
    }
  }

  return precio
}

const precioBase = computed(() => {
  const tipo = reserva.value.tarifa.tipo;
  const datos = reserva.value.tarifa.datos;
  const sel = reserva.value.seleccion;

  if (tipo === 'Otros') {
    return obtenerPrecioComun(datos);
  }

  if (tipo === 'Grupos reducidos') {
    return obtenerPrecioGrupo(datos, sel)
  }

  if (tipo === 'Fisioterapia') {
    return obtenerPrecioFisioterapia(datos, sel)
  }

  return 0
})

const total = computed(() => {
  const base = precioBase.value
  const descuento = (base * reserva.value.descuento.porcentaje_total) / 100
  return base - descuento
})

const continuarPago = async () => {
  try {
    const response = await reservarActividad(
      reserva.value.tarifa.idActividad,
      reserva.value.seleccion.personas,
      reserva.value.seleccion.modalidad,
      reserva.value.seleccion.tipoSesion
    )

    const idPago = response.idPago

    router.push({
      name: 'pasarela-pago',
      params: { tipo: "reserva_actividad", id: idPago }
    })
  } catch (e) {
    lanzarMensaje(t.value.noActivityReservation, "error")
    console.error("Error al reservar la actividad", e)
  }
}

function cancelar() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id);
  const data = await getTarifaDescuentoActividad(id)

  reserva.value.tarifa = data.tarifa
  reserva.value.descuento = data.descuento
});
</script>
