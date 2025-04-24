<template>
    <div class="container my-5">
        <h2>Список заказов</h2>

        <!-- Загрузка -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
        </div>

        <!-- Таблица заказов -->
        <div v-else>
            <div v-if="orders.length">
                <div class="table-responsive">
                    <table class="table table-hover table-bordered align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Клиент</th>
                                <th>Стоимость</th>
                                <th>Дата заказа</th>
                                <th>Статус</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="order in orders" :key="order.id">
                                <td>{{ order.id }}</td>
                                <td>{{ order.client_name }}</td>
                                <td>{{ order.cost }}</td>
                                <td>{{ order.order_date }}</td>
                                <td>{{ order.status }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else class="alert alert-info">Нет заказов для отображения.</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const orders = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
    try {
        const res = await fetch('http://localhost:8000/orders/', {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!res.ok) {
            throw new Error('Ошибка при загрузке заказов');
        }

        orders.value = await res.json();
    } catch (err: any) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
});
</script>
