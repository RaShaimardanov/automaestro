 # 🤖 Bot AutoMaestro <img src="https://github.com/user-attachments/assets/360c6c27-8ae2-4add-a3ed-b74b3b6d0f30" align="right" />
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
Проект представляет собой бота, разработанного для проведения опроса среди клиентов о возможных функциях мобильного приложения по уходу за автомобилем.

Бот поможет выявить процент заинтересованности клиентов в новых функциях приложения и собрать обратную связь для улучшения взаимодействия клиентов с отделом сервиса.

Концепция направлена на повышение лояльности клиентов, улучшение их осведомленности о состоянии автомобиля и стимулирование регулярного обслуживания. Основная цель концепции - предоставить владельцам автомобилей все необходимые инструменты для заботы о своём транспортном средстве и повысить их вовлечённость в процесс ухода за ним.

Бот имеет три уровня доступа: администратор, пользователь и мастер-консультант. Каждый уровень имеет свой набор функций:

**Функционал пользователя:**
- регистрация/изменение гос.номера автомобиля
- прохождение опроса
- просмотр статуса автомобиля
- получение визитки мастера-консультанта
- получение уведомления о готовности автомобиля из сервиса
- получение сообщения с просьбой оценить качество обслуживания
- возможность оставить отзыв о качестве обслуживания

**Функционал мастера-консультанта:**
- регистрация/изменение контактных данных
- получение QR-кода с помощью которого клиенты могут появляться в спике "Автомобили"
- изменение статуса автомобиля
- отправка уведомлений клиентам о готовности

**Функционал администратора:**
- добавление нового опроса с вопросами и вариантов ответов
- редактирование и удаление опроса, вопросов и вариантов ответов
- просмотр списка пользователей и гос.номеров автомобилей
- просмотр списка сотрудников

<details>
<summary>Демонстрация возможностей</summary>
 <video src='https://github.com/user-attachments/assets/590705c7-1d72-4d7d-9b44-1a6a17d22496'/></video>
  _______________
 <video src='https://github.com/user-attachments/assets/c92bb6ae-2b30-40b5-94c0-ea2323ad8bdd'/></video>
 ______________
 <video src='https://github.com/user-attachments/assets/a9f1c7ec-d120-4ea4-90bc-41e622cca5d5'/></video>
</details>

## :hamburger: Архитектура проекта
<details>
<summary>Развернуть</summary>

```
.
├── alembic
├── app
│   ├── bot               # файлы бота
│   │   ├── handlers      # хендлеры
│   │   ├── keyboards     # клавиатуры
│   │   ├── middlewares   # мидлвари
│   │   ├── scenes        # сцены
│   │   └── utils
│   ├── core              # файлы конфигурации
│   ├── database          # файлы для работы с БД
│   │   ├── models
│   │   └──  repo
│   ├── __main__.py       # файл запуска
│   ├── resources
│   │   ├── data          # загруженные файлы
│   │   └── locales       # файлы локализации
│   ├── services
│   │   ├── fluent.py
│   │   └── tasks         # celery
│   ├── utils
│   └── web               # файлы web app
│       ├── api           
│       ├── middlewares   # мидлвари
│       └── templates     # шаблоны
├── alembic.ini
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
poetry install
```
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
**[Расим Шаймарданов]**
