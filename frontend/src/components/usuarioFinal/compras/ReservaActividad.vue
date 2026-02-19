<template>
  <div class="container py-4">

    <!-- TÍTULO -->
    <div class="text-center mb-4">
      <h2 class="fw-bold">{{ t.activityBookingTitle }}</h2>
      <p class="text-muted">
        {{ t.activityBookingSubtitle }}
      </p>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">

        <h5 class="fw-bold mb-3">{{ reserva.tarifa.nombre }}</h5>

        <ul class="list-group list-group-flush mb-4">

          <li v-if="reserva.tarifa.horario.length != 0" v-for="(h, index) in reserva.tarifa.horario" :key="index"
            class="list-group-item d-flex justify-content-between align-items-center">
            <!-- Días -->
            <span class="fw-semibold">
              <i class="bi bi-calendar-event me-2 text-muted"></i>
              {{ h.dia }}
            </span>

            <!-- Horario -->
            <span class="badge bg-primary-subtle text-primary fw-semibold px-3 py-2">
              <i class="bi bi-clock me-1"></i>
              {{ h.horaInicio }} – {{ h.horaFin }}
            </span>
          </li>

          <span v-else>
            <p class="fs-5">{{ t.noSession }}</p>
          </span>
        </ul>

        <!-- TARIFAS -->
        <h6 class="fw-bold mb-2">{{ t.tariff }}</h6>

        <table v-if="reserva.tarifa.tipo === 'OTROS'" class="table table-sm mb-4">
          <tbody>
            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
              <td>UAM</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioUAM }} € / {{ reserva.tarifa.datos.numeroHorasSemana }} {{ t.weekHours }}
              </td>
            </tr>

            <tr :class="{ 'table-primary': !usuarioFinalStore.isUAM }">
              <td>{{ t.other }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioOtros }} € / {{ reserva.tarifa.datos.numeroHorasSemana }} {{ t.weekHours }}
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="reserva.tarifa.tipo === 'GRUPOS_REDUCIDOS'" class="table table-sm mb-4 align-middle">
          <tbody>

            <tr>
              <td>
                <i class="bi bi-people me-2"></i>
                {{ t.people }}
              </td>

              <td class="text-end" style="max-width: 120px">
                <input type="number" class="form-control form-control-sm text-end"
                  v-model.number="reserva.seleccion.personas" :min="1" :max="reserva.tarifa.datos.numeroPersonas" />
              </td>
            </tr>

            <tr>
              <td>
                <i class="bi bi-credit-card me-2"></i>
                {{ t.paymentMethod }}
              </td>

              <td class="text-end">
                <select class="form-select form-select-sm text-end" v-model="reserva.seleccion.modalidad">
                  <option value="mensual">{{ t.monthly }}</option>
                  <option value="cuatrimestral">{{ t.quarterly }}</option>
                  <option value="total">{{ t.fullPayment }}</option>
                </select>
              </td>
            </tr>

            <tr>
              <td colspan="2">
                <hr class="my-2">
              </td>
            </tr>

            <tr>
              <td>{{ t.hours }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.numeroHoras }}
              </td>
            </tr>

            <tr>
              <td>{{ t.people }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.numeroPersonas }}
              </td>
            </tr>

            <tr>
              <td>{{ t.monthly }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioMensual }} €
              </td>
            </tr>

            <tr>
              <td>{{ t.quarterly }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioCuatrimestre }} €
              </td>
            </tr>

            <tr class="table-light fw-bold">
              <td>{{ t.fullPayment }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precio }} €
              </td>
            </tr>

          </tbody>
        </table>


        <table v-else-if="reserva.tarifa.tipo === 'FISIOTERAPIA'" class="table table-sm mb-4">
          <tbody>
            <tr>
              <td>
                {{ t.sessionType }}
              </td>

              <td class="text-end">
                <select class="form-select form-select-sm text-end" v-model="reserva.seleccion.tipoSesion">
                  <option value="consulta">{{ t.initialConsultation }}</option>
                  <option value="sesiones1_5">{{ t.sessions1to5 }}</option>
                  <option value="sesiones6">{{ t.sessions6plus }}</option>
                </select>
              </td>
            </tr>

            <tr :class="{ 'table-primary': usuarioFinalStore.hasTda }">
              <td>TDA</td>
              <td class="text-end">
                {{ precioFisioTDA }} €
              </td>
            </tr>

            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
              <td>UAM</td>
              <td class="text-end">
                {{ precioFisioUAM }} €
              </td>
            </tr>

            <tr :class="{ 'table-primary': !usuarioFinalStore.isUAM && !usuarioFinalStore.hasTda }">
              <td>{{ t.other }}</td>
              <td class="text-end">
                {{ precioFisioOtros }} €
              </td>
            </tr>
          </tbody>
        </table>

        <!-- DESCUENTOS -->
        <div v-if="reserva.descuento.aplicados.length" class="alert alert-success py-2">
          <div class="fw-bold mb-1">
            {{ t.discount }}:
            {{ reserva.descuento.porcentaje_total }}%
          </div>

          <ul class="mb-0 ps-3">
            <li v-for="descuento in reserva.descuento.aplicados" :key="descuento.id">
              {{ descuento.nombre }} ({{ descuento.porcentaje }}%)
            </li>
          </ul>
        </div>

        <!-- TOTAL -->
        <div class="border-top pt-3 mt-3">
          <div class="d-flex justify-content-between fs-5">
            <span class="fw-bold">{{ t.price }}</span>
            <span class="fw-bold">
              {{ total }} €
            </span>
          </div>
        </div>

        <div class="d-flex justify-content-end gap-2 mt-4">
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
    modalidad: 'total',
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
  if (sel.modalidad == "mensual") {
    precio = precios.precioMensual;
  } else if (sel.modalidad == "cuatrimestral") {
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

  if (tipo === 'OTROS') {
    return obtenerPrecioComun(datos);
  }

  if (tipo === 'GRUPOS_REDUCIDOS') {
    return obtenerPrecioGrupo(datos, sel)
  }

  if (tipo === 'FISIOTERAPIA') {
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
  const response = await reservarActividad(reserva.value.tarifa.idActividad)

  const idReserva = response.id

  router.push({
    name: 'pasarela-pago',
    query: { id: idReserva }
  })
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
