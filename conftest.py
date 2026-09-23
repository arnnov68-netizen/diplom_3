import os
import uuid

import allure
import pytest
import requests
from faker import Faker
from selenium import webdriver

fake = Faker()

API_BASE = "https://stellarburgers.education-services.ru/api"
BASE_URL = "https://stellarburgers.education-services.ru/"


# ============================================================
# Фикстуры для UI-тестов (Selenium)
# ============================================================

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """Фикстура для создания драйвера браузера.
    Selenium Manager сам скачает нужный драйвер.
    """
    browser = request.param
    allure.attach(
        f"Запуск теста в браузере: {browser}",
        name="Browser info",
        attachment_type=allure.attachment_type.TEXT
    )

    driver = None
    try:
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options)
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)

        try:
            driver.maximize_window()
        except Exception:
            pass

        driver.browser_name = browser

        yield driver

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


@pytest.fixture
def base_url():
    """Базовый URL приложения."""
    return BASE_URL


@pytest.fixture
def ui_user():
    """Создаёт уникального пользователя для UI-тестов через API."""
    unique = uuid.uuid4().hex[:8]
    user_data = {
        "email": f"test_{unique}@example.com",
        "password": "TestPass123!",
        "name": f"Test User {unique}"
    }
    response = requests.post(f"{API_BASE}/auth/register", json=user_data)

    if response.status_code == 403:
        unique = uuid.uuid4().hex[:8]
        user_data = {
            "email": f"test_{unique}@example.com",
            "password": "TestPass123!",
            "name": f"Test User {unique}"
        }
        requests.post(f"{API_BASE}/auth/register", json=user_data)

    return user_data


# ============================================================
# Хук для скриншотов при падении UI-тестов
# ============================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Создаёт скриншот при падении UI-теста и прикрепляет к Allure-отчёту."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)

                browser = getattr(driver, "browser_name", "unknown")
                safe_test_name = item.name.replace("/", "_").replace("\\", "_")
                screenshot_path = os.path.join(
                    screenshot_dir, f"{safe_test_name}_{browser}.png"
                )

                try:
                    driver.save_screenshot(screenshot_path)
                    allure.attach.file(
                        screenshot_path,
                        name=f"Screenshot_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception:
                    pass