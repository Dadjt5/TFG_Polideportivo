<template>
  <div class="min-vh-100 bg-light">
    <ForoUsuarioFinal v-if="userStore.isUsuarioFinal" />
    <ForoAdministrador v-else-if="userStore.isAdminUsuarios || userStore.isAdminRaiz" />
  </div>
</template>


<script setup lang="ts">
import { useAuthStore } from "@/stores/auth"

import ForoUsuarioFinal from '@/components/usuarioFinal/ForoUsuarioFinal.vue';
import ForoAdministrador from '@/components/administrador/ForoAdministrador.vue';

const userStore = useAuthStore();
</script>