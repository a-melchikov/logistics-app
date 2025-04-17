import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as null | { id: number; username: string; role: string },
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

      await this.fetchMe();
    },

    async fetchMe() {
      const res = await fetch("http://localhost:8000/auth/me/", {
        method: "GET",
        credentials: "include",
      });

      if (res.ok) {
        this.user = await res.json();
      } else {
        this.user = null;
      }
    },

    async logout() {
      fetch("http://localhost:8000/auth/logout/", {
        method: "POST",
        credentials: "include",
      }).finally(() => {
        this.user = null;
        document.cookie = "users_access_token=; Max-Age=0";
      });
    },

    isAuthenticated() {
      return this.user !== null;
    },
  },
});
