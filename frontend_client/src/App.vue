<template>
  <router-view v-slot="{ Component, route }">
    <transition name="fade-scale" mode="out-in">
      <component :is="Component" :key="route.path" />
    </transition>
  </router-view>
</template>

<script setup>
</script>

<style>
html, body, #app { margin:0; padding:0; width:100%; height:100%; overflow:auto; }
.fade-scale-enter-active { transition: all 0.25s var(--ease-out-expo); }
.fade-scale-leave-active { transition: all 0.2s var(--ease-in-out); }
.fade-scale-enter-from { opacity: 0; transform: scale(0.96); }
.fade-scale-leave-to { opacity: 0; }
</style>
