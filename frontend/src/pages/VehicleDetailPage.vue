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

        <!-- Спиннер загрузки -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <!-- Основной контент -->
        <div v-else>
            <!-- Информация о машине -->
            <div v-if="vehicle" class="card shadow-sm mb-4">
                <div class="card-header bg-primary text-white">
                    Машина #{{ vehicleId }}
                </div>
                <div class="card-body">
                    <p><strong>Водитель:</strong> {{ vehicle.driver_name || 'Не указан' }}</p>
                    <p><strong>Тип:</strong> {{ vehicle.vehicle_type || 'Не указан' }}</p>
                    <p><strong>Номер:</strong> {{ vehicle.license_plate || 'Не указан' }}</p>
                </div>
            </div>

            <div v-else class="alert alert-warning">Информация о машине не найдена.</div>

            <!-- История заказов -->
            <h3 class="mt-4">История заказов</h3>

            <div v-if="orders.length" class="row row-cols-1 row-cols-md-2 g-3 mt-3">
                <div v-for="order in orders" :key="order.id" class="col">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">Заказ #{{ order.id }}</h5>
                            <p><strong>Клиент:</strong> {{ order.client_name }}</p>
                            <p><strong>Статус:</strong>
                                <span class="badge bg-secondary">{{ order.status }}</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else class="alert alert-info mt-3">Нет заказов для этой машины.</div>

            <!-- Виджет путевого листа -->
            <div class="mt-5">
                <TripSheetWidget :vehicleId="vehicleId" />
            </div>
        </div>
    </div>
</template>
