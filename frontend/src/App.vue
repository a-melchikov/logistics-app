<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const auth = useAuthStore()
const router = useRouter()

onMounted(() => {
    auth.fetchMe()
})

const handleLogout = () => {
    auth.logout()
    router.push('/login')
}
</script>

<template>
    <div id="app" class="d-flex flex-column min-vh-100">
        <!-- Header -->
        <header class="bg-primary text-white py-3 shadow">
            <div class="container d-flex justify-content-between align-items-center">
                <h1 class="h4 mb-0">Логистика</h1>
                <nav class="d-flex gap-3">
                    <RouterLink class="text-white fw-semibold" to="/orders">Заказы</RouterLink>
                    <RouterLink class="text-white fw-semibold" to="/vehicles">Машины</RouterLink>
                    <RouterLink v-if="auth.user?.role === 'admin'" class="text-white fw-semibold" to="/admin">Админка
                    </RouterLink>

                    <template v-if="auth.user">
                        <span class="text-white">Привет, {{ auth.user.username }}</span>
                        <button class="btn btn-outline-light btn-sm" @click="handleLogout">Выйти</button>
                    </template>
                    <template v-else>
                        <RouterLink class="btn btn-light btn-sm" to="/login">Вход</RouterLink>
                    </template>
                </nav>
            </div>
        </header>

        <!-- Main content -->
        <main class="flex-grow-1 container py-4">
            <RouterView />
        </main>

        <!-- Footer -->
        <footer class="bg-light text-center text-muted py-3 border-top mt-auto">
            &copy; 2025 Логистика
        </footer>
    </div>
</template>
