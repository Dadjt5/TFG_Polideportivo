<script setup lang="ts">
import { type Ref, inject } from 'vue';
import type { Language } from "../../useI18N";
import { useI18n } from "../../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

defineProps<{
  instalacion: {
    id: number
    nombre: string
    horaApertura: string
    horaCierre: string
    pabellon?: {
      nombre: string
      direccion: string
    }
  }
  icon: any
}>()
</script>

<template>
    <div class="card shadow-sm h-100 installation-card">
      <div class="card-body">

        <div class="d-flex justify-content-between align-items-start mb-3">
          <div class="d-flex align-items-start gap-3">
            <div class="icon-wrapper bg-success-subtle">
              <component :is="icon" class="icon text-success" />
            </div>

            <div>
              <h5 class="mb-1">{{ instalacion.nombre }}</h5>
              <span class="badge rounded-pill text-bg-success">
                {{ t.facility }}
              </span>
            </div>
          </div>
        </div>

        <div class="text-muted small">
          <div class="d-flex justify-content-between mb-1">
            <span>{{ t.schedule }}</span>
            <strong>
              {{ instalacion.horaApertura }} - {{ instalacion.horaCierre }}
            </strong>
          </div>

          <div
            v-if="instalacion.pabellon"
            class="d-flex justify-content-between"
          >
            <span>{{ t.pavilions }}</span>
            <strong>{{ instalacion.pabellon.nombre }}</strong>
          </div>
        </div>

      </div>
    </div>
</template>


<style scoped>
.installation-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.installation-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.15);
}

.icon-wrapper {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  width: 20px;
  height: 20px;
}
</style>
