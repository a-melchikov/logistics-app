<script setup lang="ts">
defineProps<{
    vehicle: {
        id: number
        driver_name: string
        vehicle_type: string
        license_plate: string
    }
}>()
</script>

<template>
    <div class="order-card card p-4 mb-3 shadow-sm">
        <router-link :to="`/vehicles/${vehicle.id}`" class="text-decoration-none">
            <h4 class="card-title">Машина #{{ vehicle.id }}</h4>
        </router-link>
        <div class="card-body">
            <p><strong>Водитель:</strong> {{ vehicle.driver_name }}</p>
            <p><strong>Тип:</strong> {{ vehicle.vehicle_type }}</p>
            <p><strong>Номер:</strong> {{ vehicle.license_plate }}</p>
        </div>
    </div>
</template>

<style scoped>
.vehicle-card {
    transition: background-color 0.2s ease;
}

.vehicle-card:hover {
    background-color: #f8f9fa;
}
</style>
