FastAPI Task Manager API для управления задачами с авторизацией и интеграцией в Docker-окружение.

Стек:
Язык: Python 3.12
Фреймворк: FastAPI
База данных: PostgreSQL
ORM: SQLAlchemy 2.0 (Async) + Alembic
Безопасность: JWT (JSON Web Tokens), Passlib (Bcrypt)
Контейнеризация: Docker + Docker Compose
Менеджер зависимостей: Poetry

Установка и запуск:
1. Клонировние репозитория
git clone https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПО.git

2. Настройка окружения
Создать файл .env в корне проекта на основе примера .env.example
Заполнить переменные: DATABASE_URL, SECRET_KEY, ALGORITHM.
SECRET_KEY можно сгенерировать командой python -c "import secrets; print(secrets.token_hex(32))"

3. Запуск через Docker
Команда ниже поднимет базу данных, применит миграции и запустит приложение:
docker-compose up --build
Приложение будет доступно по адресу: http://localhost:8000

Документация API:
После запуска доступна интерактивная документация:
Swagger UI: http://localhost:8000/docs — для тестирования эндпоинтов.
Redoc: http://localhost:8000/redoc 

Структура проекта
├── app/
│   ├── core/           # Конфигурация, безопасность (JWT, хэширование)
│   ├── database.py     # SQLAlchemy модели базы данных
│   ├── task.py         # модель базы данных
│   ├── user.py         # модель базы данных
│   ├── schemas.py      # Pydantic модели (валидация данных)
│   ├── auth.py         # Роутеры для авторизации и задач
│   └── main.py         # Инициализация FastAPI приложения
├── alembic/            # История миграций базы данных
├── docker-compose.yml  # Описание сервисов (app, db)
├── Dockerfile          # Сборка образа приложения
└──  pyproject.toml      # Зависимости Poetry

Основные эндпоинты:
POST/auth/register Регистрация нового пользователя
POST/auth/login Получение JWT-токена
GET/auth/me Получение данных о текущем пользователе
POST/auth/createtask Создание новой задачи (требует Auth)
GET/auth/ Получение списка всех задач пользователя
