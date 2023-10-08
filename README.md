
# Проект "Прогнозирование спроса на товары Ленты"

## Описание проекта

Цель проекта - создание предсказательной модели и интерфейса для прогнозирования спроса на товары заказчика собственного производства ООО "Лента". 

## Задачи проекта

1. Сбор и анализ данных о продажах товаров Ленты.
2. Разработка предсказательной модели на основе анализа данных.
3. Создание интерфейса для ввода данных и получения прогнозов.

## Технологии

Для реализации проекта используются следующие технологии:

### Backend
- Python 3.11
- Django 4.2
- Django REST framework 3.14
- Gunicorn 21.2
- Swagger
- Docker

### Frontend
- JavaScript
- HTML/CSS
- React
- Redux
- Vite
- AntDesign

### DS
- Pandas 1.5
- Numpy 1.23
- Flask 2.2
- Catboost 1.2
- Holidays 0.34
- Prophet 1.1
- Lightgbm 4.0

### Design
- Figma
- ChartJS
- AntDesign

## Как использовать

 Краткая инструкция по запуску:
 - скачать проект на локальную машину `git clone git@github.com:weekend-warriors-team/hackathon-lenta.git`
 - в директории /hackathon-lenta создать файл `.env` с таким содержанием:
   ```
      POSTGRES_USER=django_user
      POSTGRES_PASSWORD=yourpassword
      POSTGRES_DB=django
      DB_HOST=db
      DB_PORT=5432
   ```

 - в терминале перейти в директорию с проектом:  `cd <путь к проекту>/hackathon-lenta`
 - в директории проекта `/hackathon-lenta` выполнить команду `docker compose stop && docker compose up --build`
 - дождаться сборки и запуска контейнеров с проектом
 - собрать статику Django `docker compose exec backend python manage.py collectstatic`
 - скопировать статику `docker compose exec backend cp -r collected_static/. ../backend_static/static/`
 - сделать миграции в бд: `docker compose exec backend python manage.py makemigrations`
- применить миграции: `docker compose exec backend python manage.py migrate`
- для доступа к админке создать суперпользователя: `docker compose exec backend python manage.py createsuperuser` (под Windows команда может быть такой: `winpty docker compose exec backend python manage.py createsuperuser`)
- для работы с API проекта, необходимо получить токен(достать токен можно как через POSTMAN так и через SWAGGER) по адресу: `http://127.0.0.1:8000/api/v1/auth/token/login/`
POST запрос вида:
```json
{
    "email": "user@user.ru",
    "password": "mypassword"
}
```
Ответ:
```json
{
    "auth_token": "c49f6ebb3d5a55gfjkgfdjkgdfjkgjkdgj3c9"
}
```
- далее в postman в поле Headers, мы вносим наш токен - Authorization: Token c49f6ebb3d5a55gfjkgfdjkgdfjkgjkdgj3c9
- API документация доступна по адресу http://127.0.0.1:8000/swagger/
- админ-панель доступна по адресу http://127.0.0.1:8000/admin/

### Загрузка данных в базу:

- Скопировать файлы `st_df.csv, sales_submission.csv, sales_df_train.csv, pr_df.csv` в директорию       `/backend/initial_data`
-  в терминале перейти в директорию с проектом:  `cd <путь к проекту>/hackathon-lenta` . Все команды выполняются из этой директории.
- Загрузка товарной иерархии и данных о ТЦ: `docker compose exec backend python manage.py load_data`
- Загрузка данных о продажах за год: `docker compose exec backend python manage.py load_sales_data`
- Загрузка данных с прогнозом: `docker compose exec backend python manage.py load_forecast_data`

### Запуск проекта производится командой `docker compose stop && docker compose up --build`

## Примеры API эндпоинтов:
* ```/api/v1/``` Get-запрос - основное api
 ``` json
{
    "users": "http://127.0.0.1:8000/api/v1/users/",
    "shops": "http://127.0.0.1:8000/api/v1/shops/",
    "products": "http://127.0.0.1:8000/api/v1/products/",
    "sales": "http://127.0.0.1:8000/api/v1/sales/",
    "forecast": "http://127.0.0.1:8000/api/v1/forecast/"
}
```
* ```/api/v1/users/``` Post-запрос - регистрация пользователя. Get-запрос – получение списка пользователей. 
``` json
[
    {
        "email": "hutjicsgo@gmail.com",
        "id": 1,
        "username": "hutji",
        "first_name": "",
        "last_name": ""
    }
]
```
* ```/api/v1/products/```  Get-запрос – получение списка продуктов/товаров.
``` json
    {
        "sku": "002c3a40ac50dc870f1ff386f11f5bae",
        "group": "6512bd43d9caa6e02c990b0a82652dca",
        "category": "c9f95a0a5af052bffce5c89917335f67",
        "subcategory": "507c9dcd6538b05090d22c4b73c535a7",
        "uom": 1
    },
```
* ```/api/v1/shops/```  Get-запрос – получение списка магазинов.
``` json
{
        "store": "084a8a9aa8cced9175bd07bc44998e75",
        "city": "3202111cf90e7c816a472aaceb72b0df",
        "division": "32586311f16876abf92901085bd87b99",
        "type_format": 4,
        "loc": 3,
        "size": 19,
        "is_active": true
    },
```
* ```/api/v1/sales/```  Get-запрос – получение списка продаж за год.
* ```/api/v1/forecast/```  Get-запрос – получение списка прогнозируемых товаров.

## Команда разработки:

### Дизайнеры: 
- Бекжанов Арсен
  
- Ананьева Наталия Андреевна
  
- Орлова Татьяна Александровна

### DS: 
- Лаговский Дмитрий Владимирович
  
- Завесова Анна Александровна
  
- Евдакова Екатерина Геннадьевна

### Backend-разработчики: 
- Лашков Павел Александрович
  
- Кочетов Данил Владимирович

### Frontend-разработчики: 
- Фаталиев Джамал Алиханович

### Менеджер проекта 
- Котов Артём Алексеевич

## Лицензия

Проект распространяется под лицензией MIT. Подробнее о лицензии можно узнать в файле LICENSE.

# Lenta x Yandex.Practicum 2023
