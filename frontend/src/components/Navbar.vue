<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark sticky-top shadow py-3">
    <div class="container-fluid px-4">

      <span class="navbar-brand fw-bold fs-4">
        <router-link to="/" class="nav-link px-3 text-white">
          Polideportivo XX
        </router-link>
      </span>

      <ul class="navbar-nav ms-auto flex-row align-items-center">
        <li class="nav-item fs-5">
          <router-link to="/" class="nav-link px-3 text-white">
            {{ t.home }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/actividades" v-if="userStore.role === 'usuario_final'" class="nav-link px-3 text-white">
            {{ t.activities }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/comprar-abonos" v-if="userStore.role === 'usuario_final'" class="nav-link px-3 text-white">
            {{ t.seasonTickets }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/foro" v-if="userStore.role === 'usuario_final' || userStore.role === 'administrador'" class="nav-link px-3 text-white">
            {{ t.forum }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/contacto" v-if="userStore.role !== 'administrador'" class="nav-link px-3 text-white">
            {{ t.contact }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/faq" v-if="userStore.role !== 'administrador'" class="nav-link px-3 text-white">
            {{ t.faq }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <a
            v-if="userStore.user"
            href="#"
            class="nav-link px-3 text-white"
            @click.prevent="logout"
          >
            {{ t.logout }}
          </a>

          <router-link to="/login" class="nav-link px-3 text-white" v-else>
            {{ t.login }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/perfil" v-if="userStore.user" class="nav-link">
            <i class="bi bi-person-fill px-3 text-white me-2 fs-2"></i>
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <button
            class="btn btn-link nav-link fs-4 px-3 text-white"
            @click="toggleLanguage"
            :title="language === 'es' ? 'Switch to English' : 'Cambiar a Español'"
          >
            {{ language === "es" ? "🇪🇸" : "🇬🇧" }}
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { inject, type Ref, computed } from "vue";
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
  if(userStore.role == "usuario_final") {
    return usuarioFinalStore;
  }

  if(userStore.role == "monitor") {
    return monitorStore;
  }

  return administradorStore;
});

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
}

.navbar .nav-link:hover {
  color: #0d6efd;
}
</style>
