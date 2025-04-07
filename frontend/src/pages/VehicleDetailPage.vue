<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import TripSheetWidget from '@/components/TripSheetWidget.vue'
import { getVehicleById, getVehicleOrders } from '@/api/vehicles'

const route = useRoute()
const vehicleId = Number(route.params.id)

const vehicle = ref<{
    driver_name: string
    vehicle_type: string
    license_plate: string
} | null>(null)
const orders = ref<any[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    try {
        const [vehicleData, vehicleOrders] = await Promise.all([
            getVehicleById(vehicleId),
            getVehicleOrders(vehicleId),
        ])

        vehicle.value = vehicleData
        orders.value = vehicleOrders
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Информация о машине</h2>
        <LoadingSpinner v-if="loading" />
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-else>
            <div v-if="vehicle" class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Машина #{{ vehicleId }}</h5>
                    <p><strong>Водитель:</strong> {{ vehicle.driver_name || 'Не указан' }}</p>
                    <p><strong>Тип:</strong> {{ vehicle.vehicle_type || 'Не указан' }}</p>
                    <p><strong>Номер:</strong> {{ vehicle.license_plate || 'Не указан' }}</p>
                </div>
            </div>
            <div v-else class="alert alert-warning">Информация о машине не найдена.</div>

            <h3 class="mt-4">История заказов:</h3>
            <div v-if="orders.length" class="list-group">
                <div v-for="order in orders" :key="order.id" class="list-group-item mb-3">
                    <p><strong>Клиент:</strong> {{ order.client_name }}</p>
                    <p><strong>Статус:</strong> {{ order.status }}</p>
                </div>
            </div>
            <div v-else>
                <p class="alert alert-info">Нет заказов для этой машины.</p>
            </div>

            <TripSheetWidget :vehicleId="vehicleId" />
        </div>
    </div>
</template>
