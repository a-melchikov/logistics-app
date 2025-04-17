const API_URL = "http://localhost:8000";

export async function getAllVehicles(params: Record<string, string>) {
  const searchParams = new URLSearchParams(params).toString();

  const res = await fetch(`${API_URL}/vehicles/?${searchParams}`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка загрузки машин");
  return res.json();
}

export async function getVehicleById(vehicleId: number) {
  const res = await fetch(`${API_URL}/vehicles/${vehicleId}`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка загрузки машины");
  return res.json();
}

export async function createVehicle(vehicle: {
  driver_name: string;
  vehicle_type: string;
  license_plate: string;
}) {
  const res = await fetch(`${API_URL}/vehicles/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(vehicle),
  });
  if (!res.ok) throw new Error("Ошибка создания машины");
  return res.json();
}

export async function deleteVehicle(vehicleId: number) {
  const res = await fetch(`${API_URL}/vehicles/${vehicleId}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка удаления машины");
}

export async function getVehicleOrders(vehicleId: number) {
  const res = await fetch(`${API_URL}/vehicles/${vehicleId}/orders`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Ошибка загрузки истории заказов");
  return res.json();
}
