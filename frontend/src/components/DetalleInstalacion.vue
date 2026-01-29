<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <div class="text-center mt-4 mb-5">
        <h1 class="fw-semibold">{{ instalacion.nombre }}</h1>
      </div>

      <div class="row g-4">

        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h4 class="mb-3 d-flex align-items-center">
                <i class="bi bi-info-circle-fill text-primary me-2"></i>
                {{ t.facilityDetails }}
              </h4>

              <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning"
                @click.stop="cambiarFavorito">
                <i :class="[
                  'bi',
                  usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'bi-star-fill' : 'bi-star'
                ]" class="fs-2"></i>
              </button>
            </div>
            <div class="row g-3">

              <div class="col-12 col-sm-6">
                <p>
                  <span class="fw-medium">{{ t.capacity }}:</span>
                  {{ instalacion.aforoMaximo }}
                </p>
              </div>

              <div class="col-12 col-sm-6">
                <p>
                  <span class="fw-medium">{{ t.light }}:</span>
                  {{ instalacion.luz ? t.yes : "No" }}
                </p>
              </div>

              <div class="col-12 col-sm-6">
                <p>
                  <span class="fw-medium">{{ t.tdaPercent }}:</span>
                  {{ instalacion.porcentajeTDA }} %
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p>
                  <span class="fw-medium">{{ t.pavilion }}:</span>
                  {{ instalacion.pabellon.nombre }}
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p>
                  <span class="fw-medium">{{ t.address }}:</span>
                  {{ instalacion.pabellon.direccion }}
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.tipoInstalacion">
                <p>
                  <span class="fw-medium">{{ t.facilityType }}:</span>
                  {{ instalacion.tipoInstalacion }}
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.horaApertura">
                <p>
                  <span class="fw-medium">{{ t.openHour }}:</span>
                  {{ instalacion.horaApertura }}
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.horaCierre">
                <p>
                  <span class="fw-medium">{{ t.closeHour }}:</span>
                  {{ instalacion.horaCierre }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6 d-flex flex-column gap-4">

          <div class="bg-white rounded-3 shadow-sm p-4" v-if="instalacion.imagenURL">
            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <div class="row g-2">
              <div class="col-6" v-for="(img, i) in instalacion.imagenURL" :key="i">

                <img :src="img" class="img-fluid rounded" alt="Instalacion" />
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Reserva y Volver -->
      <div class="d-flex justify-content-center mt-5">
        <button v-if="usuarioFinalStore.isLogged" class="btn btn-success btn-lg px-5 me-4" @click="reservar">
          {{ t.booking }}
        </button>

        <button class="btn btn-secondary btn-lg px-5" @click="volver">
          {{ t.return }}
        </button>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { inject, ref, onMounted, type Ref } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de instalaciones del backend */
import { getInstalacionDetalle } from "../services/detalleService";
import { useUserStore } from '../stores/usuarioFinal';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();

const instalacion = ref({
  id: 0,
  nombre: "",
  imagenURL: [] as string[],
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  horaApertura: "",
  horaCierre: "",
  pabellon: { id: -1, nombre: "", direccion: "" },
  tipoInstalacion: ""
});

const cambiarFavorito = () => {
  usuarioFinalStore.marcarInstalacionFavorita(instalacion.value.id)
}

const reservar = () => {
  router.push({
    name: 'reservar-instalacion',
    params: { id: instalacion.value.id }
  })
}

const volver = () => {
  router.back();
}

onMounted(async () => {
  const id = parseInt(props.id);
  instalacion.value = await getInstalacionDetalle(id);
});
</script>
