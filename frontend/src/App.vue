<template>
  <Navbar/>
  <Home/>
</template>

<script setup lang="ts">
import { ref, provide } from "vue";
import Navbar from "./components/Navbar.vue";
import Home from "./components/Home.vue";

const language = ref("es");
provide("language", language);

</script>
