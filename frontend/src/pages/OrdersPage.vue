<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
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

const filters = ref({
    client_name: '',
    cost_from: null as number | null,
    cost_to: null as number | null,
    order_date: '',
    status: '',
})

async function fetchOrders() {
    loading.value = true
    try {
        const filteredParams = Object.fromEntries(
            Object.entries(filters.value).filter(([_, v]) => v !== '' && v !== null)
        )
        orders.value = await getAllOrders(filteredParams)
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

onMounted(fetchOrders)
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Список заказов</h2>

        <form class="row g-3 mb-4" @submit.prevent="fetchOrders">
            <div class="col-md-3">
                <input v-model="filters.client_name" type="text" class="form-control" placeholder="Клиент" />
            </div>
            <div class="col-md-2">
                <input v-model.number="filters.cost_from" type="number" class="form-control"
                    placeholder="Стоимость от" />
            </div>

            <div class="col-md-2">
                <input v-model.number="filters.cost_to" type="number" class="form-control" placeholder="Стоимость до" />
            </div>

            <div class="col-md-2">
                <input v-model="filters.order_date" type="date" class="form-control" />
            </div>
            <div class="col-md-3">
                <select v-model="filters.status" class="form-select">
                    <option value="">Статус</option>
                    <option value="pending">В ожидании</option>
                    <option value="in_progress">В процессе</option>
                    <option value="completed">Завершён</option>
                </select>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary w-100">Фильтровать</button>
            </div>
        </form>

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
                            <p class="card-text"><strong>Дата:</strong> {{ new
                                Date(order.order_date).toLocaleDateString() }}</p>
                            <p class="card-text"><strong>Стоимость:</strong> {{ order.cost }} ₽</p>
                            <span class="badge bg-secondary">{{ order.status }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="!orders.length" class="alert alert-info mt-4">Нет заказов по заданным параметрам.</div>
        </div>
    </div>
</template>
