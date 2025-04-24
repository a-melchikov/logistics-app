<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getAllOrders, createOrder } from '@/api/orders'
import { getMe } from '@/api/auth'

interface Order {
    id: number
    client_name: string
    order_date: string
    cost: number
    status: string
}

interface User {
    id: number
    username: string
    role: string
}

// State
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

const user = ref<User | null>(null)
const isAdmin = computed(() => user.value?.role === 'admin')

const showModal = ref(false)
const newOrder = ref({ client_name: '', cost: null as number | null, order_date: '' })
const createError = ref('')
const creating = ref(false)

// Fetch current user and orders
async function fetchUser() {
    try {
        user.value = await getMe()
    } catch (err: any) {
        console.error('Ошибка при получении пользователя:', err)
    }
}
async function fetchOrders() {
    loading.value = true
    try {
        const params = Object.fromEntries(
            Object.entries(filters.value).filter(([_, v]) => v !== '' && v !== null)
        )
        orders.value = await getAllOrders(params)
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

// Modal handlers
function openModal() {
    createError.value = ''
    // Set default values, with order_date as current moment
    const now = new Date().toISOString().slice(0, 16)
    newOrder.value = { client_name: '', cost: null, order_date: now }
    showModal.value = true
}
function closeModal() {
    showModal.value = false
}

// Submit new order
async function submitNewOrder() {
    if (!newOrder.value.client_name || !newOrder.value.cost || !newOrder.value.order_date) {
        createError.value = 'Заполните все поля'
        return
    }
    creating.value = true
    try {
        await createOrder({
            ...newOrder.value,
            created_by_id: user.value!.id,
        })
        closeModal()
        await fetchOrders()
    } catch (err: any) {
        createError.value = err.message
    } finally {
        creating.value = false
    }
}

onMounted(async () => {
    await fetchUser()
    await fetchOrders()
})
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Список заказов</h2>

        <!-- Фильтры и кнопки -->
        <form class="row g-3 mb-4 align-items-end" @submit.prevent="fetchOrders">
            <div class="col-md-3">
                <label class="form-label">Клиент</label>
                <input v-model="filters.client_name" type="text" class="form-control" />
            </div>
            <div class="col-md-2">
                <label class="form-label">Стоимость от</label>
                <input v-model.number="filters.cost_from" type="number" class="form-control" />
            </div>
            <div class="col-md-2">
                <label class="form-label">Стоимость до</label>
                <input v-model.number="filters.cost_to" type="number" class="form-control" />
            </div>
            <div class="col-md-2">
                <label class="form-label">Дата</label>
                <input v-model="filters.order_date" type="date" class="form-control" />
            </div>
            <div class="col-md-2">
                <label class="form-label">Статус</label>
                <select v-model="filters.status" class="form-select">
                    <option value="">Все</option>
                    <option value="pending">В ожидании</option>
                    <option value="in_progress">В процессе</option>
                    <option value="completed">Завершён</option>
                </select>
            </div>
            <div class="col-md-auto d-flex gap-2">
                <button type="submit" class="btn btn-primary">Фильтровать</button>
                <button v-if="isAdmin" type="button" class="btn btn-success" @click="openModal">Добавить заказ</button>
            </div>
        </form>

        <!-- Список заказов -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border" role="status"></div>
        </div>
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-else>
            <div class="row row-cols-1 row-cols-md-2 g-4">
                <div v-for="order in orders" :key="order.id" class="col">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">Заказ #{{ order.id }}</h5>
                            <p><strong>Клиент:</strong> {{ order.client_name }}</p>
                            <p><strong>Дата:</strong> {{ new Date(order.order_date).toLocaleDateString() }}</p>
                            <p><strong>Стоимость:</strong> {{ order.cost }} ₽</p>
                            <span class="badge bg-secondary">{{ order.status }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="!orders.length" class="alert alert-info mt-4">Нет заказов.</div>
        </div>

        <!-- Модальное окно создания заказа через Teleport -->
        <teleport to="body">
            <div v-if="showModal">
                <div class="modal fade show d-block" tabindex="-1" role="dialog">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Создать заказ</h5>
                                <button type="button" class="btn-close" @click="closeModal"></button>
                            </div>
                            <div class="modal-body">
                                <div v-if="createError" class="alert alert-danger">{{ createError }}</div>
                                <form @submit.prevent="submitNewOrder">
                                    <div class="mb-3">
                                        <label class="form-label">Клиент</label>
                                        <input v-model="newOrder.client_name" type="text" class="form-control" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Стоимость</label>
                                        <input v-model.number="newOrder.cost" type="number" class="form-control" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Дата оформления</label>
                                        <input v-model="newOrder.order_date" type="datetime-local"
                                            class="form-control" />
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeModal">Отмена</button>
                                <button type="button" class="btn btn-primary" :disabled="creating"
                                    @click="submitNewOrder">
                                    {{ creating ? 'Сохраняем...' : 'Создать' }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-backdrop fade show"></div>
            </div>
        </teleport>
    </div>
</template>
