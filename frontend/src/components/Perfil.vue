<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">

      <div class="card shadow-sm h-100 mb-5">
        <div class="card-body text-center">
          <i class="bi bi-person-circle text-primary icono-perfil"></i>
          
          <p class="mb-1 fs-4">{{ data.nombre }} {{ data.apellidos }}</p>
          <p class="mb-1 fs-4">{{ data.email }}</p>
          <p class="mb-0 text-muted fs-5">{{ data.rol }}</p>
        </div>
      </div>

      <div class="linea-fina"></div>

      <div class="row g-4 mt-4">
        <div class="col-md-6">
          <div class="card shadow-sm h-100 option-card" role="button" @click="verTarjeta">
            <div class="card-body">
              <div class="d-flex align-items-center gap-3">
                <i class="bi bi-credit-card text-primary fs-3"></i>
                <div>
                  <h6 class="mb-1">{{ t.viewTDA }}</h6>
                  <p class="text-muted mb-0 small">
                    {{ t.moreViewTDA }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card shadow-sm h-100 option-card" role="button" @click="verFavoritos">
            <div class="card-body">
              <div class="d-flex align-items-center gap-3">
                <i class="bi bi-heart text-primary fs-3"></i>
                <div>
                  <h6 class="mb-1">{{ t.favoriteSports }}</h6>
                  <p class="text-muted mb-0 small">
                    {{ t.moreFavoriteSports }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card shadow-sm h-100 option-card" role="button" @click="modificarDatos">
            <div class="card-body">
              <div class="d-flex align-items-center gap-3">
                <i class="bi bi-nut text-primary fs-3"></i>
                <div>
                  <h6 class="mb-1">{{ t.modifyPersonalData }}</h6>
                  <p class="text-muted mb-0 small">
                    {{ t.moreModifyPersonalData }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card shadow-sm h-100 option-card" role="button" @click="verAbonos">
            <div class="card-body">
              <div class="d-flex align-items-center gap-3">
                <i class="bi bi-ticket-perforated text-primary fs-3"></i>
                <div>
                  <h6 class="mb-1">{{ t.viewTickets }}</h6>
                  <p class="text-muted mb-0 small">
                    {{ t.moreViewTickets }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

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
import { ref, type Ref, inject, onMounted } from 'vue';
import { useRouter } from "vue-router";

/* Importamos las comunicaciones con el backend a traves de nuestro Store para guardar las estadisticas */
import { useAuthStore } from "../stores/auth";

/* Importamos la funcion para obtener el usuario final del backend */
import { getUsuarioFinal } from '../services/usuarioFinalService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const userStore = useAuthStore();

const data = ref({
  nombre: '',
  apellidos: '',
  email: '',
  rol: ''
});

const logout = () => {
  userStore.logout();
  router.push("/");
};

onMounted(async () => {
  try {
    const user = await getUsuarioFinal(userStore.user?.usuario_final_id);

    data.value = {
      nombre: user.nombre,
      apellidos: user.apellidos,
      email: userStore.user?.email || '',
      rol: user.rol
    };
  } catch(e) {
    console.log("Error al obtener el usuario", e)
  }
})
</script>

<style scoped>
.icono-perfil {
  font-size: 6rem;
}
</style>
