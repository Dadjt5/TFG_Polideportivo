<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-5">
      <h2 class="mb-4 fw-bold text-primary d-flex align-items-center gap-2">
        <i class="bi bi-bell-fill"></i>
        {{ t.newNotification }}
      </h2>

      <div class="card p-4 shadow-lg border-0 rounded-4"
           style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <div class="mb-3">
          <label class="form-label fw-medium">{{ t.title }}</label>
          <input v-model="form.titulo" class="form-control rounded-3" />
        </div>

        <div class="mb-3">
          <label class="form-label fw-medium">{{ t.description }}</label>
          <textarea v-model="form.descripcion" class="form-control rounded-3" rows="3"></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label fw-medium">{{ t.recipients }}</label>
          <select v-model="form.tipo" class="form-select rounded-3">
            <option value="TODOS">{{ t.allUsers }}</option>
            <option value="USUARIOS_FINALES">{{ t.finalUsers }}</option>
            <option value="MONITORES">{{ t.monitors }}</option>
            <option value="ADMINISTRADORES">{{ t.admins }}</option>
            <option value="ACTIVIDAD">{{ t.byActivity }}</option>
            <option value="INSTALACION">{{ t.byFacility }}</option>
            <option value="PABELLON">{{ t.byPavilion }}</option>
          </select>
        </div>

        <div v-if="form.tipo === 'ACTIVIDAD'" class="mb-3">
          <label class="form-label fw-medium">{{ t.activity }}</label>
          <select v-model="form.actividad_id" class="form-select rounded-3">
            <option v-for="act in actividades" :key="act.id" :value="act.id">
              {{ act.nombre }}
            </option>
          </select>
        </div>

        <button class="btn btn-primary mt-3 rounded-3 px-4 py-2 fw-semibold d-flex align-items-center gap-2" @click="enviar">
          <i class="bi bi-send-fill"></i>
          {{ t.sendNotification }}
        </button>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, inject, onMounted } from "vue";
import { useRouter } from "vue-router";

import { getInstalacionesSimples, getActividadesSimples, getPabellonesSimples } from "@/services/listadoService";
import { nuevaNotificacion } from '@/services/crearRecursosService'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const loading = ref(false);
const error = ref<string | null>(null);
const success = ref(false);

const form = ref({
  titulo: "",
  descripcion: "",
  tipo: "TODOS", // TODOS | USUARIOS_FINALES | MONITORES | ADMINISTRADORES | ACTIVIDAD | INSTALACION | PABELLON
  actividad_id: null as number | null,
  instalacion_id: null as number | null,
  pabellon_id: null as number | null,
});

const actividades = ref<any[]>([]);
const instalaciones = ref<any[]>([]);
const pabellones = ref<any[]>([]);

const validar = () => {
  if (!form.value.titulo || !form.value.descripcion) {
    error.value = "Debes completar título y descripción.";
    return false;
  }

  if (form.value.tipo === "ACTIVIDAD" && !form.value.actividad_id) {
    error.value = "Selecciona una actividad.";
    return false;
  }

  if (form.value.tipo === "INSTALACION" && !form.value.instalacion_id) {
    error.value = "Selecciona una instalación.";
    return false;
  }

  if (form.value.tipo === "PABELLON" && !form.value.pabellon_id) {
    error.value = "Selecciona un pabellón.";
    return false;
  }

  return true;
};

const enviar = async () => {
  error.value = null;
  success.value = false;

  if (!validar()) return;

  loading.value = true;

  try {
    await nuevaNotificacion({
      titulo: form.value.titulo,
      descripcion: form.value.descripcion,
      usuarios: form.value.tipo,
      actividad_id: form.value.actividad_id,
      instalacion_id: form.value.instalacion_id,
      pabellon_id: form.value.pabellon_id,
    });

    success.value = true;
    router.push({ name: 'notificaciones' })
  } catch (e: any) {
    error.value = e.response?.data?.respuesta
    console.error(e);
  } finally {
    loading.value = false;
  }
};


onMounted(async () => {
  try {
    actividades.value = await getActividadesSimples();
    instalaciones.value = await getInstalacionesSimples();
    pabellones.value = await getPabellonesSimples();
  } catch (e) {
    console.error(e);
  }
});
</script>