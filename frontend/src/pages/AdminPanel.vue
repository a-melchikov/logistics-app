<script setup lang="ts">
import { ref, onMounted } from "vue";
import OrderList from "@/components/OrderList.vue";
import VehiclesList from "@/components/VehiclesList.vue";
import UserManagement from "@/components/UserManagement.vue";
import TripsheetsList from "@/components/TripsheetsList.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const selectedTab = ref("orders");
const loading = ref(true);
const error = ref("");

onMounted(async () => {
    try {
        await auth.fetchMe();
        if (!auth.isAuthenticated()) {
            error.value = "Вы не авторизованы!";
        }
    } catch (err) {
        error.value = "Ошибка при аутентификации";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="container my-5">
        <!-- Показываем только если авторизованы и нет ошибки -->
        <template v-if="auth.isAuthenticated() && !error">
            <h2 class="mb-4">Панель администратора</h2>

            <!-- Загрузка -->
            <div v-if="loading" class="text-center">
                <div class="spinner-border text-primary" role="status"></div>
            </div>

            <!-- Переключение вкладок -->
            <div v-if="!loading" class="mb-3">
                <button @click="selectedTab = 'orders'"
                    :class="{ 'btn btn-primary': selectedTab === 'orders', 'btn btn-secondary': selectedTab !== 'orders' }">
                    Заказы
                </button>
                <button @click="selectedTab = 'vehicles'"
                    :class="{ 'btn btn-primary': selectedTab === 'vehicles', 'btn btn-secondary': selectedTab !== 'vehicles' }">
                    Машины
                </button>
                <button @click="selectedTab = 'tripsheets'"
                    :class="{ 'btn btn-primary': selectedTab === 'tripsheets', 'btn btn-secondary': selectedTab !== 'tripsheets' }">
                    Путевые листы
                </button>
                <button @click="selectedTab = 'users'"
                    :class="{ 'btn btn-primary': selectedTab === 'users', 'btn btn-secondary': selectedTab !== 'users' }">
                    Пользователи
                </button>
            </div>

            <!-- Таблицы -->
            <div v-if="!loading">
                <div v-if="selectedTab === 'orders'">
                    <OrderList />
                </div>
                <div v-if="selectedTab === 'vehicles'">
                    <VehiclesList />
                </div>
                <div v-if="selectedTab === 'tripsheets'">
                    <TripsheetsList />
                </div>
                <div v-if="selectedTab === 'users'">
                    <UserManagement />
                </div>
            </div>
        </template>

        <!-- Сообщение об ошибке (неавторизованный доступ) -->
        <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
        </div>
    </div>
</template>