from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Страница входа /login"""

    # Email: в реальной вёрстке name="name" (странно, но так есть)
    EMAIL_INPUT = (By.XPATH, "//input[@type='text' and @name='name']")

    # Пароль: name="Пароль" (по-русски!), надёжнее искать по type
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")

    # Кнопка "Войти"
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")

    # Ссылка на регистрацию (если нужна)
    REGISTER_LINK = (By.XPATH, "//a[contains(., 'Зарегистрироваться')]")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        elem = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        elem.clear()
        elem.send_keys(email)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        elem = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        elem.clear()
        elem.send_keys(password)
        return self

    @allure.step("Клик на кнопку 'Войти'")
    def click_login_button(self):
        self.click_element(self.LOGIN_SUBMIT_BUTTON)
        # Ждём ухода с /login
        WebDriverWait(self.driver, 15).until(
            lambda d: "/login" not in d.current_url
        )
        from pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step("Авторизоваться: {email}")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        return self.click_login_button()