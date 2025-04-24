<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
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

const filters = ref({
    driver_name: '',
    vehicle_type: '',
    license_plate: '',
})

async function fetchVehicles() {
    loading.value = true
    try {
        const filteredParams = Object.fromEntries(
            Object.entries(filters.value).filter(([_, v]) => v !== '')
        )
        vehicles.value = await getAllVehicles(filteredParams)
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

onMounted(fetchVehicles)
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Список машин</h2>

        <form class="row g-3 mb-4" @submit.prevent="fetchVehicles">
            <div class="col-md-4">
                <input v-model="filters.driver_name" type="text" class="form-control" placeholder="ФИО водителя" />
            </div>
            <div class="col-md-4">
                <input v-model="filters.license_plate" type="text" class="form-control" placeholder="Госномер" />
            </div>
            <div class="col-md-4">
                <select v-model="filters.vehicle_type" class="form-select">
                    <option value="">Тип машины</option>
                    <option value="car">Легковая</option>
                    <option value="truck">Грузовая</option>
                    <option value="van">Фургон</option>
                </select>
            </div>

            <div class="col-md-2">
                <button type="submit" class="btn btn-primary w-100">Фильтровать</button>
            </div>
        </form>

        <div v-if="loading" class="text-center">
            <LoadingSpinner />
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
                            <div class="d-flex justify-content-end">
                                <RouterLink :to="`/vehicles/${vehicle.id}`" class="btn btn-outline-primary btn-sm">
                                    Подробнее
                                </RouterLink>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="!vehicles.length" class="alert alert-info mt-4">
                Нет машин по заданным параметрам.
            </div>
        </div>
    </div>
</template>
