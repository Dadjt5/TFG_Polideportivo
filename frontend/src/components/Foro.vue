<template>
  <div class="min-vh-100 bg-light">
    <ForoUsuarioFinal v-if="userStore.role === 'usuario_final'" />
    <ForoAdministrador v-else-if="userStore.role === 'administrador'" />
  </div>
</template>


<script setup lang="ts">
import { useAuthStore } from "@/stores/auth"

import ForoUsuarioFinal from '@/components/usuarioFinal/ForoUsuarioFinal.vue';
import ForoAdministrador from '@/components/administrador/ForoAdministrador.vue';

const userStore = useAuthStore();
</script>