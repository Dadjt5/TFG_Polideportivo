<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <div class="text-center mt-4 mb-5">
        <h1 class="fw-semibold">{{ actividad.nombre }}</h1>
      </div>

      <div class="row g-4">
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">

            <div class="d-flex justify-content-between align-items-start mb-3">
              <h4 class="mb-3 d-flex align-items-center">
                <i class="bi bi-info-circle-fill text-primary me-2"></i>
                {{ t.activityDetails }}
              </h4>

              <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning"
                @click.stop="cambiarFavorito">
                <i :class="[
                  'bi',
                  usuarioFinalStore.activityIsFavorite(actividad.id) ? 'bi-star-fill' : 'bi-star'
                ]" class="fs-2"></i>
              </button>
            </div>

            <div class="row g-3">
              <div class="col-12 col-sm-4" v-if="actividad.periodo">
                <p>
                  <span class="fw-medium">{{ t.period }}:</span>
                  {{ actividad.periodo }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.estado">
                <p>
                  <span class="fw-medium">{{ t.status }}:</span>
                  {{ actividad.estado }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.edadMinima">
                <p>
                  <span class="fw-medium">{{ t.minimumAge }}:</span>
                  {{ actividad.edadMinima }}
                </p>
              </div>

              <div class="col-12 col-sm-4">
                <p>
                  <span class="fw-medium">{{ t.availablePlaces }}:</span>
                  {{ actividad.plazasMaximas }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.nivel">
                <p>
                  <span class="fw-medium">{{ t.level }}:</span>
                  {{ actividad.nivel }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.tipoReserva">
                <p>
                  <span class="fw-medium">{{ t.reserveType }}:</span>
                  {{ actividad.tipoReserva }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.tipoActividad">
                <p>
                  <span class="fw-medium">{{ t.activityType }}:</span>
                  {{ actividad.tipoActividad }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.terreno">
                <p>
                  <span class="fw-medium">{{ t.terrainType }}:</span>
                  {{ actividad.terreno }}
                </p>
              </div>

              <div class="col-12 col-sm-4">
                <p>
                  <span class="fw-medium">{{ t.credits }}:</span>
                  {{ actividad.numeroCreditos }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.año">
                <p>
                  <span class="fw-medium">{{ t.academicYear }}:</span>
                  {{ actividad.año }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.instalacion">
                <p>
                  <span class="fw-medium">{{ t.facility }}: </span>
                  <span class="text-primary fw-medium" style="cursor: pointer;"
                    @click="facilityDetail(actividad.instalacion.id)">
                    {{ actividad.instalacion.nombre }}
                  </span>
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.material">
                <p>
                  <span class="fw-medium">{{ t.material }}:</span>
                  {{ actividad.material }}
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.monitor">
                <p>
                  <span class="fw-medium">{{ t.monitorName }}:</span>
                  {{ actividad.monitor.nombre || "-" }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- DERECHA -->
        <div class="col-lg-6 d-flex flex-column gap-4">

          <!-- IMÁGENES -->
          <div class="bg-white rounded-3 shadow-sm p-4">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <div class="row g-2">
              <div class="col-6" v-for="(img, i) in actividad.imagenURL" :key="i">

                <img :src="img" class="img-fluid rounded" alt="Actividad" />
              </div>
            </div>

          </div>

          <!-- SESIONES -->
          <div class="bg-white rounded-3 shadow-sm p-4">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-calendar-event text-primary"></i>
              {{ t.sessions }}
            </h4>

            <div v-for="s in actividad.sesiones" :key="s.id"
              class="d-flex justify-content-between align-items-center p-3 mb-2 border rounded-3 bg-light">
              <div>
                <div class="fw-semibold">{{ s.dia }}</div>
                <div class="text-muted">
                  {{ s.horario.horaInicio }} - {{ s.horario.horaFin }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Reserva y Volver -->
      <div class="d-flex justify-content-center mt-5">
        <button v-if="usuarioFinalStore.isLogged" class="btn btn-success btn-lg px-5 me-4">
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
import { inject, type Ref, ref, onMounted } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de actividades del backend y el usuario*/
import { getActividadDetalle } from "../services/detalleService";
import { useUserStore } from '../stores/usuarioFinal';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();

type Generic = {
  id: number
  nombre: string
}

const actividad = ref({
  id: 0,
  nombre: "",
  tipoActividad: "",
  imagenURL: [] as string[],
  plazasMaximas: 0,
  plazasReservadas: 0,
  edadMinima: 0,
  año: 0,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  tipoReserva: "",
  terreno: "",
  periodo: "",
  estado: "",
  dias: "",
  instalacion: {
    id: -1,
    nombre: ""
  } as Generic,

  monitor: {
    id: -1,
    nombre: ""
  } as Generic,

  sesiones: [] as any[]
});

const facilityDetail = (id: number) => {
  router.push({
    name: 'detalle-instalacion',
    params: { id }
  });
}

const volver = () => {
  router.back();
};

const cambiarFavorito = () => {
  usuarioFinalStore.marcarActividadFavorita(actividad.value.id)
}

onMounted(async () => {
  const id = parseInt(props.id);
  actividad.value = await getActividadDetalle(id);
});

</script>
