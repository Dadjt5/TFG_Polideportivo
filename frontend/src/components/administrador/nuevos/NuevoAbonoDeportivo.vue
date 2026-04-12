<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newSportSubscription }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
          style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.nombre }"
                   v-model="abono.nombre" />
          </div>

          <!-- MESES -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.months }}</label>
            <input type="number" min="1" class="form-control form-control-lg"
                   v-model.number="abono.meses" :class="{ 'is-invalid': errores.meses }"/>
          </div>

          <!-- PRECIO MENSUAL UAM -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.monthlyPriceUAM }}</label>
            <input type="number" step="0.01" min="0" class="form-control form-control-lg"
                   v-model.number="abono.precioTotalMensual" :class="{ 'is-invalid': errores.precioTotalMensual }"/>
          </div>

          <!-- PRECIOS -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.totalPriceUAM }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   v-model.number="abono.precioPagoUnicoUAM" :class="{ 'is-invalid': errores.precioPagoUnicoUAM }"/>
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.familyPrice }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   v-model.number="abono.precioFamiliar" :class="{ 'is-invalid': errores.precioFamiliar }"/>
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.monthlyPriceOthers }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   v-model.number="abono.precioTotalMensualOtros" :class="{ 'is-invalid': errores.precioTotalMensualOtros }"/>
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.totalPriceOthers }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   v-model.number="abono.precioPagoUnicoOtros" :class="{ 'is-invalid': errores.precioPagoUnicoOtros }"/>
          </div>

          <!-- DESCUENTOS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.firstActivityDiscount }} (%)</label>
            <input type="number" step="0.1" class="form-control form-control-lg"
                   v-model.number="abono.descuentoPrimeraActividad" :class="{ 'is-invalid': errores.descuentoPrimeraActividad }"/>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.otherActivitiesDiscount }} (%)</label>
            <input type="number" step="0.1" class="form-control form-control-lg"
                   v-model.number="abono.descuentoRestoActividades" :class="{ 'is-invalid': errores.descuentoRestoActividades }"/>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.outdoorDiscount }} (%)</label>
            <input type="number" step="0.1" class="form-control form-control-lg"
                   v-model.number="abono.descuentoActividadesExteriores" :class="{ 'is-invalid': errores.descuentoActividadesExteriores }"/>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.rentDiscount }} (%)</label>
            <input type="number" step="0.1" class="form-control form-control-lg"
                   v-model.number="abono.descuentoAlquileres" :class="{ 'is-invalid': errores.descuentoAlquileres }"/>
          </div>
        </div>

        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearAbono">
            {{ t.createSportSubscription }}
          </button>

          <button class="btn btn-outline-secondary btn-lg px-5 rounded-pill shadow-sm" @click="volver">
            {{ t.return }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { type Ref, ref, inject } from "vue"
import { useRouter } from "vue-router"

import { nuevoAbonoDeportivo } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()

const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const abono = ref({
  nombre: "",
  meses: 1,
  descuentoPrimeraActividad: 0,
  descuentoRestoActividades: 0,
  descuentoActividadesExteriores: 0,
  precioTotalMensual: 0,
  precioPagoUnicoUAM: 0,
  precioFamiliar: 0,
  precioTotalMensualOtros: 0,
  precioPagoUnicoOtros: 0,
  descuentoAlquileres: 0
})

const errores = ref({
  nombre: false,
  meses: false,
  descuentoPrimeraActividad: false,
  descuentoRestoActividades: false,
  descuentoActividadesExteriores: false,
  precioTotalMensual: false,
  precioPagoUnicoUAM: false,
  precioFamiliar: false,
  precioTotalMensualOtros: false,
  precioPagoUnicoOtros: false,
  descuentoAlquileres: false
})

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function validar() {
  let valido = true

  errores.value.nombre = abono.value.nombre === ""
  errores.value.precioTotalMensual = abono.value.precioTotalMensual <= 0
  errores.value.precioPagoUnicoUAM = abono.value.precioPagoUnicoUAM <= 0
  errores.value.precioFamiliar = abono.value.precioFamiliar <= 0
  errores.value.precioTotalMensualOtros = abono.value.precioTotalMensualOtros <= 0
  errores.value.precioPagoUnicoOtros = abono.value.precioPagoUnicoOtros <= 0
  errores.value.meses = abono.value.meses <= 0

  errores.value.descuentoPrimeraActividad = 
    abono.value.descuentoPrimeraActividad <= 0 || abono.value.descuentoPrimeraActividad > 100

  errores.value.descuentoRestoActividades = 
    abono.value.descuentoRestoActividades <= 0 || abono.value.descuentoRestoActividades > 100

  errores.value.descuentoActividadesExteriores = 
    abono.value.descuentoActividadesExteriores <= 0 || abono.value.descuentoActividadesExteriores > 100

  errores.value.descuentoAlquileres = 
    abono.value.descuentoAlquileres <= 0 || abono.value.descuentoAlquileres > 100

	for (const key in errores.value) {
		if (errores.value[key]) valido = false
	}

	return valido
}

const crearAbono = async () => {
  if (!validar()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  try {
    await nuevoAbonoDeportivo(abono.value)
    router.back()
  } catch(e) {
    lanzarMensaje(t.value.subscriptionNoCreated, "error")
    console.error("Error al crear el abono deportivo", e);
  }
}

const volver = () => router.back()
</script>