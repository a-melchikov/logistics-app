<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <header class="bg-light py-3 shadow-sm mb-4 fixed-top">
        <div class="container d-flex justify-content-between align-items-center">
            <!-- Логотип по центру -->
            <div class="flex-grow-1 text-center">
                <h1 class="h3 font-weight-bold">Логистика</h1>
            </div>
            <!-- Навигация справа -->
            <nav>
                <RouterLink to="/orders" class="btn btn-link text-primary">Заказы</RouterLink>
                <RouterLink to="/vehicles" class="btn btn-link text-primary">Машины</RouterLink>
                <RouterLink to="/admin" class="btn btn-link text-primary">Админка</RouterLink>
                <RouterLink to="/login" class="btn btn-link text-primary">Вход</RouterLink>
            </nav>
        </div>
    </header>

    <main class="container px-4 mt-5">
        <RouterView />
    </main>
</template>

<style scoped>
header {
    z-index: 1000;
}

main {
    min-height: 80vh;
}

.mt-5 {
    margin-top: 5rem; /* Чтобы контент не перекрывался шапкой */
}
</style>
