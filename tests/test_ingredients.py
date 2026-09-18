import allure
from pages.main_page import MainPage


@allure.epic("UI Тесты")
@allure.feature("Ингредиенты")
class TestIngredients:

    @allure.story("Модальное окно")
    @allure.title("Открытие модального окна для булки")
    @allure.description("Проверка открытия модального окна при клике на булку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bun_modal_open(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_bun_ingredient()

        with allure.step("Проверка открытия модального окна"):
            assert modal.is_modal_open(), "Модальное окно не открылось"

        with allure.step("Проверка названия ингредиента"):
            name = modal.get_ingredient_name()
            allure.attach(name, name="Название ингредиента",
                          attachment_type=allure.attachment_type.TEXT)
            assert name, "Название ингредиента пустое"
            assert "Детали" not in name, \
                f"Получен заголовок '{name}' вместо названия булки"
            assert "булка" in name.lower(), \
                f"Название '{name}' не содержит 'булка'"

    @allure.story("Модальное окно")
    @allure.title("Открытие модального окна для соуса")
    @allure.description("Проверка открытия модального окна при клике на соус")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sauce_modal_open(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_sauce_ingredient()

        with allure.step("Проверка открытия модального окна"):
            assert modal.is_modal_open(), "Модальное окно не открылось"

        with allure.step("Проверка названия ингредиента"):
            name = modal.get_ingredient_name()
            allure.attach(name, name="Название ингредиента",
                          attachment_type=allure.attachment_type.TEXT)
            assert name, "Название ингредиента пустое"
            assert "Детали" not in name, \
                f"Получен заголовок '{name}' вместо названия соуса"

    @allure.story("Модальное окно")
    @allure.title("Открытие модального окна для начинки")
    @allure.description("Проверка открытия модального окна при клике на начинку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filling_modal_open(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_filling_ingredient()

        with allure.step("Проверка открытия модального окна"):
            assert modal.is_modal_open(), "Модальное окно не открылось"

        with allure.step("Проверка названия ингредиента"):
            name = modal.get_ingredient_name()
            allure.attach(name, name="Название ингредиента",
                          attachment_type=allure.attachment_type.TEXT)
            assert name, "Название ингредиента пустое"
            assert "Детали" not in name, \
                f"Получен заголовок '{name}' вместо названия начинки"

    @allure.story("Модальное окно")
    @allure.title("Закрытие модального окна")
    @allure.description("Проверка закрытия модального окна по крестику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_modal_close(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_bun_ingredient()

        with allure.step("Проверка, что модальное окно открылось"):
            assert modal.is_modal_open(), "Модальное окно не открылось"

        with allure.step("Закрытие модального окна"):
            modal.close_modal()

        with allure.step("Проверка, что модальное окно закрылось"):
            assert modal.is_modal_closed(), "Модальное окно не закрылось"

    @allure.story("Модальное окно")
    @allure.title("Отображение деталей ингредиента")
    @allure.description("Проверка отображения пищевой ценности ингредиента в модальном окне")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ingredient_details(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        modal = main_page.click_bun_ingredient()

        with allure.step("Проверка названия ингредиента"):
            assert modal.get_ingredient_name(), "Название ингредиента не найдено"

        with allure.step("Проверка калорийности"):
            assert modal.get_ingredient_calories(), "Калории не найдены"

        with allure.step("Проверка белков"):
            assert modal.get_ingredient_proteins(), "Белки не найдены"

        with allure.step("Проверка жиров"):
            assert modal.get_ingredient_fats(), "Жиры не найдены"

        with allure.step("Проверка углеводов"):
            assert modal.get_ingredient_carbohydrates(), "Углеводы не найдены"

    @allure.story("Счётчики")
    @allure.title("Увеличение счётчика булок")
    @allure.description("Проверка увеличения счётчика при добавлении булки")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bun_counter_increases(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        with allure.step("Получить начальное значение счётчика"):
            initial_counter = main_page.get_bun_counter()
            allure.attach(str(initial_counter),
                          name="Начальное значение счётчика",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Добавить булку в заказ"):
            main_page.add_bun_to_order()

        with allure.step("Получить новое значение счётчика"):
            new_counter = main_page.get_bun_counter()
            allure.attach(str(new_counter),
                          name="Новое значение счётчика",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка увеличения счётчика"):
            assert new_counter > initial_counter, \
                f"Счётчик не увеличился: {initial_counter} -> {new_counter}"

    @allure.story("Счётчики")
    @allure.title("Многократное добавление ингредиента")
    @allure.description("Проверка счётчика при многократном добавлении ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_additions(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)

        with allure.step("Получить начальное значение счётчика"):
            initial_counter = main_page.get_bun_counter()
            allure.attach(str(initial_counter),
                          name="Начальное значение",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Добавить булку 3 раза"):
            for i in range(3):
                main_page.add_bun_to_order()
                allure.attach(f"Добавление {i + 1}",
                              name=f"Попытка_{i + 1}",
                              attachment_type=allure.attachment_type.TEXT)

        with allure.step("Получить новое значение счётчика"):
            new_counter = main_page.get_bun_counter()
            allure.attach(str(new_counter),
                          name="Новое значение",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка увеличения счётчика"):
            assert new_counter >= initial_counter + 1, \
                f"Счётчик не увеличился: {initial_counter} -> {new_counter}"