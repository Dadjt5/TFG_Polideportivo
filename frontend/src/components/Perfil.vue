<template>
  <div class="min-vh-100 bg-light">
    <PerfilUsuarioFinal v-if="userStore.role === 'usuario_final'" />
    <PerfilMonitor v-else-if="userStore.role === 'monitor'" />
    <PerfilAdministrador v-else />
  </div>
</template>


<script setup lang="ts">
/* Importamos el usuario final guardado para ver si tiene TDA */
import { useAuthStore } from "@/stores/auth"

import PerfilUsuarioFinal from '@/components/usuarioFinal/PerfilUsuarioFinal.vue';
import PerfilMonitor from '@/components/monitor/PerfilMonitor.vue';
import PerfilAdministrador from "@/components/administrador/PerfilAdministrador.vue";

const userStore = useAuthStore();
</script>