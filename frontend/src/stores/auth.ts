// stores/auth.ts
import { defineStore } from 'pinia';

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as null | { id: number; username: string; role: string },
    token: "",
  }),

  actions: {
    async login(username: string, password: string) {
      const res = await fetch("http://localhost:8000/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) throw new Error("Неверные данные");

      const data = await res.json();
      this.token = data.access_token;
      document.cookie = `users_access_token=${this.token}; HttpOnly`;

      await this.fetchMe(); // Запрос данных о текущем пользователе после авторизации
    },

    async fetchMe() {
      const token = this.getTokenFromCookie();
      if (!token) return;

      const res = await zfetch("http://localhost:8000/auth/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        this.user = await res.json();
      }
    },

    logout() {
      this.token = "";
      this.user = null;
      document.cookie = "users_access_token=; Max-Age=0";
    },

    getTokenFromCookie(): string | null {
      const match = document.cookie.match(new RegExp("(^| )users_access_token=([^;]+)"));
      return match ? match[2] : null;
    },

    // Проверка авторизации
    isAuthenticated() {
      return this.token !== "" && this.user !== null;
    }
  },
});
