# TenderBot :: AI + Parser + Telegram

Полноценный проект с AI-ассистентом (через VPN), парсером тендеров и Telegram-ботом. Сборка через `docker-compose`.

---

## 🚀 Сервисы

| Сервис         | Назначение                                | VPN  |
|----------------|--------------------------------------------|------|
| `api`          | FastAPI UI и эндпоинты                    | ❌   |
| `parser`       | Поиск тендеров на zakupki.gov.ru         | ❌   |
| `ai_worker`    | Запросы к Together / OpenAI / Mistral     | ✅   |
| `telegram_bot` | Общение с пользователем через Telegram    | ❌   |
| `vpn_gateway`  | OpenVPN-туннель                           | ✅   |

---

## ⚙️ Запуск проекта

```bash
git clone https://github.com/yourname/TenderBotProject.git
cd TenderBotProject

# Старт всех контейнеров
docker compose up --build
```

---

## 📁 Пример .env

Создай файл `.env` в корне проекта:

```env
# OpenAI или Together API
TOGETHER_API_KEY=your_api_key_here

# Telegram Bot Token
BOT_TOKEN=your_telegram_token_here

# Модель (например, Mistral)
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
```

---

## 🔌 Команды управления

| Действие                    | Команда                             |
|----------------------------|-------------------------------------|
| Запуск                     | `docker compose up --build`        |
| Остановка                  | `docker compose down`              |
| Перезапуск одного сервиса | `docker compose restart parser`    |
| Подключение к контейнеру   | `docker exec -it parser bash`      |

---

## 📄 Docker-файлы

- `Dockerfile.api` — FastAPI-интерфейс
- `Dockerfile.parser` — Парсер тендеров
- `Dockerfile.ai` — AI-инференс (через VPN)
- `Dockerfile.bot` — Telegram бот
- `Dockerfile` — VPN (OpenVPN-конфиг)

---

## 📌 Порты по умолчанию

| Сервис      | Порт         |
|-------------|--------------|
| FastAPI     | `http://localhost:8000` |
| Parser API  | `http://localhost:9001` (если открыт) |

---

## 🧾 Логи

Логи хранятся в папке `logs/`:

- `app.log` — логи FastAPI и парсера
- `ai_worker.log` — логи запросов к AI
- `vpn_gateway.log` — VPN-подключение

Ротация логов пока не настроена, можно подключить `logrotate` или встроенную систему `logging.handlers` при необходимости.

---

## 🔁 Auto-Restart

Каждый контейнер настроен с:
```yaml
restart: always
```
Это значит, что контейнер будет перезапущен автоматически при падении или перезагрузке хоста.

---

## 🚀 Планы на расширение

- [ ] Расширить AI-помощника: понимание PDF/документов, чат-контекст
- [ ] Подключение модели через локальный Mistral/LLaMA
- [ ] Расширить парсеры: ETP, Контур, РТС-тендер, закупки Москвы
- [ ] UI-фильтры по региону, цене, дате
- [ ] Хранение тендеров в SQLite или PostgreSQL
- [ ] Фронт на React или Bootstrap с графиками
- [ ] Система уведомлений (email, Telegram)

---

## 🔒 Безопасность
- API-ключи не коммить! Используй `.env`
- Telegram token и Together API должны быть скрыты

---

## 🧠 Авторизация VPN (если нужно)
Файлы конфигурации для OpenVPN положи в:
```
vpn_gateway/config/
```

---

## 👨‍💻 Автор
Разработка: [Твой Никнейм или GitHub](https://github.com/yourname)

