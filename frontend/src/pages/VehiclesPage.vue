<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { getAllVehicles, createVehicle } from '@/api/vehicles'
import { getMe } from '@/api/auth'

interface Vehicle {
    id: number
    driver_name: string
    vehicle_type: string
    license_plate: string
}

interface User {
    id: number
    username: string
    role: string
}

const loading = ref(true)
const error = ref('')
const vehicles = ref<Vehicle[]>([])
const user = ref<User | null>(null)
const isAdmin = computed(() => user.value?.role === 'admin')

const filters = ref({
    driver_name: '',
    vehicle_type: '',
    license_plate: '',
})

// Модальное окно создания машины
const showModal = ref(false)
const newVehicle = ref({ driver_name: '', vehicle_type: '', license_plate: '' })
const createError = ref('')
const creating = ref(false)

async function fetchUser() {
    try {
        user.value = await getMe()
    } catch (err: any) {
        console.error('Ошибка при получении пользователя:', err)
    }
}

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

function openModal() {
    createError.value = ''
    newVehicle.value = { driver_name: '', vehicle_type: '', license_plate: '' }
    showModal.value = true
}

function closeModal() {
    showModal.value = false
}

// Создание новой машины
async function submitNewVehicle() {
    if (!newVehicle.value.driver_name || !newVehicle.value.vehicle_type || !newVehicle.value.license_plate) {
        createError.value = 'Заполните все поля'
        return
    }
    creating.value = true
    try {
        await createVehicle(newVehicle.value)
        closeModal()
        await fetchVehicles()
    } catch (err: any) {
        createError.value = err.message
    } finally {
        creating.value = false
    }
}

onMounted(async () => {
    await fetchUser()
    await fetchVehicles()
})
</script>

<template>
    <div class="container my-5">
        <h2 class="mb-4">Список машин</h2>

        <form class="row g-3 mb-4" @submit.prevent="fetchVehicles">
            <div class="col-md-4">
                <label class="form-label">ФИО водителя</label>
                <input v-model="filters.driver_name" type="text" class="form-control" />
            </div>
            <div class="col-md-4">
                <label class="form-label">Госномер</label>
                <input v-model="filters.license_plate" type="text" class="form-control" />
            </div>
            <div class="col-md-4">
                <label class="form-label">Тип машины</label>
                <select v-model="filters.vehicle_type" class="form-select">
                    <option value="">Все</option>
                    <option value="car">Легковая</option>
                    <option value="truck">Грузовая</option>
                    <option value="van">Фургон</option>
                </select>
            </div>

            <div class="col-md-auto d-flex gap-2">
                <button type="submit" class="btn btn-primary">Фильтровать</button>
                <button v-if="isAdmin" type="button" class="btn btn-success" @click="openModal">Добавить машину</button>
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

        <!-- Модальное окно создания машины -->
        <teleport to="body">
            <div v-if="showModal">
                <div class="modal fade show d-block" tabindex="-1" role="dialog">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Создать машину</h5>
                                <button type="button" class="btn-close" @click="closeModal"></button>
                            </div>
                            <div class="modal-body">
                                <div v-if="createError" class="alert alert-danger">{{ createError }}</div>
                                <form @submit.prevent="submitNewVehicle">
                                    <div class="mb-3">
                                        <label class="form-label">ФИО водителя</label>
                                        <input v-model="newVehicle.driver_name" type="text" class="form-control" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Тип машины</label>
                                        <select v-model="newVehicle.vehicle_type" class="form-select">
                                            <option value="car">Легковая</option>
                                            <option value="truck">Грузовая</option>
                                            <option value="van">Фургон</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Госномер</label>
                                        <input v-model="newVehicle.license_plate" type="text" class="form-control" />
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeModal">Отмена</button>
                                <button type="button" class="btn btn-primary" :disabled="creating"
                                    @click="submitNewVehicle">
                                    {{ creating ? 'Создаём...' : 'Создать' }}
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
