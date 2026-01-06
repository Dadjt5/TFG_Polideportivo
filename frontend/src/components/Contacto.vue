<template>
  <div class="min-vh-100 bg-light">

    <div class="container py-5">
      <div class="text-center mb-5">
        <h1 class="fw-semibold text-dark">
          {{ t.contactTitle }}
        </h1>
        <p class="fs-5 text-secondary">
          {{ t.contactSubtitle }}
        </p>
      </div>

      <div class="card shadow-lg border-0 rounded-4 mx-auto" style="max-width:800px">
        <div class="card-body p-4 d-flex flex-column gap-4">

          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-telephone-fill text-primary fs-4"></i>
            <span class="fw-medium">{{ t.phoneNumber }}:</span>
            <span class="text-muted">{{ contactInfo.phone }}</span>
          </div>

          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-envelope-fill text-primary fs-4"></i>
            <span class="fw-medium">{{ t.email }}:</span>
            <span class="text-muted">{{ contactInfo.email }}</span>
          </div>

          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-geo-alt-fill text-primary fs-4"></i>
            <span class="fw-medium">{{ t.address }}:</span>
            <span class="text-muted">{{ contactInfo.address }}</span>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { type Ref, inject } from "vue";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);


const contactInfo = {
  phone: "91 497 85 56",
  email: "instalacionesdeportivas@informacion.es",
  address:
    "C. de Erasmo de Rotterdam, 1, Fuencarral-El Pardo, 28049 Madrid, España",
};
</script>
