import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test.locators import LoginPageLocators
from credentials import EMAIL, PASSWORD, BASE_URL
from test.helpers import is_user_logged_out, login, skip_if_empty


class TestLogoutUser:
    def test_user_can_logout(self, driver):
        skip_if_empty(
            (EMAIL, PASSWORD),
            'Заполните EMAIL и PASSWORD в credentials.py',
            pytest
        )

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)
        login(wait, EMAIL, PASSWORD)
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGOUT_BUTTON)
        ).click()

        assert is_user_logged_out(wait), (
            'После выхода не отображается состояние '
            'неавторизованного пользователя'
        )
