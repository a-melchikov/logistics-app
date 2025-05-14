<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import { getTripsheetsForVehicle, createTripsheet } from '@/api/tripsheets'
import { getAllOrders } from '@/api/orders'

const props = defineProps<{ vehicleId: number }>()

const tripSheets = ref<any[]>([])
const pendingOrders = ref<any[]>([])
const selectedOrder = ref<any>(null)

const selectionStart = ref<number | null>(null)
const selectionEnd = ref<number | null>(null)

const loading = ref(true)
const error = ref('')
const date = new Date().toISOString().slice(0, 10)

const successMessage = ref<string>('')
const errorMessage = ref<string>('')

async function loadData() {
    loading.value = true
    try {
        const data = await getTripsheetsForVehicle(props.vehicleId)
        tripSheets.value = data.filter((sheet: any) =>
            sheet.start_time.startsWith(date)
        )
        const allOrders = await getAllOrders()
        pendingOrders.value = allOrders.filter(
            (order: any) => order.status === 'pending'
        )
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
    const s = new Date(start).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
    })
    const e = new Date(end).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
    })
    return `${s} — ${e}`
}

function handleFreeCellClick(hour: number) {
    if (selectionStart.value === null) {
        selectionStart.value = hour
        selectionEnd.value = null
    } else if (selectionEnd.value === null) {
        selectionEnd.value = hour
    } else {
        selectionStart.value = hour
        selectionEnd.value = null
        selectedOrder.value = null
    }
    errorMessage.value = ''
}

function handleSelectOrder(order: any) {
    selectedOrder.value = order
}

async function saveTripSheet() {
    if (
        selectionStart.value === null ||
        selectionEnd.value === null ||
        !selectedOrder.value
    ) {
        errorMessage.value = 'Выберите диапазон и заказ'
        return
    }
    const startHour =
        Math.min(selectionStart.value, selectionEnd.value) - 1
    const endHour = Math.max(selectionStart.value, selectionEnd.value)
    const start = `${date}T${String(startHour).padStart(2, '0')}:00:00`
    const end = `${date}T${String(endHour).padStart(2, '0')}:00:00`

    try {
        await createTripsheet({
            vehicle_id: props.vehicleId,
            order_id: selectedOrder.value.id,
            start_time: start,
            end_time: end,
        })
        successMessage.value = 'Путевой лист успешно создан!'
        selectionStart.value = null
        selectionEnd.value = null
        selectedOrder.value = null
        loadData()
    } catch (err: any) {
        errorMessage.value =
            err.response?.data?.detail || 'Ошибка создания путевого листа'
    }
}
</script>

<template>
    <div class="trip-sheet-widget">
        <h3 class="mb-4">Путевой лист на <strong>{{ date }}</strong></h3>

        <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
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
                <tr v-for="hour in 24" :key="hour" :class="{
                    // зелёный для выбранных
                    'table-success':
                        (selectionStart !== null && selectionEnd === null && hour === selectionStart) ||
                        (selectionStart !== null && selectionEnd !== null &&
                            hour >= Math.min(selectionStart, selectionEnd) &&
                            hour <= Math.max(selectionStart, selectionEnd)),
                    // остальное зеброй только если не выделено
                    'table-light':
                        hour % 2 === 0 &&
                        !(
                            (selectionStart !== null && selectionEnd === null && hour === selectionStart) ||
                            (selectionStart !== null && selectionEnd !== null &&
                                hour >= Math.min(selectionStart, selectionEnd) &&
                                hour <= Math.max(selectionStart, selectionEnd))
                        )
                }">
                    <td class="fw-bold text-nowrap text-secondary">
                        {{ (hour - 1).toString().padStart(2, '0') }}:00 —
                        {{ hour.toString().padStart(2, '0') }}:00
                    </td>

                    <!-- Занятые -->
                    <template v-if="tripSheets.some(ts => getHour(ts.start_time) === hour - 1)">
                        <template v-for="sheet in tripSheets" :key="sheet.id">
                            <template v-if="getHour(sheet.start_time) === hour - 1">
                                <td :rowspan="getDurationInHours(sheet.start_time, sheet.end_time)"
                                    class="bg-info bg-opacity-25 border-info">
                                    <div class="p-1">
                                        <span class="badge bg-info text-dark mb-1">
                                            Заказ #{{ sheet.order_id }}
                                        </span><br />
                                        <small>{{ formatTimeRange(sheet.start_time, sheet.end_time) }}</small>
                                    </div>
                                </td>
                            </template>
                        </template>
                    </template>

                    <!-- Свободные -->
                    <template v-else-if="!tripSheets.some(ts => {
                        const s = getHour(ts.start_time), e = getHour(ts.end_time)
                        return hour - 1 > s && hour - 1 < e
                    })">
                        <td class="text-muted" @click="handleFreeCellClick(hour)">—</td>
                    </template>
                </tr>
            </tbody>
        </table>

        <!-- Модальное окно после двух кликов -->
        <div v-if="selectionStart !== null && selectionEnd !== null" class="modal fade show d-block" tabindex="-1"
            aria-labelledby="modalLabel">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            Выбран интервал:
                            {{ String(Math.min(selectionStart, selectionEnd) - 1).padStart(2, '0')
                            }}:00 —
                            {{ String(Math.max(selectionStart, selectionEnd)).padStart(2, '0')
                            }}:00
                        </h5>
                        <button type="button" class="btn-close" @click="() => {
                            selectionStart = null
                            selectionEnd = null
                            selectedOrder = null
                        }"></button>
                    </div>
                    <div class="modal-body">
                        <ul v-if="pendingOrders.length" class="list-group">
                            <li v-for="order in pendingOrders" :key="order.id" class="list-group-item"
                                :class="{ active: selectedOrder && selectedOrder.id === order.id }"
                                @click="handleSelectOrder(order)">
                                Заказ #{{ order.id }}: {{ order.client_name }}
                                <span class="badge bg-warning text-dark float-end">PENDING</span>
                            </li>
                        </ul>
                        <div v-else>
                            <p>Нет доступных заказов.</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="() => {
                            selectionStart = null
                            selectionEnd = null
                            selectedOrder = null
                        }">
                            Отмена
                        </button>
                        <button type="button" class="btn btn-primary" :disabled="!selectedOrder" @click="saveTripSheet">
                            Сохранить
                        </button>
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
    background-color: #0d6efd !important;
    color: #fff;
}
</style>
