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
                <p v-if="order.status === 'in_progress'" class="text-primary fw-bold">
                    Заказ выполняется
                </p>
                <p v-else>
                    <strong>Нету</strong>
                </p>
            </div>

            <div class="card shadow-sm mt-4" v-if="order.status !== 'in_progress'">
                <div class="card-body">
                    <h5 class="card-title mb-4">Создать путевой лист</h5>

                    <div v-if="submitError" class="alert alert-danger mb-3">{{ submitError }}</div>

                    <form @submit.prevent="createTripsheetHandler">
                        <div class="mb-3">
                            <label for="vehicleSelect" class="form-label">Выберите машину</label>
                            <select id="vehicleSelect" class="form-select" v-model="selectedVehicleId" required>
                                <option value="" disabled>Выберите машину</option>
                                <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
                                    {{ vehicle.vehicle_type }} ({{ vehicle.license_plate }}) - {{ vehicle.driver_name }}
                                </option>
                            </select>
                        </div>

                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label for="startTime" class="form-label">Время начала</label>
                                <input type="datetime-local" class="form-control" id="startTime" v-model="startTime"
                                    required>
                            </div>
                            <div class="col-md-6">
                                <label for="endTime" class="form-label">Время окончания</label>
                                <input type="datetime-local" class="form-control" id="endTime" v-model="endTime"
                                    required>
                            </div>
                        </div>

                        <div class="d-flex justify-content-end">
                            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                                <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status"></span>
                                Создать путевой лист
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getOrderById } from '@/api/orders'
import { getAllVehicles } from '@/api/vehicles'
import { createTripsheet } from '@/api/tripsheets'

interface Order {
    id: number
    client_name: string
    order_date: string
    cost: number
    status: string
    comment?: string
}

interface Vehicle {
    id: number
    driver_name: string
    vehicle_type: string
    license_plate: string
}

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const error = ref('')
const submitError = ref('')
const order = ref<Order | null>(null)
const vehicles = ref<Vehicle[]>([])
const selectedVehicleId = ref<number | null>(null)
const startTime = ref('')
const endTime = ref('')
const isSubmitting = ref(false)

const fetchOrderDetails = async () => {
    try {
        const orderId = route.params.id as string
        order.value = await getOrderById(Number(orderId))
        await fetchVehicles()
    } catch (err: any) {
        error.value = 'Ошибка при загрузке данных заказа: ' + (err.message || 'неизвестная ошибка')
        console.error('Order loading error:', err)
    } finally {
        loading.value = false
    }
}

const fetchVehicles = async () => {
    try {
        vehicles.value = await getAllVehicles({})
    } catch (err: any) {
        error.value = 'Ошибка при загрузке списка машин: ' + (err.message || 'неизвестная ошибка')
        console.error('Vehicles loading error:', err)
    }
}

const createTripsheetHandler = async () => {
    if (!selectedVehicleId.value || !startTime.value || !endTime.value) {
        submitError.value = 'Заполните все обязательные поля'
        return
    }

    if (!order.value?.id) {
        submitError.value = 'Не удалось определить заказ'
        return
    }

    isSubmitting.value = true
    submitError.value = ''

    try {
        console.log('Creating tripsheet with:', {
            vehicle_id: selectedVehicleId.value,
            order_id: order.value.id,
            start_time: startTime.value,
            end_time: endTime.value
        })

        const response = await createTripsheet({
            vehicle_id: selectedVehicleId.value,
            order_id: order.value.id,
            start_time: startTime.value,
            end_time: endTime.value
        })

        console.log('Tripsheet created:', response)
        alert('Путевой лист успешно создан!')

    } catch (err: any) {
        console.error('Tripsheet creation error:', err)
        submitError.value = err.message || 'Ошибка при создании путевого листа'
    } finally {
        isSubmitting.value = false
    }
}

onMounted(() => {
    fetchOrderDetails()
})

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