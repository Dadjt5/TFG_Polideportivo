<template>
  <div class="min-vh-100 bg-light">

    <div class="container py-5">
      <div class="text-center mb-5">
        <h1 class="fw-semibold text-dark">
          {{ t.faqTitle }}
        </h1>
      </div>

      <div class="card shadow-lg border-0 rounded-4 mx-auto" style="max-width: 800px">
        <div class="card-body p-4">

          <div v-for="(q, index) in t.questions" :key="index" class="mb-4">
            <h5 class="fw-semibold text-dark">
              {{ q.question }}
            </h5>
            <p class="text-secondary">{{ q.answer }}</p>
            <hr class="my-3">
          </div>

        </div>
      </div>
    </div>

  </div>
</template>


<script setup lang="ts">
import { type Ref, ref, inject } from "vue";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
</script>
