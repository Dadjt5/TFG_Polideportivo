<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- Cabecera -->
      <div class="text-center mt-4 mb-5">
        <h1 class="fw-semibold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-building me-2"></i>{{ instalacion.nombre }}
        </h1>
      </div>

      <div class="row g-4">

        <!-- DETALLES -->
        <div class="col-lg-6">
          <div class="rounded-3 shadow-sm p-4 h-100 card-hover"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h4 class="mb-3 d-flex align-items-center">
                <i class="bi bi-info-circle-fill text-primary me-2"></i>
                {{ t.facilityDetails }}
              </h4>

              <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning"
                      @click.stop="cambiarFavorito" :title="usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'">
                <i :class="[ 'bi', usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'bi-star-fill' : 'bi-star']" class="fs-2"></i>
              </button>
            </div>

            <div class="row g-3">
              <div class="col-12 col-sm-6">
                <p><i class="bi bi-people-fill text-success me-1"></i><span class="fw-medium">{{ t.capacity }}:</span> {{ instalacion.aforoMaximo }}</p>
              </div>

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-lightbulb-fill text-warning me-1"></i><span class="fw-medium">{{ t.light }}:</span> {{ instalacion.luz ? t.yes : "No" }}</p>
              </div>

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-percent text-info me-1"></i><span class="fw-medium">{{ t.tdaPercent }}:</span> {{ instalacion.porcentajeTDA }} %</p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p>
                  <i class="bi bi-building text-primary me-1"></i>
                  <span class="fw-medium">{{ t.pavilion }}: </span>
                  <span class="text-primary fw-medium" style="cursor: pointer;" @click="pavilionDetail(instalacion.pabellon.id)">
                    {{ instalacion.pabellon.nombre }}
                  </span>
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p><i class="bi bi-geo-alt-fill text-danger me-1"></i><span class="fw-medium">{{ t.address }}:</span> {{ instalacion.pabellon.direccion }}</p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.tipoInstalacion">
                <p><i class="bi bi-door-open-fill text-primary me-1"></i><span class="fw-medium">{{ t.facilityType }}:</span> {{ instalacion.tipoInstalacion }}</p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.horaApertura">
                <p><i class="bi bi-clock-fill text-success me-1"></i><span class="fw-medium">{{ t.openHour }}:</span> {{ instalacion.horaApertura }}</p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.horaCierre">
                <p><i class="bi bi-clock text-danger me-1"></i><span class="fw-medium">{{ t.closeHour }}:</span> {{ instalacion.horaCierre }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- IMÁGENES -->
        <div class="col-lg-6 d-flex flex-column gap-4">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <img :src="instalacion.imagenURL" class="img-fluid rounded mb-3 img-hover" />
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
import { getInstalacionDetalle } from "@/services/detalleService";
import { useUserStore } from '@/stores/usuarioFinal';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();

const instalacion = ref({
  id: 0,
  nombre: "",
  imagenURL: "",
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

const pavilionDetail = (id: number) => {
  router.push({
    name: 'detalle-pabellon',
    params: { id }
  });
}


const reservar = () => {
  router.push({
    name: 'reservar-instalacion',
    params: { id: instalacion.value.id }
  })
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);

  try {
    instalacion.value = await getInstalacionDetalle(id);
  } catch(e) {
    console.log("Error al obtener la informacion de instalaciones", e);
  }
});
</script>
