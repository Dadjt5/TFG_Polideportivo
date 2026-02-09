<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 1000px">
      <h1 class="text-center mb-5 fw-semibold">
        {{ t.manageActivities }}
      </h1>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4">

          <!-- ACTIVIDADES -->
          <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-dumbbell me-2"></i>{{ t.activities }}
              </h5>
              <button class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newActivity }}
              </button>
            </div>

            <!-- BUSCADOR -->
            <div class="mb-4">
              <div class="input-group">
                <span class="input-group-text bg-white">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  :placeholder="t.searchActivities"
                  v-model="search"
                />
              </div>
            </div>

            <!-- LISTADO -->
            <div class="list-group list-group-flush">
              <div
                v-for="a in actividadesFiltradas"
                :key="a.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm"
                @click="actividadDetail(a.id)">
                <span class="fw-medium text-primary">
                  {{ a.nombre }}
                </span>
              </div>
            </div>

          </div>

        </div>
      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { onMounted, type Ref, ref, computed, inject } from "vue"
import { useRouter } from "vue-router"

import { getActividadesSimples } from "../services/listadoService"

import type { Language } from "../useI18N"
import { useI18n } from "../useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const search = ref("")

const actividades = ref<any[]>([])

const actividadesFiltradas = computed(() =>
  actividades.value.filter(a =>
    a.nombre.toLowerCase().includes(search.value.toLowerCase())
  )
)

const actividadDetail = (id: number) => {
  router.push({
    name: "editar-actividad",
    params: { id }
  })
}

onMounted(async () => {
  try {
    actividades.value = await getActividadesSimples()
  } catch (e) {
    console.log("Error al obtener las actividades", e)
  }
});
</script>
