<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import VehicleCard from '@/components/VehicleCard.vue'
import { getAllVehicles } from '@/api/vehicles'

interface Vehicle {
    id: number
    driver_name: string
    vehicle_type: string
    license_plate: string
}

const loading = ref(true)
const error = ref('')
const vehicles = ref<Vehicle[]>([])

onMounted(async () => {
    try {
        vehicles.value = await getAllVehicles()
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Список машин</h2>

        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-else>
            <div class="row row-cols-1 row-cols-md-2 g-4">
                <div v-for="vehicle in vehicles" :key="vehicle.id" class="col">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">Машина #{{ vehicle.id }}</h5>
                            <p class="card-text"><strong>Водитель:</strong> {{ vehicle.driver_name || '—' }}</p>
                            <p class="card-text"><strong>Тип:</strong> {{ vehicle.vehicle_type || '—' }}</p>
                            <p class="card-text"><strong>Госномер:</strong> {{ vehicle.license_plate || '—' }}</p>
                            <RouterLink :to="`/vehicles/${vehicle.id}`" class="btn btn-outline-primary btn-sm mt-2">
                                Подробнее</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>