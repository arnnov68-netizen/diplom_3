import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class IngredientModal(BasePage):
    """Модальное окно ингредиента"""

    MODAL_CONTAINER = (
        By.XPATH, "//div[contains(@class, 'Modal_modal__container')]"
    )
    MODAL_OVERLAY = (
        By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]"
    )
    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//button[contains(@class, 'Modal_modal__close')]"
    )
    INGREDIENT_NAME = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//p[contains(@class, 'text_type_main-medium')]"
    )
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
        if self.is_element_present(self.MODAL_CLOSE_BUTTON, timeout=5):
            self.js_click(self.MODAL_CLOSE_BUTTON)
        else:
            self.press_escape()
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
        return self.is_element_present(self.MODAL_CONTAINER, timeout=5)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self):
        return self.wait_for_element_to_disappear(
            self.MODAL_CONTAINER, timeout=5
        )