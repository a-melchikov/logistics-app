<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const auth = useAuthStore()
const users = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    try {
        const res = await fetch('/auth/all_users/', {
            headers: {
                Authorization: `Bearer ${auth.token}`,
            }
        })

        if (!res.ok) throw new Error('Ошибка при загрузке пользователей')

        users.value = await res.json()
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div>
        <h2>Панель администратора</h2>
        <LoadingSpinner v-if="loading" />
        <div v-if="error">{{ error }}</div>
        <ul v-else>
            <li v-for="user in users" :key="user.id">
                {{ user.username }} — {{ user.role }}
            </li>
        </ul>
    </div>
</template>
