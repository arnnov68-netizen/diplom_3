import allure
import requests
import uuid
from faker import Faker
from pages.main_page import MainPage

fake = Faker()

API_BASE = "https://stellarburgers.education-services.ru/api"


def _create_test_user():
    """Создаёт нового уникального пользователя через API.
    Гарантирует уникальность email через uuid4.
    """
    unique = uuid.uuid4().hex[:8]
    user_data = {
        "email": f"test_{unique}@example.com",
        "password": "TestPass123!",
        "name": f"Test User {unique}"
    }
    response = requests.post(f"{API_BASE}/auth/register", json=user_data)

    if response.status_code == 403:
        # Крайне редкий случай коллизии — повторная попытка
        unique = uuid.uuid4().hex[:8]
        user_data = {
            "email": f"test_{unique}@example.com",
            "password": "TestPass123!",
            "name": f"Test User {unique}"
        }
        response = requests.post(f"{API_BASE}/auth/register", json=user_data)

    assert response.status_code == 200, \
        f"Не удалось создать пользователя: {response.status_code} {response.text}"
    return user_data


@allure.epic("UI Тесты")
@allure.feature("Основная функциональность")
class TestMainFunctionality:

    # ---------- Навигация ----------

    @allure.story("Навигация")
    @allure.title("Переход на страницу 'Конструктор'")
    @allure.description("Проверка, что клик по кнопке 'Конструктор' открывает главную страницу")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_constructor_navigation(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        main_page.click_order_feed()
        main_page.click_constructor()

        with allure.step("Проверка, что мы на главной странице"):
            assert main_page.find_element(main_page.CONSTRUCTOR_BUTTON), \
                "Кнопка 'Конструктор' не найдена"
            assert "stellarburgers" in main_page.get_current_url()

    @allure.story("Навигация")
    @allure.title("Переход на страницу 'Лента Заказов'")
    @allure.description("Проверка, что клик по кнопке 'Лента Заказов' открывает соответствующую страницу")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_feed_navigation(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        order_feed_page = main_page.click_order_feed()

        with allure.step("Проверка, что мы на странице ленты заказов"):
            assert "feed" in order_feed_page.get_current_url(), \
                "URL не содержит 'feed'"
            title = order_feed_page.get_text(order_feed_page.ORDER_FEED_TITLE)
            assert "Лента заказов" in title or "Лента Заказов" in title, \
                f"Заголовок 'Лента заказов' не найден, получено: {title}"

    # ---------- Ингредиенты ----------

    @allure.story("Ингредиенты")
    @allure.title("Открытие модального окна ингредиента")
    @allure.description("Проверка, что клик по ингредиенту открывает модальное окно с деталями")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_modal_open(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_bun_ingredient()

        with allure.step("Проверка, что модальное окно открыто"):
            assert modal.is_modal_open(), "Модальное окно не открылось"
            name = modal.get_ingredient_name()
            assert name, "Название ингредиента не найдено"

    @allure.story("Ингредиенты")
    @allure.title("Закрытие модального окна ингредиента")
    @allure.description("Проверка, что модальное окно закрывается по клику на крестик")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_modal_close(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_bun_ingredient()

        with allure.step("Закрыть модальное окно"):
            assert modal.is_modal_open(), "Модальное окно не открылось"
            modal.close_modal()

        with allure.step("Проверка, что модальное окно закрыто"):
            assert modal.is_modal_closed(), "Модальное окно не закрылось"

    @allure.story("Ингредиенты")
    @allure.title("Детали ингредиента в модальном окне")
    @allure.description("Проверка, что в модальном окне отображаются все детали ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ingredient_details(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_bun_ingredient()

        with allure.step("Проверка всех деталей ингредиента"):
            assert modal.get_ingredient_name(), "Название ингредиента не найдено"
            assert modal.get_ingredient_calories(), "Калории не найдены"
            assert modal.get_ingredient_proteins(), "Белки не найдены"
            assert modal.get_ingredient_fats(), "Жиры не найдены"
            assert modal.get_ingredient_carbohydrates(), "Углеводы не найдены"

    # ---------- Конструктор ----------

    @allure.story("Конструктор заказа")
    @allure.title("Увеличение счётчика ингредиента при добавлении")
    @allure.description("Проверка, что при добавлении ингредиента в заказ счётчик увеличивается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_counter_increases(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        with allure.step("Получить начальное значение счётчика"):
            initial_counter = main_page.get_bun_counter()

        with allure.step("Добавить ингредиент в заказ"):
            main_page.add_bun_to_order()

        with allure.step("Получить новое значение счётчика"):
            new_counter = main_page.get_bun_counter()

        with allure.step("Проверка, что счётчик увеличился"):
            assert new_counter > initial_counter, \
                f"Счётчик не увеличился: {initial_counter} -> {new_counter}"

    # ---------- Создание заказа (с авторизацией) ----------

    @allure.story("Конструктор заказа")
    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка создания заказа после авторизации и добавления ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order(self, driver, base_url):
        with allure.step("Создать тестового пользователя через API"):
            user_data = _create_test_user()
            allure.attach(user_data['email'], name="Email",
                          attachment_type=allure.attachment_type.TEXT)

        main_page = MainPage(driver)
        main_page.open(base_url)

        with allure.step("Перейти на страницу входа"):
            login_page = main_page.click_login_button()

        with allure.step("Авторизоваться"):
            main_page = login_page.login(user_data['email'], user_data['password'])

        with allure.step("Добавить ингредиенты и создать заказ"):
            order_number = main_page.create_order()

        with allure.step("Проверка, что заказ создан"):
            allure.attach(order_number, name="Номер заказа",
                          attachment_type=allure.attachment_type.TEXT)
            assert order_number, "Номер заказа не получен"
            assert order_number.isdigit(), \
                f"Номер заказа должен содержать только цифры, получено: {order_number}"