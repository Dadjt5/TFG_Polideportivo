<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark sticky-top shadow py-3">
    <div class="container-fluid px-4">

      <span class="navbar-brand fw-bold fs-4">
        Polideportivo XX
      </span>

      <ul class="navbar-nav ms-auto flex-row align-items-center">
        <li class="nav-item fs-5">
          <router-link to="/" class="nav-link px-3 text-white">
            {{ t.home }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/contact" class="nav-link px-3 text-white">
            {{ t.contact }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/faq" class="nav-link px-3 text-white">
            {{ t.faq }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <router-link to="/login" class="nav-link px-3 text-white">
            {{ t.login }}
          </router-link>
        </li>

        <li class="nav-item fs-5">
          <button
            class="btn btn-link nav-link fs-4 px-3 text-white"
            @click="$emit('toggle-language')"
            :title="language === 'es' ? 'Switch to English' : 'Cambiar a Español'"
          >
            {{ language === 'es' ? '🇪🇸' : '🇬🇧' }}
          </button>
        </li>
      </ul>

    </div>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  language: "es" | "en";
  t: Record<string, string>;
}>();

defineEmits(["toggle-language"]);
</script>

<style scoped>
.navbar .nav-link {
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s ease-in-out;
}

.navbar .nav-link:hover {
  color: #0d6efd; /* primary de Bootstrap */
}
</style>
