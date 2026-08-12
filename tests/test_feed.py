from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage

import allure
import urls
import time

# Раздел «Лента заказов»
#
# Проверяем:
#
# - при создании нового заказа счётчик «Выполнено за всё время» увеличивается;
# - при создании нового заказа счётчик «Выполнено за сегодня» увеличивается;
# - после оформления заказа его номер появляется в разделе «В работе».


class TestFeed:

    @allure.title('Проверка, что при создании нового заказа счётчик «Выполнено за всё время» увеличивается')
    def test_completed_all_time_counter_in_feed_increases_after_new_order(self, driver):
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)
        constructor_page = ConstructorPage(driver)

        login_page.load_login_page()
        login_page.login_user()
        login_page.wait_url_to_be(urls.MAIN_PAGE_URL)

        feed_page.click_order_feed_button()
        feed_page.wait_url_to_be(urls.FEED_PAGE_URL)

        counter = feed_page.get_text_of_completed_all_time_counter()
        counter_expected = int(counter) + 1

        feed_page.click_constructor_button()
        feed_page.wait_url_to_be(urls.MAIN_PAGE_URL)

        time.sleep(2)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        constructor_page.drag_first_bun_to_constructor()
        constructor_page.wait_text_presence_in_first_bun_counter()

        constructor_page.click_order_button_under_constructor()

        constructor_page.wait_preloader_visibility()
        constructor_page.wait_preloader_invisibility()

        constructor_page.click_cross_in_modal_window()

        time.sleep(2)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут

        feed_page.click_order_feed_button()
        feed_page.wait_url_to_be(urls.FEED_PAGE_URL)
        time.sleep(2)  # счётчик не успевает обновиться - ставим принудительную задержку

        counter_final = int(feed_page.get_text_of_completed_all_time_counter())

        assert counter_final == counter_expected

    @allure.title('Проверка, что при создании нового заказа счётчик «Выполнено за сегодня» увеличивается')
    def test_completed_today_counter_in_feed_increases_after_new_order(self, driver):
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)
        constructor_page = ConstructorPage(driver)

        login_page.load_login_page()
        login_page.login_user()
        login_page.wait_url_to_be(urls.MAIN_PAGE_URL)

        time.sleep(2)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут
        feed_page.click_order_feed_button()
        feed_page.wait_url_to_be(urls.FEED_PAGE_URL)

        feed_page.scroll_to_completed_today_counter()

        counter = feed_page.get_text_of_completed_today_counter()
        counter_expected = int(counter) + 1

        feed_page.click_constructor_button()
        feed_page.wait_url_to_be(urls.MAIN_PAGE_URL)

        constructor_page.drag_first_bun_to_constructor()
        constructor_page.wait_text_presence_in_first_bun_counter()

        constructor_page.click_order_button_under_constructor()

        constructor_page.wait_preloader_visibility()
        constructor_page.wait_preloader_invisibility()

        constructor_page.click_cross_in_modal_window()

        time.sleep(2)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут

        feed_page.click_order_feed_button()
        feed_page.wait_url_to_be(urls.FEED_PAGE_URL)

        feed_page.scroll_to_completed_today_counter()
        time.sleep(2)  # счётчик не успевает обновиться - ставим принудительную задержку

        counter_final = int(feed_page.get_text_of_completed_today_counter())

        assert counter_final == counter_expected

    @allure.title('Проверка, что после оформления заказа его номер появляется в разделе «В работе»')
    def test_order_number_appears_inside_the_in_progress_orders_after_new_order(self, driver):
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)
        constructor_page = ConstructorPage(driver)

        login_page.load_login_page()
        login_page.login_user()
        login_page.wait_url_to_be(urls.MAIN_PAGE_URL)

        constructor_page.wait_visibility_of_ingredients_cards()
        constructor_page.drag_first_bun_to_constructor()
        constructor_page.wait_text_presence_in_first_bun_counter()

        constructor_page.click_order_button_under_constructor()

        constructor_page.wait_preloader_visibility()
        constructor_page.wait_preloader_invisibility()

        order_number = constructor_page.get_text_of_order_number()

        constructor_page.click_cross_in_modal_window()

        time.sleep(2)  # в Firefox не успевают исчезнуть оверлеи, нужен принудительный таймаут

        feed_page.click_order_feed_button()
        feed_page.wait_url_to_be(urls.FEED_PAGE_URL)

        assert feed_page.wait_text_presence_inside_the_in_progress_orders(order_number)
