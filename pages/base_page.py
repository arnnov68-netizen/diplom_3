import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовый класс для всех страниц.
    Вся работа с Selenium (WebDriverWait, execute_script, ActionChains,
    поиск элементов) живёт здесь. Наследники вызывают только эти методы.
    """

    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver

    # ---------- Общие ----------

    @allure.step("Открыть страницу: {url}")
    def open(self, url):
        self.driver.get(url)
        self._wait_document_ready()
        return self

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    # ---------- Ожидания ----------

    @allure.step("Дождаться загрузки документа")
    def _wait_document_ready(self, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    @allure.step("Дождаться появления элемента: {locator}")
    def find_element(self, locator, timeout=DEFAULT_TIMEOUT):
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

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_for_visibility(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Дождаться исчезновения элемента: {locator}")
    def wait_for_element_to_disappear(self, locator, timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить наличие элемента: {locator}")
    def is_element_present(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Дождаться, что URL содержит: {fragment}")
    def wait_for_url_contains(self, fragment, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            lambda d: fragment in d.current_url
        )
        return self

    @allure.step("Дождаться, что URL не содержит: {fragment}")
    def wait_for_url_not_contains(self, fragment, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            lambda d: fragment not in d.current_url
        )
        return self

    @allure.step("Дождаться, пока текст элемента изменится: {locator}")
    def wait_for_text_change(self, locator, previous_text, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*locator).text.strip() != previous_text
        )
        return self

    @allure.step("Дождаться выполнения условия: {description}")
    def wait_until(self, predicate, description="условие", timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(predicate)
        return self

    # ---------- Действия ----------

    @allure.step("Клик по элементу: {locator}")
    def click_element(self, locator, timeout=DEFAULT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        return self

    @allure.step("Ввести текст в элемент: {locator}")
    def send_keys(self, locator, text, timeout=DEFAULT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        return self

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        element = self.find_element(locator, timeout)
        return element.text

    @allure.step("Выполнить JavaScript на элементе: {locator}")
    def execute_script_on_element(self, locator, script, timeout=DEFAULT_TIMEOUT):
        element = self.find_element(locator, timeout)
        self.driver.execute_script(script, element)
        return self

    @allure.step("Клик через JavaScript: {locator}")
    def js_click(self, locator, timeout=DEFAULT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)
        return self

    @allure.step("Нажать ESC")
    def press_escape(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        return self

    @allure.step("Drag-and-drop: {source_locator} -> {target_locator}")
    def drag_and_drop(self, source_locator, target_locator,
                      timeout=DEFAULT_TIMEOUT):
        source = self.find_element(source_locator, timeout)
        target = self.find_element(target_locator, timeout)

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
        return self