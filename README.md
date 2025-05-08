# 🚀 PhotoHub Service: Обработка изображений

![Django](https://img.shields.io/badge/Django-5.2-green)
![Celery](https://img.shields.io/badge/Celery-5.5-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-purple)
![Docker](https://img.shields.io/badge/Docker-25.0-cyan)

**Сервис для обработки изображений**

## 🌟 Особенности

- **Асинхронная обработка** через Celery с Redis в качестве брокера
- **REST API** с документацией Swagger/OpenAPI
- Готовый **Docker-стек** (Django + PostgreSQL + Redis + Celery)
- Статистика выполнения задач в реальном времени с помощью WebSocket

## 🛠 Технологии

| Компонент       | Технологии                  |
|-----------------|-----------------------------|
| Бэкенд         | Django 5.2, DRF, Celery 5.5 |
| База данных    | PostgreSQL 17               |
| Кеширование    | Redis 7                     |
| Инфраструктура | Docker, Daphne              |
| Документация   | Swagger/OpenAPI 3.0         |

## 🚀 Быстрый старт
```bash
# Клонировать репозиторий
git clone https://github.com/Valievx/photohub-service-test.git
cd photohub-service-test

# Запустить сервисы
docker compose up -d --build

# После запуска:
# - API: http://localhost:8000
# - Админка: http://localhost:8000/admin