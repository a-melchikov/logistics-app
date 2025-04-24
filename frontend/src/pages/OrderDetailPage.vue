<template>
    <div class="container my-5" v-if="order">
        <h2 class="mb-4">Детали заказа #{{ order.id }}</h2>

        <div v-if="loading" class="text-center">
            <div class="spinner-border" role="status"></div>
        </div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-if="order">
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title">Заказ #{{ order.id }}</h5>
                    <p><strong>Клиент:</strong> {{ order.client_name }}</p>
                    <p><strong>Дата заказа:</strong> {{ new Date(order.order_date).toLocaleDateString() }}</p>
                    <p><strong>Стоимость:</strong> {{ order.cost }} ₽</p>
                    <p><strong>Статус:</strong>
                        <span :class="statusClass(order.status)" class="badge">{{ order.status }}</span>
                    </p>
                </div>
            </div>
            <div class="mb-3">
                <h5>Дополнительная информация</h5>
                <p><strong>Комментарий:</strong> {{ order.comment || 'Нет' }}</p>
            </div>
            <div v-if="isAdmin" class="mb-3">
                <button class="btn btn-warning">Редактировать заказ</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getOrderById } from '@/api/orders'

interface Order {
    id: number
    client_name: string
    order_date: string
    cost: number
    status: string
    comment?: string
}

const route = useRoute()
const loading = ref(true)
const error = ref('')
const order = ref<Order | null>(null)

const fetchOrderDetails = async () => {
    try {
        const orderId = route.params.id as string
        order.value = await getOrderById(Number(orderId))
    } catch (err: any) {
        error.value = 'Ошибка при загрузке данных заказа.'
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchOrderDetails()
})

// Определение стилей для статуса
const statusClass = (status: string) => {
    switch (status) {
        case 'pending':
            return 'bg-warning'
        case 'in_progress':
            return 'bg-primary'
        case 'completed':
            return 'bg-success'
        default:
            return 'bg-secondary'
    }
}
</script>

<style scoped>
.card {
    background-color: #f8f9fa;
}
</style>