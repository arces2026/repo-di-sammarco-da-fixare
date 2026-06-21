<template>
    <button class="fancy">
        <slot></slot>
    </button>
</template>

<style>
    .fancy{
        padding: 10px;
        background-color: bisque;
        color: rgb(172, 103, 34);
        cursor: pointer;
    }
</style>