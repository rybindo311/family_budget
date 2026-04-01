#!/bin/sh
set -e  # Останавливает выполнение при любой ошибке

echo "========================================"
echo "Starting application..."
echo "========================================"

# Проверка наличия poetry
if ! command -v poetry >/dev/null 2>&1; then
    echo "❌ Poetry not found!"
    exit 1
fi

# Проверка наличия alembic
if ! poetry run which alembic >/dev/null 2>&1; then
    echo "❌ Alembic not found in poetry environment!"
    exit 1
fi

export PYTHONPATH="/app/src:${PYTHONPATH}"

# Настройка режима
if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "local" ]; then
    echo "🔧 Development mode detected"
    RELOAD_FLAG="--reload"
elif [ "$ENVIRONMENT" = "test" ]; then
    echo "🧪 Testing mode detected"
    RELOAD_FLAG=""
else
    echo "🚀 Production mode detected"
    RELOAD_FLAG=""
fi

# Применяем миграции
echo "🔄 Applying database migrations..."
if poetry run alembic upgrade head; then
    echo "✅ Migrations applied successfully"
else
    echo "❌ Migrations failed!"
    exit 1
fi

if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "local" ]; then
    echo "🌱 Seeding test data..."
    if poetry run python -m src.seed; then
        echo "✅ Seeding completed"
    else
        echo "⚠️  Seeding failed, continuing anyway..."
    fi
fi

echo ""
echo "🚀 Starting uvicorn server..."

echo ""
echo "🚀 Starting uvicorn server..."
echo "   Host: 0.0.0.0"
echo "   Port: ${PORT:-8000}"
echo "   Reload: ${RELOAD_FLAG:-off}"

exec poetry run uvicorn src.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    $RELOAD_FLAG
