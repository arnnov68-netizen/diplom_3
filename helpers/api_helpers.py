import allure
import requests

from data.config import API_BASE


@allure.step("POST /auth/register — регистрация пользователя")
def create_user(user_data):
    return requests.post(f"{API_BASE}/auth/register", json=user_data)


@allure.step("DELETE /auth/user — удаление пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(f"{API_BASE}/auth/user", headers=headers)