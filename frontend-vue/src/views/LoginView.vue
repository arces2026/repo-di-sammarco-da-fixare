<script setup>
import Login from '@/components/Login.vue';

</script>

<template>
    <div class="container">
        <Login class="login"></Login>
    </div>
</template>

<style scoped>
    .container{
        display: flex;
        height: 100vh;
        justify-content: center;
        align-items: center;
    }

    .login{
        display: flex;
        flex-direction: column;
        gap:10px;
    }
</style>