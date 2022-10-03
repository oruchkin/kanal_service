Тестовое задание для Канал Сервис

Есть видео инструкция:
https://www.loom.com/share/656886af11ef4ce5bd40b1e55cb24642

---
google sheet:
https://docs.google.com/spreadsheets/d/1d2v2X1h3sU7N6sNnDiJyW0FpDkmmcxfxZWZlNj_6xVs/edit#gid=0
---

Как запустить:

**через Docker-compose:**
в папке infra выполнить комманду:

~ docker-compose up

проект соберется и запустится по адресу http://127.0.0.1

далее нужно сделать миграции для базы данных, выполняем комманду в другом терминале

~ docker exec -it infra_backend_1 python manage.py migrate

далее собираем статику для .css

~ docker exec -it infra_backend_1 python manage.py collectstatic

далее создаем админа для (настройки уведомлений через телеграм)

~ docker exec -it infra_backend_1 python manage.py createsuperuser

дальше нужно ввести данные админа, обычно для тестов это username: admin, password: admin

проект успешно запущен по адресу http://127.0.0.1

админка по адресу http://127.0.0.1/admin

---

Способ 2 запустить напрямую через virtual environment:

зайти в папку /backend/kanal и выполнить комманды (linux/macos) :

- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- если мы делаем не через докер то нужно в settings.py раскоментировать базу данных sqlite3, а postgres закоментировать (оно рядом с settings.py в папке components/database.py)
- python manage.py runserver 0.0.0.0:8000
- (здесь уже есть база данных sqlite3)
- в админке заходим http://127.0.0.1:8000/admin юзернейм "admin" password "admin"
- вносим себя в уведомления в телеграме

---

Чтобы получать уведомления на телеграм нужно сходить в этого [https://t.me/userinfobot](https://t.me/userinfobot) бота

Нажать /start он вернет Вам ваш id, например мой "id:299470913"

Этот id нужно ввести в админке >> [Админка](http://127.0.0.1:8000/admin)

если используется базу данных sqlite3 то доступ: user: "admin", password: "admin", если postgres то админа нужно создать (инструкция в readme.md)

Так же нужно нажать /start в бота который будет делать рассылку [https://t.me/oruchkin3_bot](https://t.me/oruchkin3_bot)

id который вы получили в первом боте нужно в админке, зайти в раздел "Telegram_notifications" >> ADD TELEGRAM_NOTIFICATION

Здесь в полях name добавить свое имя, в поле chat id добавить id который вам выдал бот >> нажать SAVE

Успех - теперь вы админ и будете получать уведомления

---

В папке где лежит settings.py ДОЛЖЕН находиться скрытый файл ".env" он есть на гитхабе, вот его содержимое (без него postgres не запустится)

DB_ENGINE=django.db.backends.postgresql

DB_NAME=postgres

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

DB_HOST=db

DB_PORT=5432

Такойже скрытый файл .env лежит в папке infra (рядом с docker-compose.yaml) нужно для того чтобы собрать базу postgres
