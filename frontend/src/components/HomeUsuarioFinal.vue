<template>
  <div class="min-vh-100 bg-light">

    <!-- MAIN -->
    <main class="container py-4">

      <!-- HERO -->
      <h1 class="text-center fw-bold mb-4">
        {{ t.welcome }}
      </h1>

      <!-- NOTIFICATIONS + QUICK ACTIONS -->
      <div class="row g-4 mb-4">

        <!-- Notifications -->
        <div class="col-lg-8">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center gap-2">
                  <Bell />
                  <h5 class="mb-0">{{ t.notifications }}</h5>
                  <span v-if="unreadNotifications"
                        class="badge bg-danger">
                    {{ unreadNotifications }}
                  </span>
                </div>
                <a href="#" class="text-primary small">
                  {{ t.seeAll }} →
                </a>
              </div>

              <div class="bg-light rounded p-3 mb-2">
                <strong>Recordatorio de actividad</strong>
                <p class="mb-0 small text-muted">
                  Mañana tienes una sesión programada…
                </p>
              </div>

              <div class="bg-light rounded p-3">
                <strong>Modificación de horario</strong>
                <p class="mb-0 small text-muted">
                  Se ha cambiado el horario de una actividad…
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="col-lg-4">
          <div class="card shadow-sm mb-3">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <BarChart3 />
                <h6 class="mb-0">{{ t.statsTitle }}</h6>
              </div>
              <button class="btn btn-primary w-100">
                {{ t.statsButton }}
              </button>
            </div>
          </div>

          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <CalendarCheck />
                <h6 class="mb-0">{{ t.bookingsTitle }}</h6>
              </div>
              <button class="btn btn-success w-100">
                {{ t.bookingsButton }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SEARCH -->
      <div class="card shadow-sm mb-4">
        <div class="card-body d-flex gap-3">
          <Search />
          <input
            class="form-control"
            :placeholder="t.searchPlaceholder"
          />
          <button class="btn btn-primary">
            {{ t.searchButton }}
          </button>
        </div>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from "vue";
import {
  Search,
  Activity,
  Building2,
  Clock,
  Calendar,
  User,
  Bell,
  BarChart3,
  CalendarCheck
} from "lucide-vue-next";

/* ========= ESTADO ========= */
const language = ref<"es" | "en">("es");
const unreadNotifications = ref(3);

/* Filtros */
const selectedDays = ref<string[]>([]);
const selectedActivityTypes = ref<string[]>([]);
const activityStartTime = ref("");
const activityEndTime = ref("");

const selectedFacilityTypes = ref<string[]>([]);
const facilityStartTime = ref("");
const facilityEndTime = ref("");

/* Modales */
const showDayFilter = ref(false);
const showActivityTypeFilter = ref(false);
const showActivityTimeFilter = ref(false);
const showFacilityTypeFilter = ref(false);
const showFacilityTimeFilter = ref(false);

/* ========= TRADUCCIONES ========= */
const translations = {
  es: {
    welcome: "Bienvenido a la web del polideportivo",
    home: "Inicio",
    forum: "Foro",
    contact: "Contacto",
    faq: "FAQ",
    logout: "Logout",
    notifications: "Notificaciones",
    seeAll: "Ver todas",
    statsTitle: "Estadísticas de uso",
    statsButton: "Ver estadísticas",
    bookingsTitle: "Reservas realizadas",
    bookingsButton: "Ver reservas",
    searchPlaceholder: "Buscar actividades o instalaciones...",
    searchButton: "Buscar",
    filterBy: "Filtrar por",
    activities: "Actividades",
    facilities: "Instalaciones"
  },
  en: {
    welcome: "Welcome to the sports center",
    home: "Home",
    forum: "Forum",
    contact: "Contact",
    faq: "FAQ",
    logout: "Logout",
    notifications: "Notifications",
    seeAll: "See all",
    statsTitle: "Usage statistics",
    statsButton: "View statistics",
    bookingsTitle: "Your bookings",
    bookingsButton: "View bookings",
    searchPlaceholder: "Search activities or facilities...",
    searchButton: "Search",
    filterBy: "Filter by",
    activities: "Activities",
    facilities: "Facilities"
  }
};

const t = computed(() => translations[language.value]);

const toggleLanguage = () => {
  language.value = language.value === "es" ? "en" : "es";
};
</script>
