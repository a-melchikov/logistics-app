const API_URL = "http://localhost:8000";

export async function login(username: string, password: string) {
  const response = await fetch(`${API_URL}/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) throw new Error("Ошибка авторизации");
  return response.json();
}

export async function getMe() {
  const response = await fetch(`${API_URL}/auth/me/`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  });

  if (!response.ok)
    throw new Error("Ошибка при получении информации о пользователе");
  return response.json();
}
