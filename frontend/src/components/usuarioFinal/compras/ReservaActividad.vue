<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-4">

      <!-- Cabecera -->
      <div class="text-center mb-4">
        <h2 class="fw-bold text-primary mb-1" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.15);">
          {{ t.activityBookingTitle }}
        </h2>
        <p class="text-muted">{{ t.activityBookingSubtitle }}</p>
      </div>

      <!-- Card principal -->
      <div class="rounded-3 shadow-sm p-4 card-hover" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
        <h5 class="fw-bold mb-3">{{ reserva.tarifa.nombre }}</h5>

        <!-- Horarios -->
        <ul class="list-group list-group-flush mb-4">
          <li v-if="reserva.tarifa.horario.length" v-for="(h, index) in reserva.tarifa.horario" :key="index"
              class="list-group-item d-flex justify-content-between align-items-center border-0 px-0 py-2">
            <span class="fw-semibold">
              <i class="bi bi-calendar-event me-2 text-muted"></i>{{ h.dia }}
            </span>
            <span class="badge bg-primary-subtle text-primary fw-semibold px-3 py-2 rounded-pill">
              <i class="bi bi-clock me-1"></i>{{ h.horaInicio }} – {{ h.horaFin }}
            </span>
          </li>
          <li v-else class="list-group-item border-0 px-0 py-2 text-muted fs-5">{{ t.noSession }}</li>
        </ul>

        <!-- Tarifas -->
        <h6 class="fw-bold mb-2">{{ t.tariff }}</h6>

        <!-- Tipo OTROS -->
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

        <!-- Tipo GRUPOS_REDUCIDOS -->
        <table v-else-if="reserva.tarifa.tipo === 'Grupos reducidos'" class="table table-sm mb-4 align-middle">
          <tbody>
            <tr>
              <td><i class="bi bi-people me-2"></i>{{ t.people }}</td>
              <td class="text-end" style="max-width: 120px">
                <input type="number" class="form-control form-control-sm text-end"
                       v-model.number="reserva.seleccion.personas"
                       :min="1" :max="reserva.tarifa.datos.numeroPersonas" />
              </td>
            </tr>
            <tr>
              <td><i class="bi bi-credit-card me-2"></i>{{ t.paymentMethod }}</td>
              <td class="text-end">
                <select class="form-select form-select-sm text-end" v-model="reserva.seleccion.modalidad">
                  <option value="Pago mensual">{{ t.monthly }}</option>
                  <option value="Pago cuatrimestral">{{ t.quarterly }}</option>
                  <option value="Pago unico">{{ t.fullPayment }}</option>
                </select>
              </td>
            </tr>
            <tr><td colspan="2"><hr class="my-2"></td></tr>
            <tr><td>{{ t.hours }}</td><td class="text-end">{{ reserva.tarifa.datos.numeroHoras }}</td></tr>
            <tr><td>{{ t.people }}</td><td class="text-end">{{ reserva.tarifa.datos.numeroPersonas }}</td></tr>
            <tr><td>{{ t.monthly }}</td><td class="text-end">{{ reserva.tarifa.datos.precioMensual }} €</td></tr>
            <tr><td>{{ t.quarterly }}</td><td class="text-end">{{ reserva.tarifa.datos.precioCuatrimestre }} €</td></tr>
            <tr class="table-light fw-bold"><td>{{ t.fullPayment }}</td><td class="text-end">{{ reserva.tarifa.datos.precio }} €</td></tr>
          </tbody>
        </table>

        <!-- Tipo FISIOTERAPIA -->
        <table v-else-if="reserva.tarifa.tipo === 'Fisioterapia'" class="table table-sm mb-4">
          <tbody>
            <tr>
              <td>{{ t.sessionType }}</td>
              <td class="text-end">
                <select class="form-select form-select-sm text-end" v-model="reserva.seleccion.tipoSesion">
                  <option value="consulta">{{ t.initialConsultation }}</option>
                  <option value="sesiones1_5">{{ t.sessions1to5 }}</option>
                  <option value="sesiones6">{{ t.sessions6plus }}</option>
                </select>
              </td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasTda }">
              <td>TDA</td><td class="text-end">{{ precioFisioTDA }} €</td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
              <td>UAM</td><td class="text-end">{{ precioFisioUAM }} €</td>
            </tr>
            <tr :class="{ 'table-primary': !usuarioFinalStore.isUAM && !usuarioFinalStore.hasTda }">
              <td>{{ t.others }}</td><td class="text-end">{{ precioFisioOtros }} €</td>
            </tr>
          </tbody>
        </table>

        <!-- Descuentos -->
        <div v-if="reserva.descuento.aplicados.length" class="alert alert-success py-2 rounded-3">
          <div class="fw-bold mb-1">{{ t.discount }}: {{ reserva.descuento.porcentaje_total }}%</div>
          <ul class="mb-0 ps-3">
            <li v-for="descuento in reserva.descuento.aplicados" :key="descuento.id">
              {{ descuento.nombre }} ({{ descuento.porcentaje }}%)
            </li>
          </ul>
        </div>

        <!-- Total -->
        <div class="border-top pt-3 mt-3">
          <div class="d-flex justify-content-between fs-5 fw-bold">
            <span>{{ t.price }}</span>
            <span>{{ total }} €</span>
          </div>
        </div>

        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensaje }}
          </div>
        </div>

        <!-- Botones -->
        <div class="d-flex justify-content-end gap-2 mt-4">
          <button class="btn btn-outline-secondary" @click="cancelar">{{ t.cancel }}</button>
          <button class="btn btn-primary" @click="continuarPago">{{ t.payContinue }}</button>
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

const props = defineProps<{id: string}>();

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
  } else if (sel.tipoSesion == "sesiones1_5") {
    precioFisioUAM.value = precios.precioSesiones1_5UAM;
    precioFisioTDA.value = precios.precioSesiones1_5TDA;
    precioFisioOtros.value = precios.precioSesiones1_5Otros;

    precio = precios.precioSesiones1_5Otros;
    if (usuarioFinalStore.hasTda) {
      precio = precios.precioSesiones1_5TDA;
    } else if (usuarioFinalStore.isUAM) {
        precio = precios.precioSesiones1_5UAM;
    }
  } else if (sel.tipoSesion == "sesiones6") {
    precioFisioUAM.value = precios.precioSesiones6UAM;
    precioFisioTDA.value = precios.precioSesiones6TDA;
    precioFisioOtros.value = precios.precioSesiones6Otros;

    precio = precios.precioSesiones6Otros;
    if (usuarioFinalStore.hasTda) {
      precio = precios.precioSesiones6TDA;
    } else if (usuarioFinalStore.isUAM) {
        precio = precios.precioSesiones6UAM;
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
  } catch(e) {
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
