const API_URL = "http://localhost:8000";

export async function getAllOrders() {
  const res = await fetch(`${API_URL}/orders/`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка загрузки заказов");
  return res.json();
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
  const res = await fetch(`${API_URL}/orders/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(order),
  });
  if (!res.ok) throw new Error("Ошибка создания заказа");
  return res.json();
}

export async function deleteOrder(orderId: number) {
  const res = await fetch(`${API_URL}/orders/${orderId}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка удаления заказа");
}
