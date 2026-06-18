<script setup>

import { useMouse } from '../composables/mouse.js'
const { x, y } = useMouse()

</script>

<template>La posizione del mouse è: {{ x }}, {{ y }}</template>