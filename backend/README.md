## Что нужно сделать

- Создавать админа перед запуском приложения используя lifespan, брать данные пароля и логина из env ADMIN_PASSWORD, ADMIN_LOGIN
- Сделать более грамотную проверку номера гос. номера, добавить еще типы транспортных средств (мотоцикл) и делать проверку
- Переписать создание пользователей чтобы хешировался пароль
- Сделать так чтобы регистрацию можно было выполнять только с токен
- Если заказ выполнен в дополнительной информации написать, что он выполнен

## Запуск сервера

```bash
uv run uvicorn main:app --reload
```

## Проверка с помощью curl

Авторизация пользователя:

```bash
curl -X POST "http://localhost:8000/auth/login/" -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'
```

Получение информации о текущем пользователе:

```bash
curl -X GET "http://localhost:8000/auth/me/" -H "Authorization: Bearer $ACCESS_TOKEN"
```

Получение всех пользователей (только для администратора):

```bash
curl -X GET "http://localhost:8000/auth/all_users/" -H "Authorization: Bearer $ACCESS_TOKEN"
```

Выход из системы:

```bash
curl -X POST "http://localhost:8000/auth/logout/" -H "Authorization: Bearer $ACCESS_TOKEN"
```

Обновление токена доступа (с использованием refresh токена):

```bash
curl -X POST "http://localhost:8000/auth/refresh/" -H "Authorization: Bearer $REFRESH_TOKEN"
```
