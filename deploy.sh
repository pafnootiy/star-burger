#!/bin/bash

# Загрузка переменных окружения из файла .env (если он существует)
if [ -f .env ]; then
  source .env
fi

# Функция для отправки сообщения в Rollbar
send_to_rollbar() {
  local ACCESS_TOKEN="$ROLLBAR_TOKEN"
  local MESSAGE="$1"

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{\"access_token\": \"$ACCESS_TOKEN\", \"data\": {\"body\": {\"message\": {\"body\": \"$MESSAGE\"}}}}" \
    https://api.rollbar.com/api/1/item/
}

# Проверка наличия токена доступа Rollbar
if [ -z "$ROLLBAR_TOKEN" ]; then
  echo "Error: ROLLBAR_TOKEN is not set. Please set the environment variable."
  exit 1
fi

# Обновление кода репозитория
echo "Updating repository code..."
cd /opt/star-burger   
git pull origin master

# Установка библиотек Python
echo "Installing Python libraries..."
pip install -r requirements.txt --assume-yes

# Накат миграций
echo "Applying database migrations..."
python manage.py migrate --noinput  # Применение миграций без интерактивного ввода

# Пересборка статики Django
echo "Collecting Django static files..."
python manage.py collectstatic --noinput

# Сборка и запуск контейнеров с помощью Docker Compose
echo "Building and starting containers with Docker Compose..."
docker-compose pull
docker-compose up -d

# Уведомление об успешном завершении деплоя
echo "Deployment completed successfully."

# В случае ошибки, завершение выполнения скрипта
set -e
# Отправка сообщения в Rollbar
echo "Sending deployment message to Rollbar..."
send_to_rollbar "Deployment completed successfully."

# В случае ошибки, отправка сообщения в Rollbar и завершение выполнения скрипта
set -e
trap 'send_to_rollbar "Deployment failed."' ERR
