from selenium.webdriver.common.by import By
from pages.base_page import BasePage

import allure
from data import USER


class LoginPage(BasePage):
    # ---------------------------------------------------------------- #
    #  Страница входа /login                                           #

    EMAIL_INPUT = (
        By.XPATH, "//div[contains(@class, 'input_type_text')]//input[@name='name']")
    PASSWORD_INPUT = (
        By.XPATH, "//div[contains(@class, 'input_type_password')]//input[@type='password']")
    LOGIN_SUBMIT_BUTTON = (
        By.XPATH, "//button[text()='Войти']")

    @allure.step('Логинимся: Заполняем данные для логина (заранее созданный пользователь)и кликаем "Войти"')
    def login_user(self):
        self.fill(self.EMAIL_INPUT, USER["email"])
        self.fill(self.PASSWORD_INPUT, USER["password"])
        self.click(self.LOGIN_SUBMIT_BUTTON)
