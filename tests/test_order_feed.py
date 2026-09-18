import allure
import time
from pages.main_page import MainPage


@allure.epic("UI Тесты")
@allure.feature("Лента заказов")
class TestOrderFeed:

    def _login(self, driver, base_url, ui_user):
        """Логинимся и возвращаем MainPage на главной."""
        main_page = MainPage(driver)
        main_page.open(base_url)
        login_page = main_page.click_login_button()
        return login_page.login(ui_user['email'], ui_user['password'])

    # ---------- Счётчики ----------

    @allure.story("Счётчики заказов")
    @allure.title("Увеличение счётчика 'Выполнено за всё время'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_total_orders_counter_increases(self, driver, base_url, ui_user):
        main_page = self._login(driver, base_url, ui_user)

        with allure.step("Перейти в ленту заказов"):
            order_feed_page = main_page.click_order_feed()

        with allure.step("Получить начальное значение"):
            initial_total = order_feed_page.get_total_orders_count()
            allure.attach(str(initial_total), "Начальное",
                          allure.attachment_type.TEXT)

        with allure.step("Создать заказ"):
            main_page.click_constructor()
            main_page.create_order()

        with allure.step("Вернуться в ленту заказов"):
            main_page.click_order_feed()
            time.sleep(3)
            new_total = order_feed_page.get_total_orders_count()
            allure.attach(str(new_total), "Новое",
                          allure.attachment_type.TEXT)

        with allure.step("Проверка, что счётчик увеличился"):
            assert new_total > initial_total, \
                f"Счётчик не увеличился: {initial_total} -> {new_total}"

    @allure.story("Счётчики заказов")
    @allure.title("Увеличение счётчика 'Выполнено за сегодня'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_today_orders_counter_increases(self, driver, base_url, ui_user):
        main_page = self._login(driver, base_url, ui_user)

        with allure.step("Перейти в ленту заказов"):
            order_feed_page = main_page.click_order_feed()

        with allure.step("Получить начальное значение"):
            initial_today = order_feed_page.get_today_orders_count()
            allure.attach(str(initial_today), "Начальное",
                          allure.attachment_type.TEXT)

        with allure.step("Создать заказ"):
            main_page.click_constructor()
            main_page.create_order()

        with allure.step("Вернуться в ленту заказов"):
            main_page.click_order_feed()
            time.sleep(3)
            new_today = order_feed_page.get_today_orders_count()
            allure.attach(str(new_today), "Новое",
                          allure.attachment_type.TEXT)

        with allure.step("Проверка, что счётчик увеличился"):
            assert new_today > initial_today, \
                f"Счётчик не увеличился: {initial_today} -> {new_today}"

    @allure.story("Заказы в работе")
    @allure.title("Появление заказа в разделе 'В работе'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_appears_in_progress(self, driver, base_url, ui_user):
        main_page = self._login(driver, base_url, ui_user)

        with allure.step("Создать заказ"):
            order_number = main_page.create_order()
            allure.attach(order_number, "Номер заказа",
                          allure.attachment_type.TEXT)

        with allure.step("Перейти в ленту заказов"):
            order_feed_page = main_page.click_order_feed()

        with allure.step("Проверить, что заказ в разделе 'В работе'"):
            # Ждём появления заказа в разделе "В работе" (до 20 секунд)
            deadline = time.time() + 20
            is_in_progress = False
            while time.time() < deadline:
                if order_feed_page.is_order_in_progress(order_number):
                    is_in_progress = True
                    break
                time.sleep(1)

            assert is_in_progress, \
                f"Заказ {order_number} не появился в разделе 'В работе'"

    @allure.story("Счётчики заказов")
    @allure.title("Обновление обоих счётчиков после создания заказа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_both_counters_update(self, driver, base_url, ui_user):
        main_page = self._login(driver, base_url, ui_user)

        with allure.step("Перейти в ленту заказов"):
            order_feed_page = main_page.click_order_feed()

        with allure.step("Получить начальные значения"):
            initial_total = order_feed_page.get_total_orders_count()
            initial_today = order_feed_page.get_today_orders_count()

        with allure.step("Создать заказ"):
            main_page.click_constructor()
            main_page.create_order()

        with allure.step("Вернуться в ленту заказов"):
            main_page.click_order_feed()
            time.sleep(3)

        with allure.step("Проверить оба счётчика"):
            new_total = order_feed_page.get_total_orders_count()
            new_today = order_feed_page.get_today_orders_count()

            assert new_total > initial_total, \
                f"Total не увеличился: {initial_total} -> {new_total}"
            assert new_today > initial_today, \
                f"Today не увеличился: {initial_today} -> {new_today}"