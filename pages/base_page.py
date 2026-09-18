from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import allure


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть страницу: {url}")
    def open(self, url):
        """Открывает страницу по URL и ждёт загрузки"""
        self.driver.get(url)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    def find_element(self, locator, timeout=15):
        """Находит элемент с ожиданием"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"element_not_found_{locator}",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def click_element(self, locator, timeout=15):
        """Кликает по элементу с обработкой перекрытия"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        return self

    def get_text(self, locator, timeout=15):
        """Получает текст элемента"""
        element = self.find_element(locator, timeout)
        return element.text

    def wait_for_visibility(self, locator, timeout=15):
        """Ожидает видимость элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_to_disappear(self, locator, timeout=15):
        """Ожидает исчезновения элемента. Возвращает True/False."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=3):
        """Проверяет наличие элемента без выброса исключения."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url