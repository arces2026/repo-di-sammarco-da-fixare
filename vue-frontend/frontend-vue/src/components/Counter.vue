<script setup>
    import {ref} from 'vue'
    const counter = ref(0); 
    
    function incrementa(){
        counter.value++
    }
</script>

<template>
    <h1>Counter {{ counter }}</h1>
    <button @click="incrementa">Incrementa</button>
</template>