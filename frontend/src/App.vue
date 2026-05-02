<template>
  <Navbar/>
  <router-view />
</template>

<script setup lang="ts">
import { ref, provide, onMounted, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/usuarioFinal";
import { useMonitorStore } from "@/stores/monitor";
import { useAdministradorStore } from "@/stores/administrador";

import Navbar from "./components/Navbar.vue";

const language = ref("es");
provide("language", language);

const INACTIVITY_TIME = 15 * 60 * 1000; // 15 minutos
let inactivityTimer: number;

const router = useRouter();
const userStore = useAuthStore();
const usuarioFinalStore = useUserStore();
const monitorStore = useMonitorStore();
const administradorStore = useAdministradorStore();

const activeStore = computed(() => {
  if (userStore.isUsuarioFinal) {
    return usuarioFinalStore;
  }

  if (userStore.isMonitor) {
    return monitorStore;
  }

  return administradorStore;
});

function logoutUsuario() {
  if (!userStore.isAuthenticated) return;

  activeStore.value.cerrarSesion();
  userStore.logout();

  localStorage.removeItem("access");
  localStorage.removeItem("refresh");

  router.push("/");
}

function resetInactivityTimer() {
  clearTimeout(inactivityTimer);
  inactivityTimer = window.setTimeout(() => {
    logoutUsuario();
  }, INACTIVITY_TIME);
}

onMounted(() => {
  if (userStore.isAuthenticated && !sessionStorage.getItem("tabAlive")) {
    logoutUsuario();
  }

  sessionStorage.setItem("tabAlive", "1");

  window.addEventListener('mousemove', resetInactivityTimer);
  window.addEventListener('keydown', resetInactivityTimer);
  window.addEventListener('click', resetInactivityTimer);
  window.addEventListener('scroll', resetInactivityTimer);
  window.addEventListener('touchstart', resetInactivityTimer);
  resetInactivityTimer();
});

onUnmounted(() => {
  window.removeEventListener('mousemove', resetInactivityTimer);
  window.removeEventListener('keydown', resetInactivityTimer);
  window.removeEventListener('click', resetInactivityTimer);
  window.removeEventListener('scroll', resetInactivityTimer);
  window.removeEventListener('touchstart', resetInactivityTimer);

  clearTimeout(inactivityTimer);
});
</script>