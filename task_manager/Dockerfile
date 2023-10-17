FROM python:3.11.4

# Устанавливаем переменную среды TZ
ENV TZ=Europe/Moscow

RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["python", "task_manager.py"]