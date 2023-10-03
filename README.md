
#  hackathon-lenta-backend

### Для запуска бэкенда проекта в контейнерах на локальной машине должен быть установлен Docker.

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
 - Собрать статику Django `docker compose exec backend python manage.py collectstatic`
 - скопировать статику `docker compose exec backend cp -r collected_static/. ../backend_static/static/`
 - сделать миграции в бд: `docker compose exec backend python manage.py makemigrations`
- применить миграции: `docker compose exec backend python manage.py migrate`
- для доступа к админке создать суперпользователя: `docker compose exec backend python manage.py createsuperuser` (под Windows команда может быть такой: `winpty docker compose exec backend python manage.py createsuperuser`
- админка доступна на http://127.0.0.1:8000/admin/

### Загрузка исходных данных, которые нам предоставили в базу:

- Скопировать файлы `st_df.csv, sales_submission.csv, sales_df_train.csv, pr_df.csv`   которые предоставили организаторы в директорию `/backend/initial_data`
-  в терминале перейти в директорию с проектом:  `cd <путь к проекту>/hackathon-lenta` . Все команды выполняются из этой директории
- Загрузка товарной иерархии и данных о ТЦ: `docker compose exec backend python manage.py load_data`
- Загрузка данных о продажах за год. **Т.к. в данных о продажах более 800 тыс. строк, загрузка занимает длительное время.** Например на машине с Ryzen  3 1200 и 16 Гб оперативки - около 1 часа 10 минут. Команда:  `docker compose exec backend python manage.py load_sales_data`
- Загрузка данных с прогнозом: `docker compose exec backend python manage.py load_forecast_data`

### В дальнейшем можно запускать проект командой `docker compose stop && docker compose up --build`
