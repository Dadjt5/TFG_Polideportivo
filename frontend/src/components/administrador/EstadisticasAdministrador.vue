<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold m-0 text-primary">
          <i class="bi bi-bar-chart-line-fill me-2"></i>
          Estadísticas Generales
        </h2>
      </div>

      <!-- KPIs -->
      <div class="row g-4 mb-4">

        <div class="col-md-4 col-xl-2" v-for="kpi in kpis" :key="kpi.title">
          <div class="card shadow-lg border-0 rounded-4 h-100 text-center"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
            <div class="card-body d-flex flex-column justify-content-center">
              <h6 class="text-muted mb-2">{{ kpi.title }}</h6>
              <h3 class="fw-bold text-dark">{{ kpi.value }}</h3>
            </div>
          </div>
        </div>

      </div>

      <!-- GRÁFICOS -->
      <div class="row g-4 mb-4">

        <!-- Reservas por mes -->
        <div class="col-lg-6">
          <div class="card shadow-lg border-0 rounded-4"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
            <div class="card-body">
              <h5 class="fw-bold mb-3 text-primary">
                <i class="bi bi-graph-up-arrow me-2"></i>
                Reservas últimos 12 meses
              </h5>
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
          <div class="card shadow-lg border-0 rounded-4"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
            <div class="card-body">
              <h5 class="fw-bold mb-3 text-primary">
                <i class="bi bi-trophy-fill me-2"></i>
                Actividades más reservadas
              </h5>
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
      <div class="card shadow-lg border-0 rounded-4"
           style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body">
          <h5 class="fw-bold mb-3 text-primary">
            <i class="bi bi-building me-2"></i>
            Uso de pabellones
          </h5>

          <div class="table-responsive">
            <table class="table align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>{{ t.pavilion }}</th>
                  <th>Horas reservadas</th>
                  <th>Ocupación</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="pabellon in usoPabellones" :key="pabellon.id">
                  <td class="fw-medium">{{ pabellon.nombre }}</td>
                  <td>{{ pabellon.horas }}</td>
                  <td style="min-width: 150px;">
                    <div class="progress" style="height: 8px;">
                      <div class="progress-bar" role="progressbar" :class="{
                        'bg-success': pabellon.ocupacion < 50,
                        'bg-warning': pabellon.ocupacion >= 50 && pabellon.ocupacion < 80,
                        'bg-danger': pabellon.ocupacion >= 80
                      }" :style="{ width: pabellon.ocupacion + '%' }"></div>
                    </div>
                    <small class="text-muted">{{ pabellon.ocupacion }}%</small>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>

      <div class="text-center">
        <button class="btn btn-primary fs-5 mt-4 rounded-pill px-4 shadow-sm" @click="volver">
          <i class="bi bi-arrow-left me-2"></i>
          {{ t.return }}
        </button>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { inject, type Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { getEstadisticasAdministrador } from "@/services/administradorService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>('language')!;
const t = useI18n(language);

const router = useRouter();

const volver = () => {
  router.back()
};

const kpis = ref([
  { title: 'Usuarios', value: 0 },
  { title: 'Monitores', value: 0 },
  { title: 'Pabellones', value: 0 },
  { title: 'Sesiones', value: 0 },
  { title: 'Reservas (mes)', value: 0 },
  { title: 'Ingresos (mes)', value: '0 €' }
])

const usoPabellones = ref([])


onMounted(async () => {
  try {
    const data = await getEstadisticasAdministrador()

    console.log(data)

    kpis.value = [
      { title: 'Usuarios', value: data.usuarios },
      { title: 'Monitores', value: data.monitores },
      { title: 'Pabellones', value: data.pabellones },
      { title: 'Sesiones', value: data.sesiones },
      { title: 'Reservas (mes)', value: data.reservas_mes },
      { title: 'Ingresos (mes)', value: data.ingresos_mes + " €" }
    ]

    usoPabellones.value = data.uso_pabellones || []

  } catch (e) {
    console.error('Error cargando estadísticas', e)
  }
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
