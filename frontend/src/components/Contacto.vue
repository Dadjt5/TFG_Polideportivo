<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <div class="container py-5">
      <div class="text-center mt-3 mb-5">
        <h1 class="fw-bold text-primary">
          {{ t.contactTitle }}
        </h1>
        <p class="fs-5 text-dark">
          {{ t.contactSubtitle }}
        </p>
      </div>

      <div class="card shadow-lg border-0 rounded-4 mx-auto"
           style="max-width:800px; background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4 d-flex flex-column gap-4">

          <!-- Teléfono -->
          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-telephone-fill text-success fs-4"></i>
            <span class="fw-medium text-dark">{{ t.phoneNumber }}:</span>
            <span class="text-secondary">{{ contactInfo.phone }}</span>
          </div>

          <!-- Email con botón copiar -->
          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-envelope-fill text-danger fs-4"></i>
            <span class="fw-medium text-dark">{{ t.email }}:</span>
            <span class="text-secondary">{{ contactInfo.email }}</span>
            <button class="btn btn-outline-secondary btn-sm ms-2"
                    @click="copyEmail"
                    @mouseenter="tooltip = 'Copiar email'"
                    @mouseleave="tooltip = ''"
            >
              <i class="bi bi-clipboard"></i>
            </button>
            <small class="text-success ms-2" v-if="copied">{{ tooltip }}</small>
          </div>

          <!-- Dirección -->
          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-geo-alt-fill text-warning fs-4"></i>
            <span class="fw-medium text-dark">{{ t.address }}:</span>
            <span class="text-secondary">{{ contactInfo.address }}</span>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, inject } from "vue";
import { useI18n } from "@/useI18N";
import type { Language } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const contactInfo = {
  phone: "91 497 85 56",
  email: "instalacionesdeportivas@informacion.es",
  address: "C. de Erasmo de Rotterdam, 1, Fuencarral-El Pardo, 28049 Madrid, España",
};

const copied = ref(false);
const tooltip = ref('');

// Función para copiar al portapapeles
const copyEmail = () => {
  navigator.clipboard.writeText(contactInfo.email).then(() => {
    copied.value = true;
    tooltip.value = 'Copiado!';
    setTimeout(() => copied.value = false, 2000);
  });
};
</script>