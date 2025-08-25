
# === 📦 TenderBot Makefile (расширенный) ===

# === 🚀 Основные команды управления ===

up:
	docker compose up -d --build

down:
	docker compose down

restart:
	docker compose restart

build:
	docker compose build

logs:
	docker compose logs -f --tail=100

# === 🔧 Сборка по сервисам ===

build-api:
	docker compose build api

build-bot:
	docker compose build telegram_bot

build-ai:
	docker compose build ai_worker

build-pars:
	docker compose build parsers

# === 📜 Логи по сервисам ===

logs-api:
	docker compose logs -f api

logs-bot:
	docker compose logs -f telegram_bot

logs-ai:
	docker compose logs -f ai_worker

logs-pars:
	docker compose logs -f parsers

# === ♻️ Только перезапуск без сборки ===

restart-api:
	docker compose restart api

restart-bot:
	docker compose restart telegram_bot

restart-ai:
	docker compose restart ai_worker

restart-pars:
	docker compose restart parsers

# === ⚡ Быстрая пересборка без кеша ===

quick-api:
	docker compose build --no-cache api && docker compose up -d api

quick-bot:
	docker compose build --no-cache telegram_bot && docker compose up -d telegram_bot

quick-ai:
	docker compose build --no-cache ai_worker && docker compose up -d ai_worker

quick-pars:
	docker compose build --no-cache parsers && docker compose up -d parsers

# === 🧪 Утилиты (по желанию можно добавить реализацию) ===

clean:
	docker system prune -f

shell-api:
	docker compose exec api bash

shell-bot:
	docker compose exec telegram_bot bash

shell-ai:
	docker compose exec ai_worker bash

shell-pars:
	docker compose exec parsers bash

# === ✅ TODO: можно добавить позже ===
# lint: black . && flake8 .
# format: black .
# test: pytest
