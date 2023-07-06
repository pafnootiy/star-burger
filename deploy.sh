#!/bin/bash

# Обновление кода репозитория
echo "Updating repository code..."
cd /opt/star-burger
git pull origin master

# Установка библиотек Python
echo "Installing Python libraries..."
pip install -r requirements.txt


# Пересборка статики Django
echo "Collecting Django static files..."
cd /opt/star-burger
python manage.py collectstatic --noinput

# Накат миграций
echo "Applying database migrations..."
python manage.py migrate

# Перезапуск сервисов Systemd
echo "Restarting Systemd services..."
sudo systemctl restart star-burger.service

# Уведомление об успешном завершении деплоя
echo "Deployment completed successfully."

# В случае ошибки, завершение выполнения скрипта
set -e
