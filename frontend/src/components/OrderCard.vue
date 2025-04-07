<script setup lang="ts">
defineProps<{
    order: {
        id: number
        client_name: string
        order_date: string
        cost: number
        status: string
    }
}>()
</script>

<template>
    <div class="order-card card p-4 mb-3 shadow-sm">
        <h4 class="card-title">Заказ #{{ order.id }}</h4>
        <div class="card-body">
            <p><strong>Клиент:</strong> {{ order.client_name }}</p>
            <p><strong>Дата:</strong> {{ order.order_date }}</p>
            <p><strong>Стоимость:</strong> {{ order.cost }} ₽</p>
            <p><strong>Статус:</strong> {{ order.status }}</p>
        </div>
    </div>
</template>

<style scoped>
.order-card {
    background-color: #f8f9fa;
}
</style>
