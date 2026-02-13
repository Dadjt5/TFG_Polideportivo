<template>
  <div class="min-vh-100 bg-light">
    <TDAActiva v-if="usuarioFinalStore.hasTda" />
    <TDAVacia v-else />
  </div>
</template>


<script setup lang="ts">
import { onMounted } from 'vue';

/* Importamos el usuario final guardado para ver si tiene TDA */
import { useUserStore } from '@/stores/usuarioFinal';

import TDAVacia from '@/components/usuarioFinal/perfil/tarjeta/TDAVacia.vue';
import TDAActiva from '@/components/usuarioFinal/perfil/tarjeta/TDAActiva.vue';

const usuarioFinalStore = useUserStore();

onMounted(async () => {
  if (!usuarioFinalStore.hasTda) {
    await usuarioFinalStore.fetchTDA();
  }
});
</script>