<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import Button from './ui/Button.vue';
import HeartIcon from './ui/HeartIcon.vue';

let username = ref("");
let password = ref("");

const authStore = useAuthStore();

async function login(){
    const payload = {
        username: username.value,
        password: password.value
    }

    try {
        const response = await fetch("http://localhost:3000/api/login",{
            method: "POST",
            headers: {
                'Content-type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok){
            throw new Error(`Errore del server ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        if(data){
            authStore.saveToken(data);
        }
            
    } catch (error) {
        console.error("Errore", error)
    }

    
}

</script>


<template>
    <form>
        <input type="text" placeholder="Username" v-model="username">
        <input type="password" placeholder="Password" v-model="password">
        <Button @click.prevent="login">
            <span>Login</span><HeartIcon/>
        </Button>
    </form>
</template>

<style scoped>
    input{
        padding: 5px;
    }
</style>