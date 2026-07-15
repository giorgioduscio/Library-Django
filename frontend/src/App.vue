<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div style="min-height: 100vh; background: linear-gradient(0deg, #333, #000);">
    <Navbar />
    <RouterView />
  </div>
</template>
