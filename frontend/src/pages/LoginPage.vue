<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const username = ref('')
const password = ref('')
const router = useRouter()

const loginMessage = ref('')
const messageType = ref<'success' | 'error' | ''>('')

const handleLogin = async () => {
    loginMessage.value = ''
    messageType.value = ''

    try {
        await auth.login(username.value, password.value)
        loginMessage.value = 'Вход выполнен успешно!'
        messageType.value = 'success'
        setTimeout(() => {
            router.push('/orders')
        }, 1500)
    } catch (err: any) {
        loginMessage.value = err.message || 'Ошибка входа'
        messageType.value = 'error'
    }
}

const handleLogout = async () => {
    auth.logout()
    loginMessage.value = 'Вы вышли из системы'
    messageType.value = 'success'
}
</script>

<template>
    <div class="container mt-5" style="max-width: 400px">
        <h2 class="mb-4">Вход</h2>

        <div v-if="loginMessage" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger']">
            {{ loginMessage }}
        </div>

        <div v-if="!auth.user">
            <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя</label>
                <input v-model="username" id="username" class="form-control" />
            </div>

            <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input v-model="password" id="password" type="password" class="form-control" />
            </div>

            <button @click="handleLogin" class="btn btn-primary w-100">Войти</button>
        </div>

        <div v-else>
            <p class="alert alert-info">
                Добро пожаловать, <strong>{{ auth.user.username }}</strong>!<br />
                Ваша роль: <strong>{{ auth.user.role }}</strong>
            </p>
            <button @click="handleLogout" class="btn btn-danger w-100">Выйти</button>
        </div>
    </div>
</template>
