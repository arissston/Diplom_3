from selenium.webdriver.common.by import By
from pages.base_page import BasePage

import allure


class FeedPage(BasePage):

    # ---------------------------------------------------------------- #
    #  Лента заказов /feed                                             #

    FEED_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")
    COMPLETED_ALL_TIME_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'OrderFeed_number__')]",
    )
    COMPLETED_TODAY_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'OrderFeed_number__')]",
    )
    # колонка «В работе» (у вёрстки обманчивое имя класса: orderListReady — это именно «В работе»)
    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady__')]/li")
    IN_PROGRESS_EMPTY_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderListReady__')]/li[normalize-space(.)='Все текущие заказы готовы!']",
    )
    # шаблон: номер в ленте выводится с ведущим нулём -> .format(394552) ищет «0394552»
    IN_PROGRESS_ORDER_BY_NUMBER = "//ul[contains(@class, 'OrderFeed_orderListReady__')]/li[normalize-space(.)='0{}']"

    @staticmethod
    def in_progress_order_by_number(number):
        return (By.XPATH, FeedPage.IN_PROGRESS_ORDER_BY_NUMBER.format(number))

    @allure.step('Ждём видимость и получаем текст счётчика «Выполнено за всё время»')
    def get_text_of_completed_all_time_counter(self):
        element = self.wait_visibility(self.COMPLETED_ALL_TIME_COUNTER)
        return element.text

    @allure.step('Ждём видимость и получаем текст счётчика «Выполнено за сегодня»')
    def get_text_of_completed_today_counter(self):
        element = self.wait_visibility(self.COMPLETED_TODAY_COUNTER)
        return element.text

    @allure.step('Скроллим до счётчика «Выполнено за сегодня»')
    def scroll_to_completed_today_counter(self):
        self.scroll(self.COMPLETED_TODAY_COUNTER)

    @allure.step('Ждём появления номера заказа {number} в разделе «В работе»')
    def wait_text_presence_inside_the_in_progress_orders(self, number):
        return self.wait_text_presence(self.in_progress_order_by_number(number), number)
