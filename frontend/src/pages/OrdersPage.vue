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
        <LoadingSpinner v-if="loading" />
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-else>
            <div class="list-group">
                <OrderCard v-for="order in orders" :key="order.id" :order="order" />
            </div>
        </div>
    </div>
</template>
