<template>
  <Navbar
    :language="language"
    :t="t"
    @toggle-language="toggleLanguage"
  />

  <Home :t="t"/>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import Navbar from "./components/Navbar.vue";
import Home from "./components/Home.vue";

const language = ref<"es" | "en">("es");

/* ------------------ Traducciones ------------------ */
const translations = {
  es: {
    home: "Inicio",
    forum: "Foro",
    contact: "Contacto",
    faq: "FAQ",
    login: "Log-in",
    welcome: "Bienvenido al Polideportivo XX",
    welcome2: "Inicia sesión para acceder a todas las funcionalidades",
    searchPlaceholder: "Buscar actividades o instalaciones...",
    searchButton: "Buscar",
    filterBy: "Filtrar por",
    activities: "Actividades",
    facilities: "Instalaciones",
    dayOfWeek: "Día de la semana",
    activityType: "Tipo de actividad",
    sessionTime: "Horario de sesión",
    facilityType: "Tipo de instalación",
    openingHours: "Horario de apertura",
  },
  en: {
    home: "Home",
    forum: "Forum",
    contact: "Contact",
    faq: "FAQ",
    login: "Log-in",
    welcome: "Welcome to Sports Center XX",
    welcome2: "Log in to access all features",
    searchPlaceholder: "Search activities or facilities...",
    searchButton: "Search",
    filterBy: "Filter by",
    activities: "Activities",
    facilities: "Facilities",
    dayOfWeek: "Day of the week",
    activityType: "Activity type",
    sessionTime: "Session time",
    facilityType: "Facility type",
    openingHours: "Opening hours",
  },
};

const t = computed(() => translations[language.value]);

const toggleLanguage = () => {
  language.value = language.value === "es" ? "en" : "es";
};
</script>
