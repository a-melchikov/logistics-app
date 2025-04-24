<template>
    <div class="container my-5">
        <h2>Список машин</h2>

        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
        </div>

        <div v-else>
            <div v-if="vehicles.length">
                <div class="table-responsive">
                    <table class="table table-hover table-bordered align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Гос. номер</th>
                                <th>ФИО водителя</th>
                                <th>Тип машины</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="vehicle in vehicles" :key="vehicle.id">
                                <td>{{ vehicle.id }}</td>
                                <td>{{ vehicle.license_plate }}</td>
                                <td>{{ vehicle.driver_name }}</td>
                                <td>{{ vehicle.vehicle_type }}</td>
                                <td>
                                    <button @click="handleDelete(vehicle.id)" class="btn btn-danger btn-sm">
                                        Удалить
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else class="alert alert-info">Нет машин для отображения.</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { deleteVehicle } from '@/api/vehicles';

const vehicles = ref([]);
const loading = ref(true);
const error = ref('');

const fetchVehicles = async () => {
    try {
        const res = await fetch('http://localhost:8000/vehicles/', {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!res.ok) {
            throw new Error('Ошибка при загрузке машин');
        }

        vehicles.value = await res.json();
    } catch (err: any) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
};

const handleDelete = async (vehicleId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту машину?')) return;

    try {
        await deleteVehicle(vehicleId);
        await fetchVehicles();
    } catch (err: any) {
        error.value = err.message || 'Ошибка при удалении машины';
    }
};

onMounted(() => {
    fetchVehicles();
});
</script>