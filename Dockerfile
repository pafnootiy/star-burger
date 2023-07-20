# ���������� ������� ����� Python
FROM python 

# ������������� ���������� ����� ��� Python
ENV PYTHONUNBUFFERED 1

# ������������� ��������� �����������
RUN apt-get update && apt-get install -y \
    postgresql-client

# ������� ���������� ��� ���������� ������ ����������
RUN mkdir /code
WORKDIR /code

# �������� ����������� ������� � ������������� ��
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# �������� ��������� ����� �������
COPY . /code/

# ��������� ����, ������� ����� ������������ ���� ����������
EXPOSE 8080

# ��������� ���� ���������� ��� ������ ����������
CMD ["gunicorn", "--access-logfile", "-", "--workers", "3", "--bind", "0.0.0.0:8080", "star_burger.wsgi:application"]
