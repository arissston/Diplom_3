from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import urls
import allure


class BasePage:

    TIMEOUT = 15

    # ---------------------------------------------------------------- #
    #  Шапка сайта (присутствует на всех страницах)                    #

    CONSTRUCTOR_LINK = (
        By.XPATH, "//a[contains(@class, 'AppHeader_header__link__')][.//p[text()='Конструктор']]")
    ORDER_FEED_LINK = (
        By.XPATH, "//a[contains(@class, 'AppHeader_header__link__')][.//p[text()='Лента Заказов']]")
    PERSONAL_ACCOUNT_LINK = (
        By.XPATH, "//a[contains(@class, 'AppHeader_header__link__')][.//p[text()='Личный Кабинет']]")

    def __init__(self, driver):
        self.driver = driver

    @allure.step('Открываем страницу {url}')
    def open_page(self, url):
        self.driver.get(url)

    @allure.step('Открываем главную страницу')
    def load_main_page(self):
        self.open_page(urls.MAIN_PAGE_URL)

    @allure.step('Открываем страницу логина')
    def load_login_page(self):
        self.open_page(urls.LOGIN_PAGE_URL)

    @allure.step('Открываем страницу ленты заказов')
    def load_feed_page(self):
        self.open_page(urls.FEED_PAGE_URL)

    @allure.step('Кликаем на элемент по локатору: "{locator}"')
    def click(self, locator):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(locator))
        element.click()

    @allure.step('Кликаем на кнопку: "Конструктор"')
    def click_constructor_button(self):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self.CONSTRUCTOR_LINK))
        element.click()

    @allure.step('Кликаем на кнопку: "Лента заказов"')
    def click_order_feed_button(self):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self.ORDER_FEED_LINK))
        element.click()

    @allure.step('Заполняем поле элемента по локатору: "{locator}" текстом "{text}"')
    def fill(self, locator, text):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    @allure.step('Ждём появления текста по локатору: "{locator}"')
    def wait_text_presence(self, locator, text):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.text_to_be_present_in_element(locator, text))
        return element

    @allure.step('Ждём видимость элемента по локатору: "{locator}"')
    def wait_visibility(self, locator):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(locator))
        return element

    @allure.step('Ждём видимость кнопки: "Конструктор"')
    def wait_visibility_constructor_button(self):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.CONSTRUCTOR_LINK))
        return element

    @allure.step('Ждём кликабельности кнопки: "Конструктор"')
    def wait_clickability_constructor_button(self):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self.CONSTRUCTOR_LINK))
        return element

    @allure.step('Ждём видимость кнопки: "Лента заказов"')
    def wait_visibility_order_feed_button(self):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.ORDER_FEED_LINK))
        return element

    @allure.step('Ждём кликабельности кнопки: "Лента заказов"')
    def wait_clickability_order_feed_button(self):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self.ORDER_FEED_LINK))
        return element

    @allure.step('Скроллим до элемента по локатору: "{locator}"')
    def scroll(self, locator):
        element = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element

    @allure.step('Ждём, пока URL станет "{url}"')
    def wait_url_to_be(self, url):
        return WebDriverWait(self.driver, self.TIMEOUT).until(EC.url_to_be(url))

    @allure.step('Ждём, что элемент по локатору: "{locator}" - исчез')
    def wait_invisibility(self, locator):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.invisibility_of_element_located(locator))
