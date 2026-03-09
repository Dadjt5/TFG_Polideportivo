<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow py-3">
    <div class="container-fluid px-4">

      <!-- Logo -->
      <router-link to="/" class="navbar-brand fw-bold fs-4" @click="menuOpen = false">
        Polideportivo XX
      </router-link>

      <!-- Botón desplegable -->
      <button class="navbar-toggler" type="button" @click="menuOpen = !menuOpen">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Contenido -->
      <div :class="['navbar-collapse collapse', { show: menuOpen }]">

        <ul class="navbar-nav ms-auto align-items-lg-center">

          <li class="nav-item fs-5">
            <router-link to="/feedback" class="nav-link text-white" @click="menuOpen = false">
              Feedback
            </router-link>
          </li>

          <li class="nav-item fs-5">
            <router-link to="/" class="nav-link text-white" @click="menuOpen = false">
              {{ t.home }}
            </router-link>
          </li>

          <li class="nav-item fs-5">
            <router-link to="/actividades" v-if="userStore.isUsuarioFinal" class="nav-link text-white" @click="menuOpen = false">
              {{ t.activities }}
            </router-link>
          </li>

          <li class="nav-item fs-5">
            <router-link to="/comprar-abonos" v-if="userStore.isUsuarioFinal" class="nav-link text-white" @click="menuOpen = false">
              {{ t.seasonTickets }}
            </router-link>
          </li>

          <li class="nav-item fs-5">
            <router-link to="/foro"
              v-if="userStore.isUsuarioFinal || userStore.isAdminUsuarios || userStore.isAdminRaiz"
              class="nav-link text-white" @click="menuOpen = false">
              {{ t.forum }}
            </router-link>
          </li>

          <li class="nav-item fs-5">
            <router-link to="/contacto" v-if="!userStore.isAdmin" class="nav-link text-white" @click="menuOpen = false">
              {{ t.contact }}
            </router-link>
          </li>

          <li class="nav-item fs-5">
            <router-link to="/faq" v-if="!userStore.isAdmin" class="nav-link text-white" @click="menuOpen = false">
              {{ t.faq }}
            </router-link>
          </li>

          <!-- Login / logout -->
          <li class="nav-item fs-5">
            <a v-if="userStore.user" href="#" class="nav-link text-white" @click.prevent="logout" @click="menuOpen = false">
              {{ t.logout }}
            </a>

            <router-link v-else to="/login" class="nav-link text-white" @click="menuOpen = false">
              {{ t.login }}
            </router-link>
          </li>

          <!-- Perfil -->
          <li class="nav-item fs-5">
            <router-link to="/perfil" v-if="userStore.user" class="nav-link" @click="menuOpen = false">
              <i class="bi bi-person-fill text-white fs-4"></i>
            </router-link>
          </li>

          <!-- Idioma -->
          <li class="nav-item fs-5">
            <button class="btn btn-link nav-link text-white fs-5" @click="toggleLanguage"
              :title="language === 'es' ? 'Switch to English' : 'Cambiar a Español'">
              {{ language === "es" ? "🇪🇸" : "🇬🇧" }}
            </button>
          </li>

        </ul>
      </div>

    </div>
  </nav>
</template>

<script setup lang="ts">
import { inject, type Ref, ref, computed } from "vue";
import { useRouter } from "vue-router";

/* Importamos las comunicaciones con el backend a traves de nuestro Store para usar el usuario */
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/usuarioFinal";
import { useMonitorStore } from "@/stores/monitor";
import { useAdministradorStore } from "@/stores/administrador";

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

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

const menuOpen = ref(false);
const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const toggleLanguage = () => {
  language.value = language.value === "es" ? "en" : "es";
};

const logout = () => {
  activeStore.value.cerrarSesion();
  userStore.logout();
  router.push("/");
};
</script>

<style scoped>
.navbar .nav-link {
  cursor: pointer;
  transition: color 0.2s ease-in-out;
  margin-left: 14px;
}

.navbar .nav-link:hover {
  color: #0d6efd;
}
</style>
