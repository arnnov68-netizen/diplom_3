import uuid

import allure
import requests

from data.config import API_BASE


def generate_user_data():
    """Генерирует уникальные данные пользователя (без регистрации)."""
    unique = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{unique}@example.com",
        "password": "TestPass123!",
        "name": f"Test User {unique}",
    }


def register_user(user_data=None):
    """Регистрирует пользователя через API.

    Если user_data не передан — генерирует его.
    Возвращает словарь с данными пользователя (email/password/name).
    Бросает RuntimeError, если регистрация не удалась.
    """
    if user_data is None:
        user_data = generate_user_data()

    response = requests.post(f"{API_BASE}/auth/register", json=user_data)

    if response.status_code == 403:
        # Редкая коллизия — перегенерируем и пробуем ещё раз
        user_data = generate_user_data()
        response = requests.post(f"{API_BASE}/auth/register", json=user_data)

    if response.status_code != 200:
        raise RuntimeError(
            f"Не удалось зарегистрировать пользователя: "
            f"status={response.status_code}, body={response.text}"
        )

    return user_data