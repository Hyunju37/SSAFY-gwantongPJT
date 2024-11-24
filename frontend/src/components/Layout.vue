<!-- src/components/Layout.vue -->
<template>
    <div class="layout">
      <Header />
      <main>
        <slot />
      </main>
      <Footer />
    </div>
  </template>
  
  <script setup>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'
  </script>
  
  <style scoped>
  .layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #F7F7F7;
  }
  
  main {
    flex: 1;
  }
  </style>
  