## Что нужно сделать
- Создавать админа перед запуском приложения используя lifespan, брать данные пароля и логина из env ADMIN_PASSWORD, ADMIN_LOGIN

## Запуск сервера

```bash
uv run uvicorn app.main:app --reload
```
