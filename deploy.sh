#!/bin/bash

# �������� ���������� ��������� �� ����� .env (���� �� ����������)
if [ -f .env ]; then
  source .env
fi

# ������� ��� �������� ��������� � Rollbar
send_to_rollbar() {
  local ACCESS_TOKEN="$ROLLBAR_TOKEN"
  local MESSAGE="$1"

  curl -X POST \
    -H "Content-Type: application/json" \
    -d "{\"access_token\": \"$ACCESS_TOKEN\", \"data\": {\"body\": {\"message\": {\"body\": \"$MESSAGE\"}}}}" \
    https://api.rollbar.com/api/1/item/
}

# �������� ������� ������ ������� Rollbar
if [ -z "$ROLLBAR_TOKEN" ]; then
  echo "Error: ROLLBAR_TOKEN is not set. Please set the environment variable."
  exit 1
fi

# ���������� ���� �����������
echo "Updating repository code..."
cd /opt/star-burger   
git pull origin master

# ��������� ��������� Python
echo "Installing Python libraries..."
pip install -r requirements.txt --assume-yes

# ����� ��������
echo "Applying database migrations..."
python manage.py migrate --noinput  # ���������� �������� ��� �������������� �����

# ���������� ������� Django
echo "Collecting Django static files..."
python manage.py collectstatic --noinput

# ������ � ������ ����������� � ������� Docker Compose
echo "Building and starting containers with Docker Compose..."
docker-compose pull
docker-compose up -d

# ����������� �� �������� ���������� ������
echo "Deployment completed successfully."

# � ������ ������, ���������� ���������� �������
set -e
# �������� ��������� � Rollbar
echo "Sending deployment message to Rollbar..."
send_to_rollbar "Deployment completed successfully."

# � ������ ������, �������� ��������� � Rollbar � ���������� ���������� �������
set -e
trap 'send_to_rollbar "Deployment failed."' ERR
