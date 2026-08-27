import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

GITHUB_URL = "https://github.com/"

LOGIN_FIELD = (By.ID, "login_field")
PASSWORD_FIELD = (By.ID, "password")

DESKTOP_SIGNIN = (By.CSS_SELECTOR, 'header a[href="/login"][class*="hiddenBelowLg"]')
MOBILE_SIGNIN = (By.CSS_SELECTOR, 'header a[href="/login"]:not([class*="hiddenBelowLg"])')


def assert_login_page(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LOGIN_FIELD))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(PASSWORD_FIELD))

    assert driver.find_element(*LOGIN_FIELD).is_displayed()
    assert driver.find_element(*PASSWORD_FIELD).is_displayed()


DESKTOP_TEST_SIZES = [
    (1400, 900),
    (1280, 720),
    pytest.param((390, 844), marks=pytest.mark.skip(reason="мобильный размер для десктопного теста"),
                 id="390x844_skip"),
    pytest.param((414, 896), marks=pytest.mark.skip(reason="мобильный размер для десктопного теста"),
                 id="414x896_skip"),
]

@pytest.mark.parametrize("size", DESKTOP_TEST_SIZES)
def test_github_signin_desktop_skip_mobile(driver, size):
    driver.set_window_size(*size)
    driver.get(GITHUB_URL)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DESKTOP_SIGNIN)).click()

    assert_login_page(driver)



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

    assert_login_page(driver)


def test_github_signin_desktop_fixture(desktop_driver):
    driver = desktop_driver
    driver.get(GITHUB_URL)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DESKTOP_SIGNIN)).click()

    assert_login_page(driver)


def test_github_signin_mobile_fixture(mobile_driver):
    driver = mobile_driver
    driver.get(GITHUB_URL)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MOBILE_SIGNIN)).click()

    assert_login_page(driver)
