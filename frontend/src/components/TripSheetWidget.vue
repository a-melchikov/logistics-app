<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import { getTripsheetsForVehicle, createTripsheet } from '@/api/tripsheets'
import { getAllOrders } from '@/api/orders'

const props = defineProps<{ vehicleId: number }>()

const tripSheets = ref<any[]>([])
const pendingOrders = ref<any[]>([])
const selectedOrder = ref<any>(null)
const selectedTime = ref<string>('')
const selectedRow = ref<number | null>(null)

const loading = ref(true)
const error = ref('')
const date = new Date().toISOString().slice(0, 10)

// Загрузка данных
async function loadData() {
    loading.value = true
    try {
        const data = await getTripsheetsForVehicle(props.vehicleId)
        tripSheets.value = data.filter((sheet: any) => sheet.start_time.startsWith(date))

        const allOrders = await getAllOrders()
        pendingOrders.value = allOrders.filter((order: any) => order.status === 'pending')
    } catch (err: any) {
        error.value = err.message || 'Ошибка загрузки данных'
    } finally {
        loading.value = false
    }
}

onMounted(loadData)

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

    const start = `${date}T${(selectedRow.value - 1).toString().padStart(2, '0')}:00:00`
    const end = `${date}T${selectedRow.value.toString().padStart(2, '0')}:00:00`

    await createTripsheet({
        vehicle_id: props.vehicleId,
        order_id: selectedOrder.value.id,
        start_time: start,
        end_time: end
    })
}

</script>

<template>
    <div class="trip-sheet-widget">
        <h3 class="mb-4">Путевой лист на <strong>{{ date }}</strong></h3>

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

                    <!-- Занятые часы -->
                    <template v-if="tripSheets.some(ts => getHour(ts.start_time) === hour - 1)">
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

                    <!-- Свободные часы -->
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

        <!-- Модальное окно -->
        <div v-if="selectedRow !== null" class="modal fade show d-block" tabindex="-1" aria-labelledby="modalLabel">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalLabel">Выбор заказа для {{ selectedTime }}</h5>
                        <button type="button" class="btn-close" @click="selectedRow = null"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="pendingOrders.length">
                            <ul class="list-group">
                                <li v-for="order in pendingOrders" :key="order.id" class="list-group-item"
                                    :class="{ active: selectedOrder && selectedOrder.id === order.id }"
                                    @click="handleSelectOrder(order)">
                                    Заказ #{{ order.id }}: {{ order.client_name }}
                                    <span class="badge bg-warning text-dark float-end">PENDING</span>
                                </li>
                            </ul>
                        </div>
                        <div v-else>
                            <p>Нет доступных заказов со статусом PENDING.</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="selectedRow = null">Закрыть</button>
                        <button type="button" class="btn btn-primary" :disabled="!selectedOrder"
                            @click="saveTripSheet">Сохранить</button>
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

td.text-muted {
    cursor: pointer;
}

.list-group-item {
    cursor: pointer;
}

.list-group-item.active {
    background-color: #0d6efd;
    color: white;
}
</style>
