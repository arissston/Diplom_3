import pytest
from selenium import webdriver


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

    else:
        driver = webdriver.Firefox(options=webdriver.FirefoxOptions())
        driver.maximize_window()

    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)

    yield driver
    driver.quit()
