<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <div class="container py-5">
      <!-- Header -->
      <div class="text-center mb-5">
        <h1 class="fw-bold text-primary">
          {{ t.faqTitle }}
        </h1>
      </div>

      <!-- Card FAQ -->
      <div class="card border-0 rounded-4 mx-auto"
           style="max-width: 800px; background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4">

          <div v-for="(q, index) in t.questions" :key="index" class="mb-4">
            <!-- Pregunta -->
            <h5 class="fw-semibold text-dark" 
                style="color: #0072ff;">
              {{ q.question }}
            </h5>

            <!-- Respuesta -->
            <p class="text-secondary">{{ q.answer }}</p>
            
            <!-- Separador colorido -->
            <hr class="my-3" style="border-top: 2px solid #ff6a00; border-radius: 2px;">
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { type Ref, inject } from "vue";
import { useI18n } from "@/useI18N";
import type { Language } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
</script>