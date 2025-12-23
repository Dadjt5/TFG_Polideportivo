<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark sticky-top shadow">
    <div class="container-fluid px-4">

      <span class="navbar-brand fw-bold">
        Polideportivo XX
      </span>

      <ul class="navbar-nav ms-auto flex-row align-items-center">
        <li class="nav-item">
          <router-link to="/" class="nav-link px-3 text-white">
            {{ t.home }}
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/contact" class="nav-link px-3 text-white">
            {{ t.contact }}
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/faq" class="nav-link px-3 text-white">
            {{ t.faq }}
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/login" class="nav-link px-3 text-white">
            {{ t.login }}
          </router-link>
        </li>

        <li class="nav-item">
          <button
            class="nav-link fs-4 px-3 btn btn-link text-white"
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
    transition: color 0.2s;
  }

  .navbar .nav-link:hover {
    color: #0d6efd;
  }
</style>
