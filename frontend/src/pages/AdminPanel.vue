<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const users = ref([]) // Добавлено для хранения списка пользователей
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    if (!auth.isAuthenticated()) {
        error.value = "Вы не авторизованы!";
        loading.value = false;
        return;
    }

    try {
        const token = auth.token; // Получаем токен из auth store
        if (!token) {
            error.value = "Токен не найден!";
            loading.value = false;
            return;
        }

        const res = await fetch('http://localhost:8000/auth/all_users/', {
            credentials: 'include',  // Обеспечиваем, что куки передаются
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`, // Передаем токен в заголовке
            }
        });

        if (!res.ok) throw new Error('Ошибка при загрузке пользователей');

        users.value = await res.json(); // Сохраняем пользователей в переменную
    } catch (err: any) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div>
        <h2>Панель администратора</h2>
        <div v-if="loading">Загрузка...</div>
        <div v-if="error">{{ error }}</div>
        <ul v-else>
            <li v-for="user in users" :key="user.id">
                {{ user.username }} — {{ user.role }}
            </li>
        </ul>
    </div>
</template>
