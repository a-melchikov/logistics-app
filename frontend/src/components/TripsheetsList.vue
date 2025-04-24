<template>
    <div class="container my-5">
        <h2>Список путевых листов</h2>

        <!-- Загрузка -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
        </div>

        <!-- Таблица путевых листов -->
        <div v-else>
            <div v-if="tripsheets.length">
                <div class="table-responsive">
                    <table class="table table-hover table-bordered align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>ID Машины</th>
                                <th>ID Заказа</th>
                                <th>Начало</th>
                                <th>Окончание</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="tripsheet in tripsheets" :key="tripsheet.id">
                                <td>{{ tripsheet.id }}</td>
                                <td>{{ tripsheet.vehicle_id }}</td>
                                <td>{{ tripsheet.order_id }}</td>
                                <td>{{ formatDateTime(tripsheet.start_time) }}</td>
                                <td>{{ formatDateTime(tripsheet.end_time) }}</td>
                                <td>
                                    <button @click="handleDelete(tripsheet.id)" class="btn btn-danger btn-sm">
                                        Удалить
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else class="alert alert-info">Нет путевых листов для отображения.</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAllTripsheets, deleteTripsheet } from '@/api/tripsheets'

interface Tripsheet {
    id: number
    vehicle_id: number
    order_id: number
    start_time: string
    end_time: string
}

const tripsheets = ref<Tripsheet[]>([])
const loading = ref(true)
const error = ref('')

const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString()
}

const fetchTripsheets = async () => {
    loading.value = true
    error.value = ''
    try {
        tripsheets.value = await getAllTripsheets()
    } catch (err: any) {
        error.value = err.message || 'Ошибка загрузки путевых листов'
        console.error('Ошибка при загрузке путевых листов:', err)
    } finally {
        loading.value = false
    }
}

const handleDelete = async (id: number) => {
    if (!confirm('Вы уверены, что хотите удалить этот путевой лист?')) return

    try {
        await deleteTripsheet(id)
        await fetchTripsheets()
    } catch (err: any) {
        error.value = err.message || 'Ошибка при удалении'
        console.error('Ошибка при удалении путевого листа:', err)
    }
}

onMounted(() => {
    fetchTripsheets()
})
</script>