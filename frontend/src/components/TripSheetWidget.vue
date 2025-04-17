<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import { getTripsheetsForVehicle } from '@/api/tripsheets'
import { getAllOrders } from '@/api/orders'

const props = defineProps<{ vehicleId: number }>()

const tripSheets = ref<any[]>([])
const orders = ref<any[]>([])
const selectedOrder = ref<any>(null)
const selectedTime = ref<string>('')
const selectedRow = ref<number | null>(null)

const loading = ref(true)
const error = ref('')
const date = new Date().toISOString().slice(0, 10)

onMounted(async () => {
    try {
        const data = await getTripsheetsForVehicle(props.vehicleId)
        tripSheets.value = data.filter((sheet: any) =>
            sheet.start_time.startsWith(date)
        )

        orders.value = await getAllOrders()
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

function handleFreeCellClick(row: number) {
    selectedRow.value = row
    selectedOrder.value = null
    selectedTime.value = `${(row - 1).toString().padStart(2, '0')}:00 - ${row.toString().padStart(2, '0')}:00`
}

function handleSelectOrder(order: any) {
    selectedOrder.value = order
}

async function saveTripSheet() {
    if (!selectedOrder.value || !selectedRow.value) return

    const startTime = `${date}T${(selectedRow.value - 1).toString().padStart(2, '0')}:00:00`
    const endTime = `${date}T${selectedRow.value.toString().padStart(2, '0')}:00:00`

    const tripSheetData = {
        vehicle_id: props.vehicleId,
        order_id: selectedOrder.value.id,
        start_time: startTime,
        end_time: endTime
    }

    try {
        await saveTripSheetAPI(tripSheetData)
        tripSheets.value.push({ ...tripSheetData, order_id: selectedOrder.value.id })
        selectedOrder.value = null
        selectedRow.value = null
        selectedTime.value = ''
    } catch (err) {
        error.value = 'Ошибка при сохранении путевого листа'
    }
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
                        <td class="text-muted" @click="handleFreeCellClick(hour)">—</td>
                    </template>
                </tr>
            </tbody>
        </table>

        <!-- Модальное окно для выбора заказа и времени -->
        <div v-if="selectedRow !== null" class="modal fade show" style="display: block;" tabindex="-1"
            aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Выбор заказа для {{ selectedTime }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                            @click="selectedRow = null"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="orders.length">
                            <ul class="list-group">
                                <li v-for="order in orders" :key="order.id" class="list-group-item"
                                    @click="handleSelectOrder(order)">
                                    Заказ #{{ order.id }}: {{ order.client_name }}
                                </li>
                            </ul>
                        </div>
                        <div v-else>
                            <p>Нет доступных заказов.</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="selectedRow = null">Закрыть</button>
                        <button type="button" class="btn btn-primary" @click="saveTripSheet">Сохранить</button>
                    </div>
                </div>
            </div>
        </div>
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
