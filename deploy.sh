#!/bin/bash

# ���������� ���� �����������
echo "Updating repository code..."
cd /opt/star-burger
git pull origin master

# ��������� ��������� Python
echo "Installing Python libraries..."
pip install -r requirements.txt


# ���������� ������� Django
echo "Collecting Django static files..."
cd /opt/star-burger
python manage.py collectstatic --noinput

# ����� ��������
echo "Applying database migrations..."
python manage.py migrate

# ���������� �������� Systemd
echo "Restarting Systemd services..."
sudo systemctl restart star-burger.service

# ����������� �� �������� ���������� ������
echo "Deployment completed successfully."

# � ������ ������, ���������� ���������� �������
set -e
