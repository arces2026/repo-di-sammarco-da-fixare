<script setup>
import { ref } from 'vue';
import Navbar from './components/Navbar.vue';
</script>

<template>
    <Navbar></Navbar>
    <main>
        <RouterView />
    </main>
</template>

<style scoped>
    main{
        padding: 0.8rem;
    }
</style>
