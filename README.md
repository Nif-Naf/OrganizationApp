# 📦 REST API сервис справочник организаций.

## 📌 Описание

Приложение реализует асинхронный REST API сервис справочник организаций
и видов их деятельности с древовидной иерархией. Взаимодействие происходит через 
HTTP-запросы с использованием статического API-ключа. Все ответы отдаются в 
формате JSON.

---

## 🏗️ Стек технологий

- ⚡️ [FastAPI](https://fastapi.tiangolo.com/) — фреймворк для создания высокопроизводительных API
- 🧬 [SQLAlchemy](https://docs.sqlalchemy.org/) — ORM для работы с базой данных
- 📜 [Alembic](https://alembic.sqlalchemy.org/) — управление миграциями 
- 🔐 [Pydantic](https://docs.pydantic.dev/) — валидация и сериализация схем
- 🐳 [Docker](https://www.docker.com/) — контейнеризация
- 🧪 [Pytest](https://docs.pytest.org/) — тестирование

---

## 📂 Сущности

### 🏢 Организация (`Company`)
- Название: например, `ООО "Рога и Копыта"`
- Номера телефонов: один или несколько
- Здание: принадлежит одному зданию
- Виды деятельности: может относиться к нескольким

### 🏠 Здание (`Address`)
- Адрес: например, `г. Москва, ул. Ленина 1`
- Координаты: широта и долгота

### 🧩 Вид деятельности (`Activity`)
- Название
- Деревовидная структура видов деятельности (максимум 3 уровня вложенности)

---

## 🔧 Функционал
Все API требуют авторизации и она происходит с помощью статического токена, ф
который должен передаваться в заголовке: `x-api-key`.

- 🔎 Поиск организаций по названию
- 🔢 Получить организацию по ID
- 📍 Получить все организации по определенному адресу
- 🧩 Получить все организации по указанному виду деятельности
- 🗺️ Получить все организации, находящиеся в радиусе x км от переданной координаты

---

## 🧪 Тесты
Не требуют поднятия контейнера, работают с отдельной файловой базой.
Загружаются тестовые данные при старте через фикстуру.

Запуск: 
```bash
pytest
```

---

## 🚀 Запуск проекта
```bash
docker compose up --build
```

---

## ️️️🛠️ Команды для разработки
Black. Форматирование кода.
```bash
black --line-length=79 --target-version=py312 --skip-string-normalization --exclude="migrations|\.venv" .
```


️️️Isort. Запуск сортировки импортов.
```bash
isort --sp=.isort.cfg .
```

📌 Alembic. Создание новой миграции.
```bash
alembic revision --autogenerate -m "Add new migration"
```

📥 Alembic. Применение миграции.
```bash
alembic upgrade head
```

⬅️ Alembic. Откатить на одну миграцию назад.
```bash
alembic downgrade -1
```

⏪ Alembic. Откатить до определённой версии.
```bash
alembic downgrade <revision_id>
```

📦 Poetry. Добавить основную зависимость.
```bash
poetry add <package-name>
```

🧪 Добавить зависимость в группу dev.
```bash
poetry add --group dev <package-name>
```

❌ Poetry. Удалить зависимость.
```bash
poetry remove <package-name>
```

📄 Poetry. Обновить pyproject.toml и зависимости.
```bash
poetry update
```

🔍 Poetry. Проверить устаревшие зависимости.
```bash
poetry show --outdated
```

⚙️ Poetry. Установить зависимости из pyproject.toml.
```bash
poetry install
```

🔁 Docker. Собрать и запустить контейнеры.
```bash
docker compose up --build
```

⏹ Docker. Остановить контейнеры
```bash
docker compose down
```

📥 Docker. Подключиться внутрь контейнера.
```bash
docker exec -it <container_name> bash
```

📜 Docker. Просмотреть логи контейнера.
```bash
docker logs <container_name>
```

🔄 Docker. Следить за логами в реальном времени.
```bash
docker logs -f <container_name>
```

🔌 Docker. Перезапустить контейнер.
```bash
docker restart <container_name>
```

🧹 Docker. Удалить все остановленные контейнеры.
```bash
docker rm $(docker ps -qa)
```

🗑 Docker. Удалить все образы.
```bash
docker rmi $(docker images -q)
```

🌐 Docker. Показать все Docker-сети.
```bash
docker network ls
```

🧼 Docker. Удалить неиспользуемые Docker-сети.
```bash
docker network prune
```

📦 Docker. Показать все volumes.
```bash
docker volume ls
```

🧯 Docker. Удалить неиспользуемые volumes.
```bash
docker volume prune
```

🚮 Docker. Полная очистка: volumes, networks, images, containers.
```bash
docker system prune -a
```