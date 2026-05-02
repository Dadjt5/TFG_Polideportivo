<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-4">

      <!-- PERFIL -->
      <div class="card mb-5 rounded-4" style="background-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <div class="card-body">

          <!-- CUANDO TIENE TDA -->
          <div v-if="usuarioFinalStore.hasTda" class="row align-items-center">
            <div class="col-md-6 text-start">
              <i class="bi bi-person-circle text-primary icono-perfil mb-2"></i>
              <p class="mb-1 fs-4">{{ usuarioFinalStore.usuarioFinal.nombre }} {{ usuarioFinalStore.usuarioFinal.apellidos }}</p>
              <p class="mb-1 fs-4">{{ usuarioFinalStore.usuarioFinal.email }}</p>
              <p class="mb-0 text-muted fs-5">{{ usuarioFinalStore.usuarioFinal.rol }}</p>
            </div>

            <div class="col-md-6 text-center">
              <QRCodeVue3 :value="qrValue" level="H" :size="100" />
            </div>
          </div>

          <!-- CUANDO NO TIENE TDA -->
          <div v-else class="text-center">
            <i class="bi bi-person-circle text-primary icono-perfil mb-2"></i>
            <p class="mb-1 fs-4">{{ usuarioFinalStore.usuarioFinal.nombre }} {{ usuarioFinalStore.usuarioFinal.apellidos }}</p>
            <p class="mb-1 fs-4">{{ usuarioFinalStore.usuarioFinal.email }}</p>
            <p class="mb-0 text-muted fs-5">{{ usuarioFinalStore.usuarioFinal.rol }}</p>
          </div>

        </div>
      </div>

      <div class="linea-fina"></div>

      <!-- OPCIONES -->
      <div class="row g-4 mt-4">

        <div class="col-md-6">
          <router-link to="/ver-tda" class="text-decoration-none text-dark">
            <div class="card h-100 option-card rounded-4" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-credit-card text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.viewTDA }}</h6>
                    <p class="text-muted mb-0 small">{{ t.moreViewTDA }}</p>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/estadisticas/usuarioFinal" class="text-decoration-none text-dark">
            <div class="card h-100 option-card rounded-4" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-bar-chart-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.viewUserStats }}</h6>
                    <p class="text-muted mb-0 small">{{ t.moreUserStats }}</p>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/modificar-datos" class="text-decoration-none text-dark">
            <div class="card h-100 option-card rounded-4" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-pencil-square text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.modifyPersonalData }}</h6>
                    <p class="text-muted mb-0 small">{{ t.moreModifyPersonalData }}</p>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

      </div>

      <!-- LOGOUT -->
      <div class="text-center mt-5">
        <button class="btn btn-danger rounded-pill px-4" @click="logout">
          <i class="bi bi-box-arrow-right me-2 fs-4"></i>
          {{ t.logout }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref, type Ref, inject } from 'vue';
import { useRouter } from "vue-router";
import QRCodeVue3 from 'qrcode-vue3';

/* Importamos las comunicaciones con el backend a traves de nuestro Store para guardar el usuario final */
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/usuarioFinal";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const authStore = useAuthStore();
const usuarioFinalStore = useUserStore();

const qrValue = computed(() =>
  JSON.stringify({
    id: usuarioFinalStore.tda?.id,
    usuario: usuarioFinalStore.usuarioFinal.nombre,
    token: usuarioFinalStore.tda?.codigo_qr,
  })
);

const logout = async () => {
  await usuarioFinalStore.cerrarSesion();
  authStore.logout();
  router.push("/");
};

onMounted(async () => {
  if (!usuarioFinalStore.hasTda) {
    await usuarioFinalStore.fetchTDA();
  }
});
</script>

<style scoped>
.icono-perfil {
  font-size: 6rem;
}
</style>
