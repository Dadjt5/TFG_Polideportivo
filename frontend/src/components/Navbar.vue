<template>
      <!-- NAVBAR -->
    <nav class="bg-slate-900 text-white sticky top-0 z-50 shadow-md">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex justify-between items-center h-16">
          <span class="text-lg font-semibold tracking-wide">
            Polideportivo XX
          </span>

          <div class="flex items-center gap-8">
            <button class="text-lg hover:text-blue-300">
              {{ t.home }}
            </button>
            <button class="text-lg hover:text-blue-300">
              {{ t.contact }}
            </button>
            <button class="text-lg hover:text-blue-300">
              {{ t.faq }}
            </button>
            <button class="text-lg hover:text-blue-300">
              {{ t.login }}
            </button>

            <button
              @click="toggleLanguage"
              class="text-2xl hover:scale-110 transition"
              :title="language === 'es' ? 'Switch to English' : 'Cambiar a Español'"
            >
              {{ language === "es" ? "🇪🇸" : "🇬🇧" }}
            </button>
          </div>
        </div>
      </div>
    </nav>
</template>

<script setup>
  import { ref, computed } from "vue";

  const language = ref<"es" | "en">("es");

  const translations = {
    es: {
      home: "Inicio",
      forum: "Foro",
      contact: "Contacto",
      faq: "FAQ",
      login: "Log-in",
    },
    en: {
      home: "Home",
      forum: "Forum",
      contact: "Contact",
      faq: "FAQ",
      login: "Log-in",
    },
  };

  const t = computed(() => translations[language.value]);

  const toggleLanguage = () => {
    language.value = language.value === "es" ? "en" : "es";
  };
</script>

<style scoped>
.navbar {
  background-color: #064180;
  padding: 0.5rem 1rem;
  transition: transform 0.3s ease;
}

.navbar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.navbar-hidden {
  transform: translateY(-100%);
  /* Mueve el navbar fuera de la vista */
  transition: transform 0.3s ease;
  /* Animación suave */
}

.navbar-brand {
  color: white;
  font-weight: bold;
  text-decoration: none;
  font-size: 1.25rem;
}

.navbar-toggler {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  padding: 0.5rem;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%28255, 255, 255, 0.7%29' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

.navbar-nav {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding-left: 0;
}

.nav-item .nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem;
  transition: color 0.3s;
}

.nav-item .nav-link:hover {
  color: #ffdd57;
}
</style>