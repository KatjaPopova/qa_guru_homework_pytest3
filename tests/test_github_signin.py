import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

GITHUB_URL = "https://github.com/"

# DESKTOP: "Sign in" который виден на больших экранах (у него class содержит hiddenBelowLg)
DESKTOP_SIGNIN = (By.CSS_SELECTOR, 'header a[href="/login"][class*="hiddenBelowLg"]')

# MOBILE: "Sign in" который НЕ скрыт ниже LG (то есть виден на маленьких экранах)
MOBILE_SIGNIN = (By.CSS_SELECTOR, 'header a[href="/login"]:not([class*="hiddenBelowLg"])')

DESKTOP_TEST_SIZES = [
    (1400, 900),
    (1280, 720),
    pytest.param((390, 844), marks=pytest.mark.skip(reason="мобильный размер для десктопного теста"),
                 id="390x844_skip"),
    pytest.param((414, 896), marks=pytest.mark.skip(reason="мобильный размер для десктопного теста"),
                 id="414x896_skip"),
]


@pytest.mark.parametrize("size", DESKTOP_TEST_SIZES)
def test_github_signin_desktop_skip_mobile_v2(driver, size):
    width, height = size
    driver.set_window_size(width, height)
    driver.get(GITHUB_URL)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DESKTOP_SIGNIN)).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/login"))


DESKTOP_SIZES = [(1400, 900), (1280, 720)]
MOBILE_SIZES = [(390, 844), (414, 896)]


@pytest.mark.parametrize(
    "driver_with_window",
    DESKTOP_SIZES + MOBILE_SIZES,
    indirect=True
)
def test_github_signin_mobile_skip_desktop(driver_with_window):
    driver = driver_with_window

    width = driver.get_window_size()["width"]

    if width >= 768:
        pytest.skip("Пропускаем десктопную версию, этот тест предназначен для мобилки")

    driver.get(GITHUB_URL)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MOBILE_SIGNIN)).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/login"))


def test_github_signin_desktop_fixture(desktop_driver):
    driver = desktop_driver
    driver.get(GITHUB_URL)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DESKTOP_SIGNIN)).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/login"))


def test_github_signin_mobile_fixture(mobile_driver):
    driver = mobile_driver
    driver.get(GITHUB_URL)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MOBILE_SIGNIN)).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/login"))
