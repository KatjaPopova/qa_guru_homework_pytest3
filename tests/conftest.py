import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def _make_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


@pytest.fixture
def driver():
    driver = _make_driver()
    yield driver
    driver.quit()


@pytest.fixture
def driver_with_window(driver, request):
    width, height = request.param
    driver.set_window_size(width, height)
    return driver


# Дополнительно: две разные фикстуры для каждого теста (пункт 3 задания)
@pytest.fixture
def desktop_driver(driver):
    driver.set_window_size(1400, 900)
    return driver


@pytest.fixture
def mobile_driver(driver):
    driver.set_window_size(390, 844)
    return driver
