import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as null | { id: number; username: string; role: string },
    accessToken: localStorage.getItem("access_token") || "",
    refreshToken: localStorage.getItem("refresh_token") || "",
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
      this.accessToken = data.access_token;
      this.refreshToken = data.refresh_token;

      localStorage.setItem("access_token", this.accessToken);
      localStorage.setItem("refresh_token", this.refreshToken);

      await this.fetchMe();
    },

    async refreshAccessToken() {
      try {
        const res = await fetch("http://localhost:8000/auth/refresh/", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh_token: this.refreshToken }),
        });

        if (!res.ok) throw new Error("Ошибка обновления токена");

        const data = await res.json();
        this.accessToken = data.access_token;

        localStorage.setItem("access_token", this.accessToken);
      } catch (error) {
        console.error("Не удалось обновить токен:", error);
        this.logout();
      }
    },

    async fetchMe() {
      try {
        const res = await this.authFetch("http://localhost:8000/auth/me/");
        if (res.ok) {
          this.user = await res.json();
        } else {
          throw new Error("Ошибка при получении информации о пользователе");
        }
      } catch (err) {
        console.error("Ошибка при получении пользователя:", err);
        this.user = null;
      }
    },

    async authFetch(url: string, options: RequestInit = {}) {
      const headers = new Headers(options.headers || {});
      if (this.accessToken) {
        headers.append("Authorization", `Bearer ${this.accessToken}`);
      }

      let res = await fetch(url, { ...options, headers });

      if (res.status === 401) {
        await this.refreshAccessToken();
        headers.set("Authorization", `Bearer ${this.accessToken}`);
        res = await fetch(url, { ...options, headers });
      }

      return res;
    },

    async logout() {
      await fetch("http://localhost:8000/auth/logout/", {
        method: "POST",
        credentials: "include",
      });

      this.user = null;
      this.accessToken = "";
      this.refreshToken = "";
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },

    isAuthenticated() {
      return this.user !== null;
    },
  },
});
