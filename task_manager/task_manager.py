import os
import time
from datetime import datetime as dt

import requests
from dotenv import load_dotenv

DEFAULT_START_TIME = '01:00'

START_TIMES = os.getenv("START_TIMES", DEFAULT_START_TIME).split(', ')

data_dir = '/shared'

load_dotenv()

BOT_NAME = os.getenv('BOT_NAME', '')
BOT_EMAIL = os.getenv('BOT_EMAIL', '')
BOT_PASS = os.getenv('BOT_PASS', '')


def get_bot_token():
    """Получает токен для бота."""
    token_url = 'http://backend:8000/api/v1/auth/token/login/'
    data = {
        "email": BOT_EMAIL,
        "password": BOT_PASS
    }
    print(f'{token_url}')
    print(data)
    token = requests.post(f'{token_url}', data=data).json()['auth_token']
    return token


def export_data_request(headers):
    """Посылает запрос для выгрузки продаж в файл."""
    data_to_file_url = 'http://backend:8000/api/v1/'
    command = 'data_to_file/'
    requests.get(f'{data_to_file_url}{command}', headers=headers)


# def simulation_forecast_request():
#     """Посылает команду для симуляции прогноза."""
#     simulation_url = 'http://ds_simulation:5000/'
#     command = 'start_simulation/'
#     print(f'{simulation_url}{command}')
#     response = requests.get(f'{simulation_url}{command}')
#     print(response.text)


def save_forecast_request(headers):
    """Посылает запрос для импорта прогноза в базу."""
    forecast_url = 'http://backend:8000/api/v1/forecast/'
    command = 'add_daily_forecast/'
    requests.get(f'{forecast_url}{command}', headers=headers)


def get_time_difference(reduced_time, deductible_time):
    """Возвращает время в секундах до следующего запуска, вычисляя
    разницу между текущим временем и временем следующего запуска."""

    # Преобразуем время в секунды
    reduced_seconds = (
        reduced_time.hour * 60 * 60
        + reduced_time.minute * 60
        + reduced_time.second
    )

    deductible_seconds = (
        deductible_time.hour * 60 * 60
        + deductible_time.minute * 60
        + deductible_time.second
    )

    time_difference = reduced_seconds - deductible_seconds
    return time_difference


def task_runner():
    """Запускает задачи."""
    token = get_bot_token()
    # Формируем заголовок для аутентификации бота
    headers = {'Authorization': f'Token {token}'}
    time.sleep(1)
    export_data_request(headers)
    time.sleep(1)
    # simulation_forecast_request()
    # time.sleep(1)
    save_forecast_request(headers)


def scheduler():
    """Запускает задачи по расписанию."""
    if not START_TIMES:
        start_times = DEFAULT_START_TIME
    else:
        start_times = START_TIMES
    # Запускаем выполнение задач по расписанию в бесконечном цикле
    while True:
        for start_time in start_times:  # поиск ближайшего времени запуска
            # текущее время
            current_time = dt.now().time()
            # время запуска из списка
            scheduled_time = dt.strptime(start_time, '%H:%M').time()
            if current_time <= scheduled_time:
                sleep_time = get_time_difference(scheduled_time, current_time)
                time.sleep(sleep_time)
                task_runner()
        current_time = dt.now().time()
        # время следующего запуска
        scheduled_time = dt.strptime(start_times[0], '%H:%M').time()
        # время ДО следующего запуска в секундах
        sleep_time = 24 * 60 * 60 - get_time_difference(
            current_time, scheduled_time
        )
        time.sleep(sleep_time)
        task_runner()


if __name__ == '__main__':
    scheduler()