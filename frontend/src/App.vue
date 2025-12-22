<template>
  <div>
    <div class="container mt-4">
      <Navbar />
      <Home />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import Navbar from "./components/Navbar.vue";
import Home from "./components/Home.vue";


</script>

<style>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>