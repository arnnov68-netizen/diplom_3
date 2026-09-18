from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import allure


class IngredientModal(BasePage):
    """Модальное окно ингредиента"""

    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")

    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//button[contains(@class, 'Modal_modal__close')]"
    )

    # Название ингредиента — это <p class="text text_type_main-medium">,
    # НЕ заголовок "Детали ингредиента" (<h2 class="Modal_modal__title_modified">)
    INGREDIENT_NAME = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//p[contains(@class, 'text_type_main-medium')]"
    )

    # Пищевая ценность: подписи БЕЗ пробела после запятой!
    CALORIES = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//p[contains(text(), 'Калории')]/following-sibling::p"
    )
    PROTEINS = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//p[contains(text(), 'Белки')]/following-sibling::p"
    )
    FATS = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//p[contains(text(), 'Жиры')]/following-sibling::p"
    )
    CARBS = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//p[contains(text(), 'Углеводы')]/following-sibling::p"
    )

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_modal(self):
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.MODAL_CLOSE_BUTTON)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", button
            )
            self.driver.execute_script("arguments[0].click();", button)
        except TimeoutException:
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        self.wait_for_element_to_disappear(self.MODAL_CONTAINER, timeout=10)
        return self

    @allure.step("Получить название ингредиента")
    def get_ingredient_name(self):
        self.wait_for_visibility(self.INGREDIENT_NAME)
        return self.get_text(self.INGREDIENT_NAME)

    @allure.step("Получить калорийность")
    def get_ingredient_calories(self):
        return self.get_text(self.CALORIES)

    @allure.step("Получить белки")
    def get_ingredient_proteins(self):
        return self.get_text(self.PROTEINS)

    @allure.step("Получить жиры")
    def get_ingredient_fats(self):
        return self.get_text(self.FATS)

    @allure.step("Получить углеводы")
    def get_ingredient_carbohydrates(self):
        return self.get_text(self.CARBS)

    @allure.step("Проверить, что модальное окно открыто")
    def is_modal_open(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.MODAL_CONTAINER)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.MODAL_CONTAINER)
            )
        except TimeoutException:
            return False
        return True