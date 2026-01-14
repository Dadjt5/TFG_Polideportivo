<template>
  <div class="container py-5">
    <h1 class="text-center mb-5">{{ t.pageTitle }}</h1>

    <div class="card shadow-lg rounded-4 p-4 mx-auto" style="max-width: 900px;">
      <div class="row g-4 align-items-center justify-content-center">

        <!-- QR -->
        <div class="col-md-5 text-center">
          <h5 class="mb-3">{{ t.qrTitle }}</h5>
          <QRCodeVue3
            :value="qrValue"
            :size="220"
            level="H"
          />
        </div>

        <div class="col-md-5">
          <div class="bg-light rounded-3 p-4 h-100">
            <h5 class="mb-3">{{ t.cardInfo }}</h5>

            <p><strong>ID:</strong> {{ usuarioFinalStore.tda?.id }}</p>
            <p><strong>{{ t.status }}:</strong> {{ usuarioFinalStore.hasTda }}</p>
            <p><strong>{{ t.issued }}:</strong> {{ usuarioFinalStore.tda?.fechaInicio }}</p>
            <p><strong>{{ t.expires }}:</strong> {{ usuarioFinalStore.tda?.fechaExpiracion }}</p>
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-primary">
          🔄 {{ t.regenerateQR }}
        </button>
        <button class="btn btn-secondary">
          ⬇️ {{ t.downloadQR }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import QRCodeVue3 from 'qrcode-vue3';

import { useUserStore } from '../../stores/usuarioFinal';

const usuarioFinalStore = useUserStore();

const language = ref<'es' | 'en'>('es');

const tda = computed(() => usuarioFinalStore.tda);

const qrValue = computed(() =>
  JSON.stringify({
    id: usuarioFinalStore.tda?.id,
    usuario: usuarioFinalStore.usuarioFinal.nombre,
    token: "1234",
  })
);

const translations = {
  es: {
    pageTitle: 'Tarjeta Deportiva Anual',
    cardInfo: 'Información de tu tarjeta',
    status: 'Estado',
    issued: 'Emitida',
    expires: 'Caduca',
    qrTitle: 'Código QR de acceso',
    regenerateQR: 'Regenerar QR',
    downloadQR: 'Descargar QR',
  },
  en: {
    pageTitle: 'Annual Sports Card',
    cardInfo: 'Your card information',
    status: 'Status',
    issued: 'Issued',
    expires: 'Expires',
    qrTitle: 'Access QR Code',
    regenerateQR: 'Regenerate QR',
    downloadQR: 'Download QR',
  }
};

const t = computed(() => translations[language.value]);
</script>
