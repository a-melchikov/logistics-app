const API_URL = "http://localhost:8000";

// Получаем токен из localStorage (или другого источника)
function getAuthToken(): string | null {
  return localStorage.getItem("access_token");
}

// Функция для создания заголовков с токеном
function getAuthHeaders(): HeadersInit {
  const token = getAuthToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function getAllOrders(filters = {}) {
  const params = new URLSearchParams(filters as any).toString();
  const response = await fetch(`${API_URL}/orders/?${params}`);
  if (!response.ok) {
    throw new Error("Ошибка при получении заказов");
  }
  return await response.json();
}

export async function getOrderById(orderId: number) {
  const res = await fetch(`${API_URL}/orders/${orderId}`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка загрузки заказа");
  return res.json();
}

export async function createOrder(order: {
  client_name: string;
  cost: number;
  date: string;
  status: string;
}) {
  const token = localStorage.getItem("access_token"); // Пример получения токена

  const res = await fetch(`${API_URL}/orders/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    credentials: "include",
    body: JSON.stringify(order),
  });

  if (!res.ok) throw new Error("Ошибка создания заказа");
  return res.json();
}

export async function deleteOrder(orderId: number) {
  const token = localStorage.getItem("access_token"); // Пример получения токена

  const res = await fetch(`${API_URL}/orders/${orderId}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
    credentials: "include",
  });

  if (!res.ok) throw new Error("Ошибка удаления заказа");
}