<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import { getTripsheetsForVehicle } from '@/api/tripsheets'

// Получаем пропс vehicleId
const props = defineProps<{
    vehicleId: number
}>()

const tripSheets = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const date = new Date().toISOString().slice(0, 10)

onMounted(async () => {
    try {
        // Получаем путевые листы для конкретной машины
        const data = await getTripsheetsForVehicle(props.vehicleId)

        // Фильтруем данные по дате, оставляем только те, которые соответствуют текущей
        tripSheets.value = data.filter((sheet: any) => sheet.start_time.startsWith(date))
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="trip-sheet-widget">
        <h3 class="mb-3">Путевой лист на {{ date }}</h3>
        <div v-if="loading">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status"></div>
        </div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <table v-else class="table table-bordered table-sm">
            <thead>
                <tr>
                    <th class="p-2">Время</th>
                    <th class="p-2">Заказ</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="sheet in tripSheets" :key="sheet.id">
                    <td class="p-2">{{ new Date(sheet.start_time).toLocaleTimeString() }}</td>
                    <td class="p-2">{{ sheet.order_id || '—' }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.trip-sheet-widget {
    margin-top: 1rem;
}
</style>
