<template>
  <div class="container py-5">
    <h1 class="text-center mb-4">{{ t.TDATitle }}</h1>

    <div class="text-center card shadow-lg rounded-4 p-4 mx-auto" style="max-width: 900px;">

      <h5 class="fs-2 mb-5">{{ t.qrTitle }}</h5>
      <QRCodeVue3 :key="qrKey" :value="qrValue" :size="220" level="H" />

      <div class="text-center bg-light rounded-3 p-4 h-100">
        <h5 class="fs-2 mt-4 mb-3">{{ t.cardInfo }}</h5>

        <div class="row g-4 align-items-center justify-content-center">
          <div class="col-12 col-md-6 fs-5 d-flex justify-content-center">
            <p><strong>ID:</strong> {{ usuarioFinalStore.tda?.id }}</p>
          </div>

          <div class="col-12 col-md-6 fs-5 d-flex justify-content-center">
            <p>
              <strong>{{ t.status }}: </strong>
              <span
                :class="usuarioFinalStore.hasTda ? 'text-success fw-semibold' : 'text-danger fw-semibold'"
              >
                {{ usuarioFinalStore.hasTda ? t.active : t.inactive }}
              </span>
            </p>
          </div>

          <div class="col-12 col-md-6 fs-5 d-flex justify-content-center">
            <p><strong>{{ t.issued }}:</strong> {{ usuarioFinalStore.tda?.fechaInicio }}</p>
          </div>

          <div class="col-12 col-md-6 fs-5 d-flex justify-content-center">
            <p><strong>{{ t.expires }}:</strong> {{ usuarioFinalStore.tda?.fechaExpiracion }}</p>
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-primary fs-5" @click="regenerarQR()">
          🔄 {{ t.regenerateQR }}
        </button>
        <button class="btn btn-secondary fs-5" @click="descargarQR()">
          ⬇️ {{ t.downloadQR }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, inject, computed, ref } from "vue";
import QRCodeVue3 from 'qrcode-vue3';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

import { useUserStore } from "@/stores/usuarioFinal";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore();

const qrKey = computed(() => token.value);
let token = ref("1234")

const qrValue = computed(() =>
  JSON.stringify({
    id: usuarioFinalStore.tda?.id,
    usuario: usuarioFinalStore.usuarioFinal.nombre,
    token: token.value,
  })
);

const regenerarQR = () => {
  if(token.value == "1234") {
    token.value = "4321"
  } else {
    token.value = "1234"
  }
};

const descargarQR = () => {
};

</script>
