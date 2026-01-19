<template>
  <div class="min-vh-100 bg-light">
    <div class="container py-5">
      <h1 class="text-center mb-5">{{ t.TDAEmptyTitle }}</h1>

      <div class="card shadow-lg rounded-4 mx-auto p-4" style="max-width: 480px;">
        <div class="card-body text-center">
          <i class="bi bi-credit-card-fill text-primary display-4 mb-3"></i>
          <p class="mb-4">{{ t.TDAinstructions }}</p>

          <input
            type="text"
            class="form-control text-center mb-3"
            :placeholder="t.inputPlaceholder"
            v-model="codigo"
          />

          <button class="btn btn-primary w-100 mb-4" @click="vincularTarjeta">{{ t.linkButton }}</button>

          <p class="text-danger" v-if="error">{{ t.TDAerror }}</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { type Ref, inject, ref } from "vue";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../../useI18N";
import { useI18n } from "../../useI18N";

/* Importamos la forma de tratar de validar la TDA desde el backend */
import { validarTDA } from "../../services/usuarioFinalService";

import { useUserStore } from '../../stores/usuarioFinal';

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore();

const codigo = ref('');
const error = ref(false);

const vincularTarjeta = async () => {
  if (codigo.value.trim() === '') {
    error.value = true
    return;
  }

  const respuesta = await validarTDA({codigo: codigo.value})

  if(respuesta.status == "error") {
    error.value = true
  } else {
    error.value = false
    await usuarioFinalStore.fetchTDA();
  }
};

</script>