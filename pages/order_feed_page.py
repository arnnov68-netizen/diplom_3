import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


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
    ORDERS_IN_PROGRESS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderListReady')]/li"
    )

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получить заголовок страницы 'Лента заказов'")
    def get_title(self):
        return self.get_text(self.ORDER_FEED_TITLE)

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

    @allure.step("Дождаться увеличения счётчика 'Выполнено за всё время'")
    def wait_for_total_orders_change(self, previous_value, timeout=15):
        """Ждёт, пока счётчик 'за всё время' станет больше previous_value."""
        self.wait_until(
            lambda d: self.get_total_orders_count() > previous_value,
            description=(
                f"увеличение счётчика 'за всё время' "
                f"относительно {previous_value}"
            ),
            timeout=timeout,
        )
        return self

    @allure.step("Дождаться увеличения счётчика 'Выполнено за сегодня'")
    def wait_for_today_orders_change(self, previous_value, timeout=15):
        """Ждёт, пока счётчик 'за сегодня' станет больше previous_value."""
        self.wait_until(
            lambda d: self.get_today_orders_count() > previous_value,
            description=(
                f"увеличение счётчика 'за сегодня' "
                f"относительно {previous_value}"
            ),
            timeout=timeout,
        )
        return self

    @allure.step("Получить список заказов в работе")
    def get_orders_in_progress(self):
        elements = self.find_elements(self.ORDERS_IN_PROGRESS)
        return [el.text.strip() for el in elements if el.text.strip()]

    @allure.step("Проверить, что заказ в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        orders = self.get_orders_in_progress()
        order_clean = str(order_number).lstrip('0').strip()
        return any(
            str(o).lstrip('0').strip() == order_clean
            for o in orders
        )

    @allure.step("Дождаться появления заказа '{order_number}' в 'В работе'")
    def wait_order_in_progress(self, order_number, timeout=20):
        self.wait_until(
            lambda d: self.is_order_in_progress(order_number),
            description=f"заказ {order_number} в разделе 'В работе'",
            timeout=timeout,
        )
        return self