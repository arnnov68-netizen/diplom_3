from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import allure
import time


class MainPage(BasePage):
    """Главная страница Stellar Burgers (Конструктор)"""

    # ---------- Навигация ----------
    CONSTRUCTOR_BUTTON = (
        By.XPATH, "//a[contains(., 'Конструктор')]"
    )
    ORDER_FEED_BUTTON = (
        By.XPATH, "//a[contains(., 'Лента Заказов')]"
    )
    LOGIN_BUTTON = (
        By.XPATH, "//button[contains(., 'Войти в аккаунт')]"
    )
    PERSONAL_ACCOUNT_BUTTON = (
        By.XPATH, "//a[contains(., 'Личный Кабинет')]"
    )

    # ---------- Ингредиенты ----------
    BUN_INGREDIENT = (
        By.XPATH,
        "//a[contains(@href, '/ingredient/')]"
        "[.//p[contains(text(), 'булка') or contains(text(), 'Булка')]]"
    )
    SAUCE_INGREDIENT = (
        By.XPATH,
        "//a[contains(@href, '/ingredient/')]"
        "[.//p[contains(text(), 'Соус') or contains(text(), 'соус')]]"
    )
    FILLING_INGREDIENT = (
        By.XPATH,
        "//a[contains(@href, '/ingredient/')]"
        "[.//p[contains(text(), 'Начинк') or contains(text(), 'начинк') "
        "or contains(text(), 'Мясо') or contains(text(), 'мясо')]]"
    )

    # Счётчик булки — цифра внутри карточки ингредиента
    BUN_COUNTER = (
        By.XPATH,
        "//a[contains(@href, '/ingredient/')]"
        "[.//p[contains(text(), 'булка') or contains(text(), 'Булка')]]"
        "//p[contains(@class, 'counter')]"
    )

    # ---------- Конструктор ----------
    CONSTRUCTOR_BASKET = (
        By.XPATH,
        "//div[contains(@class, 'BurgerConstructor_basket')]"
        " | //ul[contains(@class, 'BurgerConstructor_basket')]"
        " | //section[contains(@class, 'BurgerConstructor')]"
    )

    # ---------- Оформление заказа ----------
    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Оформить заказ')]"
    )
    ORDER_MODAL = (
        By.XPATH, "//div[contains(@class, 'Modal_modal__container')]"
    )
    ORDER_NUMBER = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//h2[contains(@class, 'text_type_digits-large')]"
    )
    CLOSE_ORDER_MODAL_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container')]"
        "//button[contains(@class, 'Modal_modal__close')]"
    )

    def __init__(self, driver):
        super().__init__(driver)

    # ---------- Навигация ----------

    @allure.step("Клик на кнопку 'Конструктор'")
    def click_constructor(self):
        self.click_element(self.CONSTRUCTOR_BUTTON)
        return self

    @allure.step("Клик на кнопку 'Лента Заказов'")
    def click_order_feed(self):
        self.click_element(self.ORDER_FEED_BUTTON)
        self.wait.until(lambda d: "/feed" in d.current_url)
        from pages.order_feed_page import OrderFeedPage
        return OrderFeedPage(self.driver)

    @allure.step("Клик на кнопку 'Личный Кабинет'")
    def click_personal_account(self):
        self.click_element(self.PERSONAL_ACCOUNT_BUTTON)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    @allure.step("Клик на кнопку 'Войти в аккаунт'")
    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    # ---------- Ингредиенты ----------

    @allure.step("Клик на булку")
    def click_bun_ingredient(self):
        self.click_element(self.BUN_INGREDIENT)
        from pages.ingredient_modal import IngredientModal
        return IngredientModal(self.driver)

    @allure.step("Клик на соус")
    def click_sauce_ingredient(self):
        self.click_element(self.SAUCE_INGREDIENT)
        from pages.ingredient_modal import IngredientModal
        return IngredientModal(self.driver)

    @allure.step("Клик на начинку")
    def click_filling_ingredient(self):
        self.click_element(self.FILLING_INGREDIENT)
        from pages.ingredient_modal import IngredientModal
        return IngredientModal(self.driver)

    # ---------- Счётчики ----------

    @allure.step("Получить счётчик булки")
    def get_bun_counter(self):
        """Возвращает число рядом с булкой или 0, если счётчика нет."""
        try:
            element = self.find_element(self.BUN_COUNTER, timeout=3)
            text = element.text.strip()
            return int(text) if text.isdigit() else 0
        except Exception:
            return 0

    # ---------- Добавление ингредиентов в заказ ----------

    @allure.step("Добавить булку в заказ")
    def add_bun_to_order(self):
        self._drag_and_drop(self.BUN_INGREDIENT)
        return self

    @allure.step("Добавить соус в заказ")
    def add_sauce_to_order(self):
        self._drag_and_drop(self.SAUCE_INGREDIENT)
        return self

    @allure.step("Добавить начинку в заказ")
    def add_filling_to_order(self):
        self._drag_and_drop(self.FILLING_INGREDIENT)
        return self

    def _drag_and_drop(self, source_locator):
        """Универсальный drag-n-drop ингредиента в конструктор."""
        source = self.find_element(source_locator)
        target = self.find_element(self.CONSTRUCTOR_BASKET)

        self.driver.execute_script("""
            function simulateDragDrop(sourceNode, destinationNode) {
                var EVENT_TYPES = {
                    DRAG_END: 'dragend',
                    DRAG_START: 'dragstart',
                    DROP: 'drop'
                };
                function createCustomEvent(type) {
                    var event = new CustomEvent("CustomEvent");
                    event.initCustomEvent(type, true, true, null);
                    event.dataTransfer = {
                        data: {},
                        setData: function(type, val) { this.data[type] = val; },
                        getData: function(type) { return this.data[type]; }
                    };
                    return event;
                }
                function dispatchEvent(node, type, event) {
                    if (node.dispatchEvent) {
                        return node.dispatchEvent(event);
                    }
                }
                var dragStartEvent = createCustomEvent(EVENT_TYPES.DRAG_START);
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START, dragStartEvent);

                var dropEvent = createCustomEvent(EVENT_TYPES.DROP);
                dropEvent.dataTransfer = dragStartEvent.dataTransfer;
                dispatchEvent(destinationNode, EVENT_TYPES.DROP, dropEvent);

                var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
                dragEndEvent.dataTransfer = dragStartEvent.dataTransfer;
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, dragEndEvent);
            }
            simulateDragDrop(arguments[0], arguments[1]);
        """, source, target)

    # ---------- Оформление заказа ----------

    @allure.step("Клик на кнопку 'Оформить заказ'")
    def click_order_button(self):
        self.click_element(self.ORDER_BUTTON)
        return self

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number(self):
        """Ждёт появления реального номера заказа (не заглушки 9999)."""
        self.wait_for_visibility(self.ORDER_NUMBER, timeout=15)

        # Ждём, пока номер перестанет быть заглушкой '9999'
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element(*self.ORDER_NUMBER).text.strip() != "9999"
        )

        # Небольшая пауза, чтобы номер точно обновился
        time.sleep(0.5)

        return self.get_text(self.ORDER_NUMBER).strip()

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        try:
            self.click_element(self.CLOSE_ORDER_MODAL_BUTTON)
            self.wait_for_element_to_disappear(self.ORDER_MODAL, timeout=10)
        except Exception:
            pass
        return self

    @allure.step("Создать заказ")
    def create_order(self, add_ingredients=True):
        if add_ingredients:
            self.add_bun_to_order()
            self.add_sauce_to_order()
            self.add_filling_to_order()
        self.click_order_button()
        order_number = self.get_order_number()
        self.close_order_modal()
        return order_number