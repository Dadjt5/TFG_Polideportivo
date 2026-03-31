<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- Cabecera -->
      <div class="text-center mt-4 mb-5">
        <h1 class="fw-semibold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-calendar2-event me-2"></i>{{ actividad.nombre }}
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
                {{ t.activityDetails }}
              </h4>

              <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning"
                      @click.stop="cambiarFavorito"
                      :title="usuarioFinalStore.activityIsFavorite(actividad.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'">
                <i :class="[ 'bi', usuarioFinalStore.activityIsFavorite(actividad.id) ? 'bi-star-fill' : 'bi-star']" class="fs-2"></i>
              </button>
            </div>

            <div class="row g-3">
              <div class="col-12 col-sm-4" v-if="actividad.periodo">
                <p><i class="bi bi-clock-fill text-success me-1"></i><span class="fw-medium">{{ t.period }}:</span> {{ actividad.periodo }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.estado">
                <p><i class="bi bi-info-circle text-info me-1"></i><span class="fw-medium">{{ t.status }}:</span> {{ actividad.estado }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.edadMinima">
                <p><i class="bi bi-person-fill text-warning me-1"></i><span class="fw-medium">{{ t.minimumAge }}:</span> {{ actividad.edadMinima }}</p>
              </div>

              <div class="col-12 col-sm-4">
                <p><i class="bi bi-people-fill text-success me-1"></i><span class="fw-medium">{{ t.availablePlaces }}:</span> {{ actividad.plazasMaximas }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.nivel">
                <p><i class="bi bi-bar-chart-fill text-primary me-1"></i><span class="fw-medium">{{ t.level }}:</span> {{ actividad.nivel }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.tipoReserva">
                <p><i class="bi bi-journal-check text-info me-1"></i><span class="fw-medium">{{ t.reserveType }}:</span> {{ actividad.tipoReserva }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.tipoActividad">
                <p><i class="bi bi-activity text-warning me-1"></i><span class="fw-medium">{{ t.activityType }}:</span> {{ actividad.tipoActividad }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.terreno">
                <p><i class="bi bi-signpost-split-fill text-secondary me-1"></i><span class="fw-medium">{{ t.terrainType }}:</span> {{ actividad.terreno }}</p>
              </div>

              <div class="col-12 col-sm-4">
                <p><i class="bi bi-credit-card-2-front-fill text-success me-1"></i><span class="fw-medium">{{ t.credits }}:</span> {{ actividad.numeroCreditos }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.año">
                <p><i class="bi bi-calendar-year text-info me-1"></i><span class="fw-medium">{{ t.academicYear }}:</span> {{ actividad.año }}</p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.instalacion">
                <p>
                  <i class="bi bi-building text-primary me-1"></i>
                  <span class="fw-medium">{{ t.facility }}: </span>
                  <span class="text-primary fw-medium" style="cursor: pointer;" @click="facilityDetail(actividad.instalacion)">
                    {{ actividad.nombreInstalacion }}
                  </span>
                </p>
              </div>

              <div class="col-12 col-sm-4" v-if="actividad.material">
                <p><i class="bi bi-tools text-warning me-1"></i><span class="fw-medium">{{ t.material }}:</span> {{ actividad.material }}</p>
              </div>

              <div class="col-12 col-sm-4">
                <p><i class="bi bi-person-badge text-info me-1"></i><span class="fw-medium">{{ t.monitorName }}:</span> {{ actividad.nombreMonitor || "-" }}</p>
              </div>

              <div class="col-12 col-sm-4">
                <p><i class="bi bi-activity text-info me-1"></i><span class="fw-medium">{{ t.sport }}:</span> {{ actividad.nombreDeporte || "-" }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- DERECHA -->
        <div class="col-lg-6 d-flex flex-column gap-4">

          <!-- IMÁGENES -->
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <img :src="actividad.imagenURL" class="img-fluid rounded mb-3 img-hover" />
          </div>

          <!-- SESIONES -->
          <div class="rounded-3 shadow-sm p-4 card-hover"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-calendar-event text-primary"></i>
              {{ t.sessions }}
            </h4>

            <div v-for="s in actividad.sesiones" :key="s.id"
                 class="d-flex justify-content-between align-items-center p-3 mb-2 border rounded-3 bg-light session-hover">
              <div>
                <div class="fw-semibold">{{ s.dia }}</div>
                <div class="text-muted">{{ s.horaInicio }} - {{ s.horaFin }}</div>
              </div>
            </div>

            <button class="btn btn-outline-primary mt-4" @click="descargarPDF">
              <i class="bi bi-file-earmark-pdf"></i> {{ t.downloadTimetable }}
            </button>
          </div>
        </div>
      </div>

      <!-- Reserva y Volver -->
      <div class="d-flex justify-content-center mt-5">
        <button v-if="puedeReservar" class="btn btn-success btn-lg px-5 me-4" @click="reservar">
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
import { inject, type Ref, ref, onMounted, computed } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de actividades del backend y el usuario*/
import { getActividadDetalle } from "@/services/detalleService";
import { useUserStore } from '@/stores/usuarioFinal';
import { descargarHorarioSesiones } from '@/services/crearRecursosService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

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
  imagenURL: "",
  plazasMaximas: 0,
  plazasReservadas: 0,
  edadMinima: 0,
  año: 0,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  inscripcion: false,
  tipoReserva: "",
  terreno: "",
  periodo: "",
  estado: "",
  dias: "",
  nombreMonitor: "",
  nombreDeporte: "",
  nombreInstalacion: "",
  horasSemanales: "",
  instalacion: 0,
  sesiones: [] as any[]
});

const puedeReservar = computed(() => {
  if (!usuarioFinalStore.isLogged) {
    return false
  }
  
  if (actividad.value.tipoReserva !== 'Permite la reserva solo online' && actividad.value.tipoReserva !== 'Permite ambos tipos de reserva') {
    return false
  }

  if (!actividad.value.inscripcion) {
    return false
  }

  return true
})

const cambiarFavorito = () => {
  usuarioFinalStore.marcarActividadFavorita(actividad.value.id)
}

async function descargarPDF() {
  try {
    const data = await descargarHorarioSesiones(actividad.value.id)

    const blob = new Blob([data], { type: 'application/pdf' })

    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "horarios.pdf"
    a.click()
    window.URL.revokeObjectURL(url)

  } catch (error) {
    console.error("Error descargando PDF:", error)
  }
}

const facilityDetail = (id: number) => {
  router.push({
    name: 'detalle-instalacion',
    params: { id }
  });
}

const reservar = () => {
  router.push({
    name: 'reservar-actividad',
    params: { id: actividad.value.id }
  })
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);
  actividad.value = await getActividadDetalle(id);
});
</script>
