# UI Автотесты для Stellar Burgers

Автотесты для UI сервиса Stellar Burgers с использованием Selenium, pytest,
Page Object и Allure.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest --alluredir=allure-results --clean-alluredir -v
```

## Просмотр Allure-отчёта

```bash
allure serve allure-results
```

## Структура

- `pages/` — Page Object'ы (`BasePage`, `MainPage`, `LoginPage`, `OrderFeedPage`, `IngredientModal`)
- `tests/` — UI-тесты (ингредиенты, основная функциональность, лента заказов)
- `helpers/` — API-хелперы (`create_user`, `delete_user`) и генерация пользователя
- `data/` — конфиг (`config.py`)
- `conftest.py` — фикстуры `driver` (chrome/firefox) и `ui_user`, хук скриншотов при падении
- `allure-results/` — результаты последнего прогона