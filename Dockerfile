# »спользуем базовый образ Python
FROM python 

# ”станавливаем переменную среды дл€ Python
ENV PYTHONUNBUFFERED 1

# ”станавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client

# —оздаем директорию дл€ приложени€ внутри контейнера
RUN mkdir /code
WORKDIR /code

#  опируем зависимости проекта и устанавливаем их
COPY requirements.txt /code/
RUN pip install -r requirements.txt

#  опируем остальные файлы проекта
COPY . /code/

# ќткрываем порт, который будет прослушивать ваше приложение
EXPOSE 8080

# «апускаем ваше приложение при старте контейнера
CMD ["gunicorn", "--access-logfile", "-", "--workers", "3", "--bind", "0.0.0.0:8080", "star_burger.wsgi:application"]
