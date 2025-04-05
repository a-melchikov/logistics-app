-- Вставляем тестовых пользователей
INSERT INTO users (username, hashed_password, role)
VALUES
    ('admin1', 'hashed_password_1', 'ADMIN'::userrole),
    ('dispatcher1', 'hashed_password_2', 'DISPATCHER'::userrole),
    ('dispatcher2', 'hashed_password_3', 'DISPATCHER'::userrole)
ON CONFLICT (username) DO NOTHING;

-- Вставляем тестовые заказы
INSERT INTO orders (client_name, cost, order_date, status, created_by_id)
VALUES
    ('Client A', 5000, '2024-04-01 10:00:00', 'PENDING'::orderstatus, 2),
    ('Client B', 12000, '2024-03-28 15:30:00', 'IN_PROGRESS'::orderstatus, 2),
    ('Client C', 8000, '2024-03-20 09:45:00', 'COMPLETED'::orderstatus, 3)
ON CONFLICT DO NOTHING;

-- Вставляем тестовые машины
INSERT INTO vehicles (driver_name, vehicle_type, license_plate)
VALUES
    ('John Doe', 'TRUCK'::vehicletype, 'ABC-1234'),
    ('Jane Smith', 'VAN'::vehicletype, 'XYZ-5678'),
    ('Bob Johnson', 'CAR'::vehicletype, 'LMN-9101')
ON CONFLICT (license_plate) DO NOTHING;

-- Вставляем тестовые путевые листы
INSERT INTO tripsheets (vehicle_id, order_id, start_time, end_time)
VALUES
    (1, 1, '2024-04-01 11:00:00', '2024-04-01 18:00:00'),
    (2, 2, '2024-03-28 16:00:00', '2024-03-28 21:00:00'),
    (3, 3, '2024-03-20 10:00:00', '2024-03-20 16:00:00')
ON CONFLICT DO NOTHING;
