<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const users = ref([]);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
    try {
        await auth.fetchMe();

        if (!auth.isAuthenticated()) {
            error.value = "Вы не авторизованы!";
            loading.value = false;
            return;
        }

        const res = await fetch("http://localhost:8000/auth/all_users/", {
            credentials: "include",
        });

        if (!res.ok) throw new Error("Ошибка при загрузке пользователей");

        users.value = await res.json();
    } catch (err: any) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Панель администратора</h2>

        <!-- Загрузка -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
        </div>

        <!-- Список пользователей -->
        <div v-else>
            <div v-if="users.length">
                <div class="table-responsive">
                    <table class="table table-hover table-bordered align-middle">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Имя пользователя</th>
                                <th scope="col">Роль</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in users" :key="user.id">
                                <td>{{ user.id }}</td>
                                <td>{{ user.username }}</td>
                                <td>
                                    <span class="badge" :class="{
                                        'bg-primary': user.role === 'admin',
                                        'bg-secondary': user.role === 'manager',
                                        'bg-info': user.role === 'user',
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
