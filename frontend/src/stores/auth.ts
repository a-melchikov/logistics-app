import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as null | { id: number; username: string; role: string },
    token: "",
  }),

  actions: {
    async login(username: string, password: string) {
      const res = await fetch("/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) throw new Error("Неверные данные");

      const data = await res.json();
      this.token = data.access_token;
      document.cookie = `users_access_token=${data.access_token}; HttpOnly`;

      // Получить текущего пользователя
      await this.fetchMe();
    },

    async fetchMe() {
      const res = await fetch("/auth/me/", {
        headers: {
          Authorization: `Bearer ${this.token}`,
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
  },
});
