<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold m-0">Estadísticas Generales</h2>
      </div>

      <!-- KPIs -->
      <div class="row g-4 mb-4">

        <div class="col-md-4 col-xl-2" v-for="kpi in kpis" :key="kpi.title">
          <div class="card shadow-sm border-0 rounded-4 h-100">
            <div class="card-body text-center">
              <h6 class="text-muted">{{ kpi.title }}</h6>
              <h3 class="fw-bold">{{ kpi.value }}</h3>
            </div>
          </div>
        </div>

      </div>

      <!-- GRÁFICOS -->
      <div class="row g-4 mb-4">

        <!-- Reservas por mes -->
        <div class="col-lg-6">
          <div class="card shadow-sm border-0 rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-3">Reservas últimos 12 meses</h5>
              <div class="chart-placeholder">
                <!-- Aquí irá Chart.js -->
                <p class="text-muted text-center m-0">
                  Gráfico de reservas por mes
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actividades más reservadas -->
        <div class="col-lg-6">
          <div class="card shadow-sm border-0 rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-3">Actividades más reservadas</h5>
              <div class="chart-placeholder">
                <p class="text-muted text-center m-0">
                  Gráfico de actividades
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- USO DE PABELLONES -->
      <div class="card shadow-sm border-0 rounded-4">
        <div class="card-body">
          <h5 class="fw-bold mb-3">Uso de pabellones</h5>

          <div class="table-responsive">
            <table class="table align-middle">
              <thead class="table-light">
                <tr>
                  <th>{{ t.pavilion }}</th>
                  <th>Horas reservadas</th>
                  <th>Ocupación</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="pabellon in usoPabellones" :key="pabellon.nombre">
                  <td>{{ pabellon.nombre }}</td>
                  <td>{{ pabellon.horas }}</td>
                  <td>
                    <div class="progress" style="height: 8px;">
                      <div
                        class="progress-bar"
                        role="progressbar"
                        :style="{ width: pabellon.ocupacion + '%' }"
                      ></div>
                    </div>
                    <small>{{ pabellon.ocupacion }}%</small>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>

      <button class="btn btn-secondary rounded-pill" @click="volver">
        {{ t.return }}
      </button>

    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>('language')!;
const t = useI18n(language);

const router = useRouter()

const volver = () => {
  router.back()
}

const kpis = ref([
  { title: 'Usuarios', value: 0 },
  { title: 'Monitores', value: 0 },
  { title: 'Pabellones', value: 0 },
  { title: 'Sesiones', value: 0 },
  { title: 'Reservas (mes)', value: 0 },
  { title: 'Ingresos (mes)', value: '0 €' }
])

const usoPabellones = ref([
  { nombre: 'Pabellón A', horas: 120, ocupacion: 75 },
  { nombre: 'Pabellón B', horas: 90, ocupacion: 60 }
])

const cargarEstadisticas = async () => {
  try {
    // const response = await api.get('/estadisticas/admin/')
    // const data = response.data

    kpis.value = [
      { title: 'Usuarios', value: 150 },
      { title: 'Monitores', value: 12 },
      { title: 'Pabellones', value: 5 },
      { title: 'Sesiones', value: 34 },
      { title: 'Reservas (mes)', value: 87 },
      { title: 'Ingresos (mes)', value: '2.450 €' }
    ]

  } catch (error) {
    console.error('Error cargando estadísticas', error)
  }
}

onMounted(() => {
  cargarEstadisticas()
})
</script>

<style scoped>
.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 1rem;
}
</style>
