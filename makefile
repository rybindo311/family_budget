# ============================================
# Docker Compose Management Makefile
# ============================================

# Переменные
DC = docker-compose
DC_DEV = -f docker-compose.yaml -f docker-compose.dev.yaml
DC_TEST = -f docker-compose.yaml -f docker-compose.test.yaml
DC_PROD = -f docker-compose.yaml

# Цели по умолчанию (запускается при просто make)
.DEFAULT_GOAL = help

# ============================================
# Основные команды
# ============================================

# Запуск в режиме разработки 🚀
up-dev:
	$(DC) $(DC_DEV) up -d
	@echo "✅ Development environment started"

# Запуск в режиме разработки с логами 📊
up-dev-logs:
	$(DC) $(DC_DEV) up

# Запуск тестового окружения 🧪
up-test:
	$(DC) $(DC_TEST) up -d
	@echo "✅ Test environment started"

# Запуск продакшн окружения 🌐
up-prod:
	$(DC) $(DC_PROD) up -d
	@echo "✅ Production environment started"

# ============================================
# Управление контейнерами
# ============================================

# Остановка всех окружений 🛑
down:
	$(DC) $(DC_DEV) down
	$(DC) $(DC_TEST) down
	$(DC) $(DC_PROD) down
	@echo "✅ All environments stopped"

# Остановка конкретного окружения
down-dev:
	$(DC) $(DC_DEV) down

down-test:
	$(DC) $(DC_TEST) down

down-prod:
	$(DC) $(DC_PROD) down

# Перезапуск
restart-dev: down-dev up-dev
	@echo "🔄 Development environment restarted"

# ============================================
# Логи и отладка
# ============================================

# Просмотр логов
logs-dev:
	$(DC) $(DC_DEV) logs -f

logs-test:
	$(DC) $(DC_TEST) logs -f

logs-prod:
	$(DC) $(DC_PROD) logs -f

# Логи конкретного сервиса
logs-dev-service:
	@read -p "Enter service name: " service; \
	$(DC) $(DC_DEV) logs -f $$service

# ============================================
# Управление сервисами
# ============================================

# Запуск конкретного сервиса
start-service-dev:
	@read -p "Enter service name: " service; \
	$(DC) $(DC_DEV) up -d $$service

# Остановка конкретного сервиса
stop-service-dev:
	@read -p "Enter service name: " service; \
	$(DC) $(DC_DEV) stop $$service

# Пересборка сервиса
rebuild-service-dev:
	@read -p "Enter service name: " service; \
	$(DC) $(DC_DEV) up -d --build $$service

# ============================================
# Работа с образами и volumes
# ============================================

# Полная пересборка
rebuild-dev:
	$(DC) $(DC_DEV) down -v
	$(DC) $(DC_DEV) build --no-cache
	$(DC) $(DC_DEV) up -d
	@echo "🔨 Development environment rebuilt"

# Очистка (удаление контейнеров, образов, volumes)
clean:
	$(DC) $(DC_DEV) down -v --rmi all
	$(DC) $(DC_TEST) down -v --rmi all
	$(DC) $(DC_PROD) down -v --rmi all
	docker system prune -f
	@echo "🧹 Cleanup completed"

# ============================================
# Полезные команды
# ============================================

# Статус контейнеров
ps:
	@echo "📊 Development:"
	$(DC) $(DC_DEV) ps
	@echo "\n📊 Test:"
	$(DC) $(DC_TEST) ps
	@echo "\n📊 Production:"
	$(DC) $(DC_PROD) ps

# Зайти в контейнер
exec-dev:
	@read -p "Enter service name: " service; \
	$(DC) $(DC_DEV) exec $$service sh

# Выполнить команду в контейнере
run-dev:
	@read -p "Enter service name: " service; \
	read -p "Enter command: " cmd; \
	$(DC) $(DC_DEV) exec $$service $$cmd

# Бэкап данных (пример для PostgreSQL)
backup-db:
	@read -p "Enter database service name: " db_service; \
	read -p "Enter database name: " db_name; \
	$(DC) $(DC_DEV) exec $$db_service pg_dump -U postgres $$db_name > backup_$$(date +%Y%m%d_%H%M%S).sql

# ============================================
# Справка
# ============================================

help:
	@echo "📋 Available commands:"
	@echo ""
	@echo "🚀 STARTUP:"
	@echo "  make up-dev        - Start development environment"
	@echo "  make up-dev-logs   - Start development environment with logs"
	@echo "  make up-test       - Start test environment"
	@echo "  make up-prod       - Start production environment"
	@echo ""
	@echo "🛑 STOP:"
	@echo "  make down          - Stop all environments"
	@echo "  make down-dev      - Stop development only"
	@echo "  make restart-dev   - Restart development"
	@echo ""
	@echo "📊 INFO:"
	@echo "  make ps            - Show container status"
	@echo "  make logs-dev      - Show development logs"
	@echo "  make help          - Show this help"
	@echo ""
	@echo "🛠️ DEVELOPMENT:"
	@echo "  make exec-dev      - Enter a container"
	@echo "  make rebuild-dev   - Full rebuild"
	@echo "  make clean         - Remove everything"