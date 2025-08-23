# === 📦 Сборка и запуск ===

rebuild-api:
	docker compose build api && docker compose up -d api

rebuild-bot:
	docker compose build telegram_bot && docker compose up -d telegram_bot

rebuild-ai:
	docker compose build ai_worker && docker compose up -d ai_worker

rebuild-vpn:
	docker compose build vpn_gateway && docker compose up -d vpn_gateway

rebuild-watchdog:
	docker compose build watchdog && docker compose up -d watchdog

rebuild-all:
	docker compose build && docker compose up -d

# === 🔍 Логи ===

logs-api:
	docker compose logs -f api

logs-bot:
	docker compose logs -f telegram_bot

logs-ai:
	docker compose logs -f ai_worker

logs-vpn:
	docker compose logs -f vpn_gateway

logs-watchdog:
	docker compose logs -f watchdog

# === ♻️ Утилиты ===

restart:
	docker compose restart

down:
	docker compose down

ps:
	docker compose ps

# === 💡 Примеры команд для новичка ===
# make rebuild-api       — пересобрать только API
# make rebuild-all       — пересобрать все контейнеры
# make logs-ai           — смотреть лог ИИ
# make restart           — перезапуск всех сервисов
# make down              — остановить всё
rebuild-api:
	docker compose build api && docker compose up -d api

rebuild-bot:
	docker compose build telegram_bot && docker compose up -d telegram_bot

rebuild-all:
	docker compose build && docker compose up -d

logs-api:
	docker compose logs -f api

logs-bot:
	docker compose logs -f telegram_bot

restart:
	docker compose restart

rebuild-api:
	docker compose build api && docker compose up -d api

rebuild-bot:
	docker compose build telegram_bot && docker compose up -d telegram_bot

rebuild-all:
	docker compose build && docker compose up -d

logs-api:
	docker compose logs -f api

logs-bot:
	docker compose logs -f telegram_bot

restart:
	docker compose restart

# --- API ---
rebuild-api: ...
logs-api: ...

# --- Telegram Bot ---
rebuild-bot: ...
logs-bot: ...

# --- AI Worker ---
rebuild-ai: ...
logs-ai: ...

# --- VPN Gateway ---
rebuild-vpn: ...
logs-vpn: ...

# --- Общие ---
restart: ...
up-all: ...

# === 📦 Сборка и запуск ===

rebuild-api:
	docker compose build api && docker compose up -d api

rebuild-bot:
	docker compose build telegram_bot && docker compose up -d telegram_bot

rebuild-ai:
	docker compose build ai_worker && docker compose up -d ai_worker

rebuild-vpn:
	docker compose build vpn_gateway && docker compose up -d vpn_gateway

rebuild-watchdog:
	docker compose build watchdog && docker compose up -d watchdog

rebuild-all:
	docker compose build && docker compose up -d

# === 🔍 Логи ===

logs-api:
	docker compose logs -f api

logs-bot:
	docker compose logs -f telegram_bot

logs-ai:
	docker compose logs -f ai_worker

logs-vpn:
	docker compose logs -f vpn_gateway

logs-watchdog:
	docker compose logs -f watchdog

# === ♻️ Утилиты ===

restart:
	docker compose restart

down:
	docker compose down

ps:
	docker compose ps

# === 💡 Примеры команд для новичка ===
# make rebuild-api       — пересобрать только API
# make rebuild-all       — пересобрать все контейнеры
# make logs-ai           — смотреть лог ИИ
# make restart           — перезапуск всех сервисов
# make down              — остановить всё
