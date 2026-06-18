<template>
    <div>
        <h1>Lista Utenti</h1>
        <table>
            <thead>
                <tr>
                    <th>N°</th>
                    <th>ID</th>
                    <th>Cognome</th>
                    <th>Nome</th>
                    <th>Età</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user, i in users" :key="user.id">
                    <td>{{ i + 1 }}</td>
                    <td>{{ user.id}}</td>
                    <td>{{ user.cognome }}</td>
                    <td>{{ user.nome }}</td>
                    <td>{{ user.eta }}</td>
                    <td>{{ user.email }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <br>
    <br>
</template>


<script setup lang="ts">

    interface User {
        id: number
        cognome: string
        nome: string
        eta: number
        email: string
    }

    const { users } = defineProps<{ users: User[] }>()

</script>