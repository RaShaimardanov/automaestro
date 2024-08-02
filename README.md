 # 🤖 Bot AutoMaestro <img src="logo_circle_readme_1.jpg" align="right" />
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logoColor=white&logo=fastapi) ![Aiogram](https://img.shields.io/badge/Aiogram-005571?style=for-the-badge&logoColor=white&logo=bitrise&color=12497F) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-005571?style=for-the-badge&logo=sqlalchemy&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logoColor=white&logo=postgresql)
## 📝 Навигация
- [О проекте](#thinking-о-проекте)
- [Архитектура](#hamburger-архитектура-проекта)
- [Инструкция по запуску](#rocket-инструкция-по-запуску)
    -  [Виртуальное окружение](#настройка-окружения)
    -  [Настройка докера, docker-compose](#settings-docker-docker-compose)
    -  [Запуск приложения](#запуск)
- [Автор](#writing_hand-автор)

## :thinking: О проекте
Проект сделан для проведения исследования которое поможет выявить процент пользователей, заинтересованных в новых функциях мобильного приложения в автобизнесе. 

**Функционал администратора:**
- добавление нового опроса с вопросами и вариантов ответов
- редактирование и удаление опроса, вопросов и вариантов ответов
- просмотр списка пользователей и гос.номеров автомобилей
- просмотр списка сотрудников

**Функционал пользователя:**
- регистрация/изменение гос.номера автомобиля
- прохождение опроса
- просмотр статуса автомобиля
- получение визитки мастера-консультанта
- получение уведомления о готовности автомобиля из сервиса
- получение сообщения с просьбой оценить качество обслуживания
- отправка отзыва о качестве обслуживания

**Функционал мастера-консультанта:**
- регистрация/изменение контактных данных
- получение QR-кода с помощью которого клиенты могут появляться в спике "Автомобили"
- изменение статуса автомобиля
- отправка уведомлений клиентам о готовности

## :hamburger: Архитектура проекта
<details>
<summary>Развернуть</summary>

```
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── 1072eee61acc_first_migration.py
├── alembic.ini
├── app
│   ├── bot
│   │   ├── bot.py
│   │   ├── dp.py
│   │   ├── handlers
│   │   │   └── admin.py
│   │   ├── keyboards
│   │   │   └── inline
│   │   │       ├── base.py
│   │   │       ├── employee.py
│   │   │       ├── __init__.py
│   │   │       ├── poll.py
│   │   │       └── user.py
│   │   ├── middlewares
│   │   │   ├── chat_type.py
│   │   │   ├── database.py
│   │   │   └── lang.py
│   │   ├── scenes
│   │   │   ├── employee
│   │   │   │   ├── main_menu.py
│   │   │   │   ├── profile.py
│   │   │   │   ├── register.py
│   │   │   │   └── work.py
│   │   │   ├── mixins.py
│   │   │   ├── poll.py
│   │   │   ├── start.py
│   │   │   └── user
│   │   │       ├── estimations.py
│   │   │       ├── main_menu.py
│   │   │       ├── notifications.py
│   │   │       ├── profile.py
│   │   │       ├── register.py
│   │   │       └── send_vcard.py
│   │   └── utils
│   │       ├── callback_data.py
│   │       └── enums.py
│   ├── core
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── logger.py
│   │   └── paths.py
│   ├── database
│   │   ├── models
│   │   │   ├── base.py
│   │   │   ├── car.py
│   │   │   ├── mixins.py
│   │   │   ├── poll.py
│   │   │   ├── user.py
│   │   │   └── visit.py
│   │   ├── repo
│   │   │   ├── base.py
│   │   │   ├── car.py
│   │   │   ├── employee.py
│   │   │   ├── poll.py
│   │   │   ├── requests.py
│   │   │   ├── user.py
│   │   │   └── visit.py
│   │   └── setup.py
│   ├── __main__.py
│   ├── resources
│   │   ├── data
│   │   │   ├── images
│   │   │   ├── qrcodes
│   │   │   │   └── logo.jpg
│   │   │   └── voices
│   │   └── locales
│   │       └── ru.ftl
│   ├── services
│   │   ├── fluent.py
│   │   └── tasks
│   │       ├── apps.py
│   │       └── messages.py
│   ├── utils
│   │   ├── enums.py
│   │   ├── gen_qrcode.py
│   │   ├── send_message.py
│   │   └── speech_to_text.py
│   └── web
│       ├── api
│       │   ├── endpoints
│       │   │   └──  admin
│       │   │       ├── main.py
│       │   │       └── poll.py
│       │   ├── routers.py
│       │   ├── utils.py
│       │    validators.py
│       ├── app.py
│       ├── middlewares
│       │   └── telegram.py
│       └── templates
│           ├── admin
│           │   ├── base.html
│           │   ├── employees.html
│           │   ├── index.html
│           │   ├── poll
│           │   │   ├── add.html
│           │   │   ├── detail.html
│           │   │   ├── list.html
│           │   │   └── update.html
│           │   ├── question
│           │   │   ├── add.html
│           │   │   ├── detail.html
│           │   │   ├── list.html
│           │   │   ├── options.html
│           │   │   └── update.html
│           │   └── users.html
│           ├── index.html
│           └── static
│               ├── context.js
│               ├── images
│               │   └── logo_shadow.jpg
│               └── style.css
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

</details>

## :rocket: Инструкция по запуску
#### 1. Клонирование проекта
```
git clone https://github.com/RaShaimardanov/automaestro.git
```

#### 2. Настройка окружения 
```
BOT_TOKEN=123456:QWERTY
BOT_USERNAME=example_bot

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

PROJECT_NAME=Project Name
WEB_APP_URL=https://example.ru/admin
ADMINS_IDS=[11111111, 22222222]
```
> [Полный пример переменных окружения](.env.example).
#### 3. Локальный запуск
```
alembic upgrade head
```
```
poetry run python -m app
```
#### 4. Запуск на сервере
```
docker compose up
```

## :writing_hand: Автор
**&#169;[Расим Шаймарданов]**
