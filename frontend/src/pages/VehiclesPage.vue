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
        <LoadingSpinner v-if="loading" />
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-else>
            <div class="list-group">
                <VehicleCard v-for="vehicle in vehicles" :key="vehicle.id" :vehicle="vehicle" />
            </div>
        </div>
    </div>
</template>
