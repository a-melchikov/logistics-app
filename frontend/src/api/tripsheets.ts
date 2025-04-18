const API_URL = 'http://localhost:8000'

export async function getAllTripsheets() {
  const res = await fetch(`${API_URL}/tripsheets/`, {
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Ошибка загрузки путевых листов')
  return res.json()
}

export async function getTripsheetById(tripSheetId: number) {
  const res = await fetch(`${API_URL}/tripsheets/${tripSheetId}`, {
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Ошибка загрузки путевого листа')
  return res.json()
}

export async function createTripsheet(tripsheet: {
  vehicle_id: number
  date: string
  entries: {
    order_id: number
    hour: number
    duration: number
  }[]
}) {
  const res = await fetch(`${API_URL}/tripsheets/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(tripsheet),
  })
  if (!res.ok) throw new Error('Ошибка создания путевого листа')
  return res.json()
}

export async function deleteTripsheet(tripSheetId: number) {
  const res = await fetch(`${API_URL}/tripsheets/${tripSheetId}`, {
    method: 'DELETE',
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Ошибка удаления путевого листа')
}

export async function getTripsheetsForVehicle(vehicleId: number) {
  const res = await fetch(`${API_URL}/tripsheets/vehicle/${vehicleId}`, {
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Ошибка загрузки путевых листов машины')
  return res.json()
}
