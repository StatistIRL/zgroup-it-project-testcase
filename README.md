# zGroup-IT тестовое задание

## Основная задача
Реализовать нижеописанный функционал, если кажется, что вы можете дополнить это тестовое другим функционалом, то будем рады увидеть ваши творческие стороны.

Возможные стеки:
1. Django DRF + PSQL
2. **FastAPI + PSQL** (выбранный) 

Endpoints:
1. /upload/ - принимает файл и имя претендента, сохраняет их
2. /delete/<>/ - удаляет резюме из базы и удаляет файл
3. /list/ - выводит пагинированный список резюме с абсолютным путем до файла резюме и именем

## EXTRA задача
Реализовать систему рейтинга для резюме проставляемого пользователем.

## Плюс балл факторы:
1. Документация написанная академическим языком
2. Чистота кода, использование максимума возможного в конкретном кейсе, функционала используемого стека
3. Заполненный и переданный APIDOG по тестовому проекту

## Развёртывание локально
1. При помощи `pdm` или любого другого пакетного менеджера накатываем зависимости и создаем виртуальное окружение
2. Создаем файл `.env` по подобию `.env.example` и заполняем поля `DATABASE_USERNAME`, `DATABASE_PASSWORD` и `DATABASE_NAME`
3. Поднимаем контейнеры `PostgreSQL` и `MinIO`
   ```bash
   docker-compose up -d
   ```
4. Накатываем мигарции базы данных через `alembic`
   ```bash
   alembic upgrade head
   ```
5. В консоли [MinIO](http://localhost:9001) сначала создаем бакет с названием из переменной `S3_BUCKET`, а затем создаем пару ключей доступа и записываем в `S3_ACCESS_KEY` и `S3_SECRET_KEY`
6. Запускаем приложение
   ```bash
   python main.py
   ```
## По чистоте кода
Мне нравится работать с `task` (конфигурация команд в `Taskfile.yml`), но даже если он не установлен, то команды следующие:
```bash
ruff format .  # Автоформатирование под PEP8
ruff check .   # Проверка на наличие неисправленных ошибок
isort .        # Исправление порядка и вида импортов
mypy .         # Проверка аннотаций типов
```