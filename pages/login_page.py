import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница входа /login"""

    EMAIL_INPUT = (By.XPATH, "//input[@type='text' and @name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(., 'Зарегистрироваться')]")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        self.send_keys(self.EMAIL_INPUT, email)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)
        return self

    @allure.step("Клик на кнопку 'Войти'")
    def click_login_button(self):
        self.click_element(self.LOGIN_SUBMIT_BUTTON)
        self.wait_for_url_not_contains("/login")
        from pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step("Авторизоваться: {email}")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        return self.click_login_button()