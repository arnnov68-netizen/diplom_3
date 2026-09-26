import allure

from data.config import BASE_URL
from pages.login_page import LoginPage
from pages.main_page import MainPage


@allure.epic("UI Тесты")
@allure.feature("Лента заказов")
class TestOrderFeed:

    def _login(self, driver, ui_user):
        """Логинимся и возвращаем MainPage на главной."""
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.login(ui_user['email'], ui_user['password'])

        return MainPage(driver)

    # ---------- Счётчики ----------

    @allure.story("Счётчики заказов")
    @allure.title("Увеличение счётчика 'Выполнено за всё время'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_total_orders_counter_increases(self, driver, ui_user):
        main_page = self._login(driver, ui_user)

        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()

        from pages.order_feed_page import OrderFeedPage
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Получить начальное значение"):
            initial_total = order_feed_page.get_total_orders_count()
            allure.attach(str(initial_total), "Начальное",
                          allure.attachment_type.TEXT)

        with allure.step("Создать заказ"):
            main_page.click_constructor()
            main_page.create_order()

        with allure.step("Вернуться в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page.wait_for_text_change(
                order_feed_page.TOTAL_ORDERS_COUNTER,
                previous_text=str(initial_total),
                timeout=15,
            )
            new_total = order_feed_page.get_total_orders_count()
            allure.attach(str(new_total), "Новое",
                          allure.attachment_type.TEXT)

        with allure.step("Проверка, что счётчик увеличился"):
            assert new_total > initial_total, \
                f"Счётчик не увеличился: {initial_total} -> {new_total}"

    @allure.story("Счётчики заказов")
    @allure.title("Увеличение счётчика 'Выполнено за сегодня'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_today_orders_counter_increases(self, driver, ui_user):
        main_page = self._login(driver, ui_user)

        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()

        from pages.order_feed_page import OrderFeedPage
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Получить начальное значение"):
            initial_today = order_feed_page.get_today_orders_count()
            allure.attach(str(initial_today), "Начальное",
                          allure.attachment_type.TEXT)

        with allure.step("Создать заказ"):
            main_page.click_constructor()
            main_page.create_order()

        with allure.step("Вернуться в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page.wait_for_text_change(
                order_feed_page.TODAY_ORDERS_COUNTER,
                previous_text=str(initial_today),
                timeout=15,
            )
            new_today = order_feed_page.get_today_orders_count()
            allure.attach(str(new_today), "Новое",
                          allure.attachment_type.TEXT)

        with allure.step("Проверка, что счётчик увеличился"):
            assert new_today > initial_today, \
                f"Счётчик не увеличился: {initial_today} -> {new_today}"

    @allure.story("Заказы в работе")
    @allure.title("Появление заказа в разделе 'В работе'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_appears_in_progress(self, driver, ui_user):
        main_page = self._login(driver, ui_user)

        with allure.step("Создать заказ"):
            order_number = main_page.create_order()
            allure.attach(order_number, "Номер заказа",
                          allure.attachment_type.TEXT)

        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()

        from pages.order_feed_page import OrderFeedPage
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Дождаться появления заказа в разделе 'В работе'"):
            order_feed_page.wait_order_in_progress(order_number, timeout=20)

        with allure.step("Проверка, что заказ в разделе 'В работе'"):
            assert order_feed_page.is_order_in_progress(order_number), \
                f"Заказ {order_number} не появился в разделе 'В работе'"

    @allure.story("Счётчики заказов")
    @allure.title("Обновление обоих счётчиков после создания заказа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_both_counters_update(self, driver, ui_user):
        main_page = self._login(driver, ui_user)

        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()

        from pages.order_feed_page import OrderFeedPage
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Получить начальные значения"):
            initial_total = order_feed_page.get_total_orders_count()
            initial_today = order_feed_page.get_today_orders_count()

        with allure.step("Создать заказ"):
            main_page.click_constructor()
            main_page.create_order()

        with allure.step("Вернуться в ленту заказов"):
            main_page.click_order_feed()

        with allure.step("Проверить оба счётчика"):
            order_feed_page.wait_for_text_change(
                order_feed_page.TOTAL_ORDERS_COUNTER,
                previous_text=str(initial_total),
                timeout=15,
            )
            order_feed_page.wait_for_text_change(
                order_feed_page.TODAY_ORDERS_COUNTER,
                previous_text=str(initial_today),
                timeout=15,
            )

            new_total = order_feed_page.get_total_orders_count()
            new_today = order_feed_page.get_today_orders_count()

            assert new_total > initial_total, \
                f"Total не увеличился: {initial_total} -> {new_total}"
            assert new_today > initial_today, \
                f"Today не увеличился: {initial_today} -> {new_today}"
