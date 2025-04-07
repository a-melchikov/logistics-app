<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const username = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = async () => {
    try {
        await auth.login(username.value, password.value)
        router.push('/orders')
    } catch (err) {
        alert('Ошибка входа')
    }
}
</script>

<template>
    <div class="container my-5">
        <h2 class="text-center mb-4">Вход</h2>
        <div class="col-md-6 mx-auto">
            <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя</label>
                <input v-model="username" id="username" class="form-control form-control-lg" placeholder="Введите имя пользователя" />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input v-model="password" id="password" type="password" class="form-control form-control-lg"
                    placeholder="Введите пароль" />
            </div>
            <button @click="handleLogin" class="btn btn-primary btn-lg w-100">Войти</button>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 500px;
}
</style>
