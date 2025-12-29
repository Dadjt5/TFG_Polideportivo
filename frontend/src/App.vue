<template>
  <Navbar/>
  <router-view />
</template>

<script setup lang="ts">
import { ref, provide } from "vue";
import Navbar from "./components/Navbar.vue";

const language = ref("es");
provide("language", language);
</script>
