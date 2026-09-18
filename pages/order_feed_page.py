from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class OrderFeedPage(BasePage):
    """Страница ленты заказов /feed"""

    ORDER_FEED_TITLE = (By.XPATH, "//h1[contains(., 'Лента заказов')]")

    # Внимание: в HTML "все время" (без буквы ё!)
    TOTAL_ORDERS_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p"
    )
    TODAY_ORDERS_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p"
    )

    # Заказы в работе — список <li> в секции "В работе"
    ORDERS_IN_PROGRESS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderListReady')]/li"
    )

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получить 'Выполнено за всё время'")
    def get_total_orders_count(self):
        element = self.find_element(self.TOTAL_ORDERS_COUNTER)
        text = element.text.strip().replace(" ", "")
        return int(text) if text.isdigit() else 0

    @allure.step("Получить 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        element = self.find_element(self.TODAY_ORDERS_COUNTER)
        text = element.text.strip().replace(" ", "")
        return int(text) if text.isdigit() else 0

    @allure.step("Получить список заказов в работе")
    def get_orders_in_progress(self):
        elements = self.driver.find_elements(*self.ORDERS_IN_PROGRESS)
        return [el.text.strip() for el in elements if el.text.strip()]

    @allure.step("Проверить, что заказ в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        orders = self.get_orders_in_progress()
        # Нормализуем: убираем # и ведущие нули
        order_clean = str(order_number).lstrip('0').strip()
        return any(
            str(o).lstrip('0').strip() == order_clean
            for o in orders
        )