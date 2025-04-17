<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import { getTripsheetsForVehicle } from '@/api/tripsheets'

const props = defineProps<{ vehicleId: number }>()

const tripSheets = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const date = new Date().toISOString().slice(0, 10)

onMounted(async () => {
    try {
        const data = await getTripsheetsForVehicle(props.vehicleId)
        tripSheets.value = data.filter((sheet: any) =>
            sheet.start_time.startsWith(date)
        )
    } catch (err: any) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})

function getHour(timeStr: string): number {
    return new Date(timeStr).getHours()
}

function getDurationInHours(start: string, end: string): number {
    const s = new Date(start).getTime()
    const e = new Date(end).getTime()
    const hours = (e - s) / (1000 * 60 * 60)
    return Math.max(1, Math.round(hours))
}

function formatTimeRange(start: string, end: string): string {
    const s = new Date(start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    const e = new Date(end).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    return `${s} — ${e}`
}
</script>

<template>
    <div class="trip-sheet-widget">
        <h3 class="mb-4">📅 Путевой лист на <strong>{{ date }}</strong></h3>

        <div v-if="loading" class="text-center my-4">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status"></div>
        </div>

        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <table v-else class="table table-bordered text-center align-middle shadow-sm">
            <thead class="table-primary">
                <tr>
                    <th style="width: 140px;">Время</th>
                    <th>Заказы</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="hour in 24" :key="hour" :class="{ 'table-light': hour % 2 === 0 }">
                    <td class="fw-bold text-nowrap text-secondary">
                        {{ (hour - 1).toString().padStart(2, '0') }}:00 - {{ hour.toString().padStart(2, '0') }}:00
                    </td>

                    <!-- Если заказ начинается в этом часу -->
                    <template v-if="tripSheets.find(ts => getHour(ts.start_time) === hour - 1)">
                        <template v-for="sheet in tripSheets" :key="sheet.id">
                            <template v-if="getHour(sheet.start_time) === hour - 1">
                                <td :rowspan="getDurationInHours(sheet.start_time, sheet.end_time)"
                                    class="bg-info bg-opacity-25 border-info">
                                    <div class="p-1">
                                        <span class="badge bg-info text-dark mb-1">Заказ #{{ sheet.order_id
                                        }}</span><br />
                                        <small>{{ formatTimeRange(sheet.start_time, sheet.end_time) }}</small>
                                    </div>
                                </td>
                            </template>
                        </template>
                    </template>

                    <!-- Если час не занят (и не покрыт rowspan'ом) -->
                    <template v-else-if="!tripSheets.some(ts => {
                        const start = getHour(ts.start_time)
                        const end = getHour(ts.end_time)
                        return hour - 1 > start && hour - 1 < end
                    })">
                        <td class="text-muted">—</td>
                    </template>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.trip-sheet-widget {
    margin-top: 2rem;
}

td {
    transition: background-color 0.2s ease;
}

td.bg-info {
    cursor: pointer;
}
</style>
