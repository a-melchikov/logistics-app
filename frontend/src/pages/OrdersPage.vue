<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import OrderCard from '@/components/OrderCard.vue'
import { getAllOrders } from '@/api/orders'

interface Order {
    id: number
    client_name: string
    order_date: string
    cost: number
    status: string
}

const loading = ref(true)
const error = ref('')
const orders = ref<Order[]>([])

onMounted(async () => {
    try {
        orders.value = await getAllOrders()
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Список заказов</h2>

        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-else>
            <div class="row row-cols-1 row-cols-md-2 g-4">
                <div v-for="order in orders" :key="order.id" class="col">
                    <div class="card shadow-sm h-100">
                        <div class="card-body">
                            <h5 class="card-title">Заказ #{{ order.id }}</h5>
                            <p class="card-text"><strong>Клиент:</strong> {{ order.client_name }}</p>
                            <p class="card-text"><strong>Дата:</strong> {{ order.order_date }}</p>
                            <p class="card-text"><strong>Стоимость:</strong> {{ order.cost }} ₽</p>
                            <span class="badge bg-secondary">{{ order.status }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>