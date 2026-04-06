<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- Cabecera -->
      <div class="d-flex justify-content-center align-items-center mt-4 mb-5 gap-2">
        <h1 class="fw-semibold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-calendar2-event me-2"></i>{{ instalacion.nombre }}
        </h1>

        <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning" @click.stop="cambiarFavorito"
          :title="usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'">
          <i :class="['bi', usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'bi-star-fill' : 'bi-star']"
            class="fs-2"></i>
        </button>
      </div>

      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <!-- NAV TABS -->
        <ul class="nav nav-pills nav-fill mb-4">
          <li class="nav-item">
            <button class="nav-link active fw-bold" data-bs-toggle="pill" data-bs-target="#info">
              {{ t.facilityDetails }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#horario">
              {{ t.timetable }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#imagenes">
              {{ t.images }}
            </button>
          </li>
        </ul>

        <!-- CONTENIDO -->
        <div class="tab-content">

          <!-- TAB INFO -->
          <div class="tab-pane fade show active" id="info">
            <div class="row g-3">

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-people-fill text-success me-1"></i>
                  <span class="fw-medium">{{ t.capacity }}:</span> {{ instalacion.aforoMaximo }}
                </p>
              </div>

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-lightbulb-fill text-warning me-1"></i>
                  <span class="fw-medium">{{ t.light }}:</span> {{ instalacion.luz ? t.yes : "No" }}
                </p>
              </div>

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-percent text-info me-1"></i>
                  <span class="fw-medium">{{ t.tdaPercent }}:</span> {{ instalacion.porcentajeTDA }} %
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p>
                  <i class="bi bi-building text-primary me-1"></i>
                  <span class="fw-medium">{{ t.pavilion }}:</span>
                  <span class="text-primary fw-medium" style="cursor: pointer;"
                    @click="pavilionDetail(instalacion.pabellon.id)">
                    {{ instalacion.pabellon.nombre }}
                  </span>
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p><i class="bi bi-geo-alt-fill text-danger me-1"></i>
                  <span class="fw-medium">{{ t.address }}:</span>
                  {{ instalacion.pabellon.direccion }}
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.tipoInstalacion">
                <p><i class="bi bi-door-open-fill text-primary me-1"></i>
                  <span class="fw-medium">{{ t.facilityType }}:</span>
                  {{ instalacion.tipoInstalacion }}
                </p>
              </div>

            </div>
          </div>

          <!-- TAB HORARIO -->
          <div class="tab-pane fade" id="horario">
            <div class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="dia in agenda" :key="dia.dia">
                <div class="card border-1 border-light shadow-sm rounded-4 h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <strong class="fs-5">{{ dia.dia }}</strong>
                      <span class="badge" :class="dia.abierto ? 'bg-success' : 'bg-danger'">
                        {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                      </span>
                    </div>

                    <div v-if="dia.abierto">
                      <div
                        class="d-flex align-items-center justify-content-center gap-2 py-2 bg-white rounded border">
                        <span class="fw-semibold text-primary">{{ dia.horaApertura?.slice(0, 5) }}</span>
                        <span class="text-muted">-</span>
                        <span class="fw-semibold text-primary">{{ dia.horaCierre?.slice(0, 5) }}</span>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>

            <button class="btn btn-outline-primary mt-4" @click="descargarPDF">
              <i class="bi bi-file-earmark-pdf"></i> {{ t.downloadTimetable }}
            </button>
          </div>

          <!-- TAB IMÁGENES -->
          <div class="tab-pane fade" id="imagenes">
            <div class="d-flex justify-content-center">
              <img :src="instalacion.imagen" class="img-fluid rounded shadow"
                style="max-height: 400px; object-fit: cover;" />
            </div>
          </div>

        </div>
      </div>

      <!-- Reserva y Volver -->
      <div class="d-flex justify-content-center align-items-center mt-5 gap-3 flex-wrap">

        <!-- RESERVAR -->
        <button v-if="usuarioFinalStore.isLogged" class="btn btn-success btn-lg px-5 shadow-sm" @click="reservar">
          {{ t.booking }}
        </button>

        <!-- VOLVER -->
        <button class="btn btn-outline-secondary btn-lg px-5" @click="volver">
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
import { descargarHorario } from '@/services/crearRecursosService';

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();
const agenda = ref<any[]>([])
const fechasEspeciales = ref<any[]>([])

const instalacion = ref({
  id: 0,
  nombre: "",
  imagen: "",
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  horaApertura: "",
  horaCierre: "",
  pabellon: { id: -1, nombre: "", direccion: "" },
  tipoInstalacion: "",
  agenda: [] as any[],
});

const cambiarFavorito = () => {
  usuarioFinalStore.marcarInstalacionFavorita(instalacion.value.id)
}

async function descargarPDF() {
  try {
    const data = await descargarHorario(instalacion.value.id)

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
    const data = await getInstalacionDetalle(id)

    agenda.value = data.agenda.filter((a: any) => a.dia && !a.fecha)
    fechasEspeciales.value = data.agenda.filter((a: any) => a.fecha)

    instalacion.value = {
      ...data,
      agenda: agenda.value
    }
  } catch (e) {
    console.log("Error al obtener la informacion de instalaciones", e);
  }
});
</script>
