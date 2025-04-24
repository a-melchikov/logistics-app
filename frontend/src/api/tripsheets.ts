const API_URL = "http://localhost:8000";

interface Tripsheet {
  id: number;
  vehicle_id: number;
  order_id: number;
  start_time: string;
  end_time: string;
  vehicle: {
    license_plate: string;
    driver_name: string;
  };
  order: {
    client_name: string;
  };
}

export async function getAllTripsheets(): Promise<Tripsheet[]> {
  const res = await fetch(`${API_URL}/tripsheets/`, {
    credentials: "include",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || "Ошибка загрузки путевых листов");
  }

  return res.json();
}

export async function getTripsheetById(
  tripSheetId: number
): Promise<Tripsheet> {
  const res = await fetch(`${API_URL}/tripsheets/${tripSheetId}`, {
    credentials: "include",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || "Ошибка загрузки путевого листа");
  }

  return res.json();
}

export async function createTripsheet(tripsheet: {
  vehicle_id: number;
  order_id: number;
  start_time: string;
  end_time: string;
}): Promise<Tripsheet> {
  const res = await fetch(`${API_URL}/tripsheets/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(tripsheet),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || "Ошибка создания путевого листа");
  }

  return res.json();
}

export async function deleteTripsheet(tripSheetId: number): Promise<void> {
  const res = await fetch(`${API_URL}/tripsheets/${tripSheetId}`, {
    method: "DELETE",
    credentials: "include",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || "Ошибка удаления путевого листа");
  }
}

export async function getTripsheetsForVehicle(
  vehicleId: number
): Promise<Tripsheet[]> {
  const res = await fetch(`${API_URL}/tripsheets/vehicle/${vehicleId}`, {
    credentials: "include",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || "Ошибка загрузки путевых листов машины");
  }

  return res.json();
}
