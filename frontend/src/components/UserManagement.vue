<template>
    <div class="container my-5">
        <h2 class="mb-4">Управление пользователями</h2>

        <div v-if="loading" class="text-center my-4">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
        </div>

        <div v-else>
            <div v-if="users.length">
                <div class="table-responsive">
                    <table class="table table-hover table-bordered align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Имя пользователя</th>
                                <th>Роль</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in users" :key="user.id">
                                <td>{{ user.id }}</td>
                                <td :class="{ 'text-danger fw-bold': user.role === 'ADMIN' }">
                                    {{ user.username }}
                                </td>
                                <td>
                                    <span :class="{
                                        'badge bg-danger': user.role === 'ADMIN',
                                        'badge bg-warning text-dark': user.role === 'DISPATCHER',
                                        'badge bg-secondary': user.role === 'USER'
                                    }">
                                        {{ user.role }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else class="alert alert-info">Нет пользователей для отображения.</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

interface User {
    id: number;
    username: string;
    role: string;
}

const users = ref<User[]>([]);
const loading = ref(true);
const error = ref("");

const fetchUsers = async () => {
    try {
        const res = await fetch("http://localhost:8000/auth/all_users", {
            method: "GET",
            credentials: "include",
        });

        if (!res.ok) throw new Error("Ошибка при загрузке пользователей");

        users.value = await res.json();
    } catch (err: any) {
        error.value = err.message || "Произошла ошибка.";
    } finally {
        loading.value = false;
    }
};

onMounted(fetchUsers);
</script>