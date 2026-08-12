from selenium.webdriver.common.by import By
from pages.base_page import BasePage

import allure


class ConstructorPage(BasePage):

    # ---------------------------------------------------------------- #
    #  Конструктор (главная страница)                                  #

    CONSTRUCTOR_HEADER = (
        By.XPATH, "//h1[text()='Соберите бургер']")

    # все карточки ингредиентов (коллекция, find_elements)
    INGREDIENT_CARDS = (
        By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__')]")
    # первый ингредиент списка и его счётчик — гарантированно один элемент
    FIRST_INGREDIENT = (
        By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient__')])[1]")
    FIRST_INGREDIENT_COUNTER = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient_ingredient__')])[1]//p[contains(@class, 'counter_counter__num__')]",
    )

    # шаблон: (By.XPATH, ConstructorPage.INGREDIENT_BY_NAME.format('Краторная булка N-200i'))
    INGREDIENT_BY_NAME = "//a[contains(@class, 'BurgerIngredient_ingredient__')][.//p[text()='{}']]"
    INGREDIENT_COUNTER_BY_NAME = (
        "//a[contains(@class, 'BurgerIngredient_ingredient__')][.//p[text()='{}']]"
        "//p[contains(@class, 'counter_counter__num__')]")
    # СПРЯЧЕМ В СТАТИЧЕСКИЕ МЕТОДЫ:

    @staticmethod
    def ingredient_by_name(name):
        return (By.XPATH, ConstructorPage.INGREDIENT_BY_NAME.format(name))

    @staticmethod
    def ingredient_counter_by_name(name):
        return (By.XPATH, ConstructorPage.INGREDIENT_COUNTER_BY_NAME.format(name))

    # зона сборки бургера — это <section>, именно на ней висит drop-таргет react-dnd
    CONSTRUCTOR_DROP_ZONE = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket__']")
    # итоговая цена заказа (не счётчик ингредиента!)
    ORDER_TOTAL_PRICE = (By.CSS_SELECTOR, "[class*='BurgerConstructor_basket__totalContainer__'] p")
    # у неавторизованного пользователя текст кнопки — «Войти в аккаунт»
    ORDER_BUTTON = (By.CSS_SELECTOR, "button[class*='button_button_size_large__']")
    # признак того, что пользователь авторизован и заказ можно оформлять
    ORDER_BUTTON_AUTHORIZED = (By.XPATH, "//button[text()='Оформить заказ']")

    # ---------------------------------------------------------------- #
    #  Модальные окна                                                   #
    #  В DOM всегда висят закрытые модалки, поэтому «открытость»        #
    #  определяется только классом со звёздочкой ("содержит"): Modal_modal_opened__.           #
    #  Контентная модалка — <section>, прелоадер — <div>.               #

    MODAL = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened__']")
    MODAL_INGREDIENT_TITLE = (
        By.XPATH, "//section[contains(@class, 'Modal_modal_opened__')]//h2[text()='Детали ингредиента']")
    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened__')]//button[contains(@class, 'Modal_modal__close__')]")
    ORDER_NUMBER = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened__')]//h2[contains(@class, 'Modal_modal__title_shadow__')]")
    # прелоадер, который показывается, пока заказ оформляется
    LOADING_MODAL = (By.CSS_SELECTOR, "div[class*='Modal_modal_opened__']")

    # @allure.step('Кликаем на кнопку "Заказать" в шапке')
    def wait_visibility_of_ingredients_cards(self):
        self.wait_visibility(self.INGREDIENT_CARDS)

    # @allure.step('Кликаем на кнопку "Заказать" в шапке')
    def click_first_ingredient(self):
        self.click(self.FIRST_INGREDIENT)

    # @allure.step('Кликаем на кнопку "Заказать" в шапке')
    def wait_visibility_of_modal_with_ingredient_details(self):
        return self.wait_visibility(self.MODAL_INGREDIENT_TITLE)

    # @allure.step('Кликаем на кнопку "Заказать" в шапке')
    def wait_visibility_of_cross_in_modal_window(self):
        self.wait_visibility(self.MODAL_CLOSE_BUTTON)

    # @allure.step('Кликаем на кнопку "Заказать" в шапке')
    def click_cross_in_modal_window(self):
        self.click(self.MODAL_CLOSE_BUTTON)

    # @allure.step('Кликаем на кнопку "Заказать" в шапке')
    def wait_visibility_of_constructor_header(self):
        return self.wait_visibility(self.CONSTRUCTOR_HEADER)

    DND_SCRIPT = """
    const [source, target] = arguments;
    const dataTransfer = new DataTransfer();
    const options = {bubbles: true, cancelable: true, dataTransfer: dataTransfer};

    source.dispatchEvent(new DragEvent('dragstart', options));
    target.dispatchEvent(new DragEvent('dragenter', options));
    target.dispatchEvent(new DragEvent('dragover', options));
    target.dispatchEvent(new DragEvent('drop', options));
    source.dispatchEvent(new DragEvent('dragend', options));
    """

    @allure.step('Перетаскиваем ингредиент {name} в конструктор')
    def drag_ingredient_to_constructor(self, name):
        source = self.driver.find_element(*self.ingredient_by_name(name))
        target = self.driver.find_element(*self.CONSTRUCTOR_DROP_ZONE)
        self.driver.execute_script(self.DND_SCRIPT, source, target)

    @allure.step('Ждём появления цифр в счётчике булки {name}')
    def wait_text_presence_in_ingredient_counter(self, name, number):
        return self.wait_text_presence(self.ingredient_counter_by_name(name), number)

    @allure.step('Перетаскиваем первую булку в конструктор')
    def drag_first_bun_to_constructor(self):
        source = self.driver.find_element(*self.ingredient_by_name("Флюоресцентная булка R2-D3"))
        target = self.driver.find_element(*self.CONSTRUCTOR_DROP_ZONE)
        self.driver.execute_script(self.DND_SCRIPT, source, target)

    @allure.step('Ждём появления количества булок в счётчике первой булки - 2 шт.: нижняя и верхняя')
    def wait_text_presence_in_first_bun_counter(self):
        self.wait_text_presence(self.ingredient_counter_by_name("Флюоресцентная булка R2-D3"), "2")

    @allure.step('Кликаем на кнопку "Оформить заказ"')
    def click_order_button_under_constructor(self):
        self.click(self.ORDER_BUTTON_AUTHORIZED)

    @allure.step('Ждём, когда появится прелоадер')
    def wait_preloader_visibility(self):
        self.wait_visibility(self.LOADING_MODAL)

    @allure.step('Ждём, когда исчезнет прелоадер')
    def wait_preloader_invisibility(self):
        self.wait_invisibility(self.LOADING_MODAL)

    @allure.step('Получаем текст номера «идентификатор заказа»')
    def get_text_of_order_number(self):
        element = self.wait_visibility(self.ORDER_NUMBER)
        return element.text
