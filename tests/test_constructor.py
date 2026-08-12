from pages.constructor_page import ConstructorPage

import allure
import pytest
import time

import urls

# Проверка основной функциональности
#
# Проверяем:
#
# - переход по клику на «Конструктор»;
# - переход по клику на раздел «Лента заказов»;
# - если кликнуть на ингредиент, появится всплывающее окно с деталями;
# - всплывающее окно закрывается кликом по крестику;
# - при добавлении ингредиента в заказ счётчик этого ингредиента увеличивается.


class TestConstructor:

    @allure.title('Проверка, что клик в шапке по кнопке "Конструктор" ведёт на главную')
    def test_redirect_to_main_page_by_constructor_button(self, driver):
        constructor_page = ConstructorPage(driver)

        constructor_page.load_login_page()
        time.sleep(1)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        constructor_page.wait_clickability_constructor_button()
        constructor_page.click_constructor_button()

        assert constructor_page.wait_url_to_be(urls.MAIN_PAGE_URL)

    @allure.title('Проверка, что клик в шапке по кнопке "Лента заказов" ведёт на ленту заказов')
    def test_redirect_to_feed_page_by_feed_button(self, driver):
        constructor_page = ConstructorPage(driver)

        constructor_page.load_login_page()
        time.sleep(1)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        constructor_page.wait_clickability_order_feed_button()
        constructor_page.click_order_feed_button()

        assert constructor_page.wait_url_to_be(urls.FEED_PAGE_URL)

    @allure.title('Проверка, что если кликнуть на ингредиент, появится всплывающее окно с деталями')
    def test_click_ingredient_popup_modal(self, driver):
        constructor_page = ConstructorPage(driver)

        constructor_page.load_main_page()
        time.sleep(1)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        constructor_page.wait_visibility_of_ingredients_cards()
        constructor_page.click_first_ingredient()

        assert constructor_page.wait_visibility_of_modal_with_ingredient_details()

    @allure.title('Проверка, что всплывающее окно закрывается кликом по крестику')
    def test_click_cross_closes_modal_window(self, driver):
        constructor_page = ConstructorPage(driver)

        constructor_page.load_main_page()
        time.sleep(1)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        constructor_page.wait_visibility_of_ingredients_cards()
        constructor_page.click_first_ingredient()
        constructor_page.wait_visibility_of_modal_with_ingredient_details()
        constructor_page.wait_visibility_of_cross_in_modal_window()
        constructor_page.click_cross_in_modal_window()

        assert constructor_page.wait_visibility_of_constructor_header()

    @allure.title('Проверка: при добавлении ингредиента {ingredient} в заказ счётчик этого ингредиента увеличивается')
    @pytest.mark.parametrize("ingredient, expected", [
        ("Флюоресцентная булка R2-D3", "2"),
        ("Соус Spicy-X", "1"),
        ("Мясо бессмертных моллюсков Protostomia", "1")])
    def test_ingredient_counter_increases(self, driver, ingredient, expected):
        constructor_page = ConstructorPage(driver)

        constructor_page.load_main_page()
        time.sleep(1)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        constructor_page.wait_visibility_of_ingredients_cards()
        constructor_page.drag_ingredient_to_constructor(ingredient)

        assert constructor_page.wait_text_presence_in_ingredient_counter(ingredient, expected)
