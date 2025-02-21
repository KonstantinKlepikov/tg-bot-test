# Tg-bot-test

Запуск стека утилитой `make`

- `make serve` для запуска dev-стека
- `make down` остановка и удаление стека

Документация доступна из (смотреть без VPN): [swagger](http://localhost:8123/docs)

## Установка зависимостей в рабочую область

1. Перейти в область отдельного репозитория (открыть новый терминал и выбрать область)
2. Установить `poetry` окружение и подготовьте линтер. Для этого используйте `poetry config virtualenvs.in-project true` и команду `poetry install --with dev --no-root`. pyproject.toml находится в корне проекта. Обрати внимание, что poetry обращается к внутреннему репозиторию и регистри, поэтмоу потребуется активировать VPN.
3. Указать путь к нтерпретатору в `.venv`. Перезапустить IDE.

Лучший способ работы с проектом - подтянуть версию python через pyenv и сохранить настройки poetry в файле конфигураций внутри проекта. Тогда зависимости окружения будут сохранены в локальной папке внутри проекта. К примеру так:

```txt
# .python-version

3.12.5
```

```toml
# poetry.toml

virtualenvs.create = true
virtualenvs.prefer-active-python = true
# ... some other variables
```

## Как работает заглушка

При перовом обращении POST вернет 404. Это сделано для проверки автоудаления бота из канала при 404.

Повторное обращение вернет 201

При обращении к PUT 200 вернется только на первые 4 запроса, после чего на 5-ом запросе поднимется 404. Это сделано для проверки автоудаления бота при отвяке юзера от айдишника канала.

Далее цикл можно повторить.

Все этом можно потыкать руками в сваггере: [swagger](http://localhost:8123/docs) на локалхосте.

Получая данные, сервис сохраняет их в виде json в папке result на диск.
