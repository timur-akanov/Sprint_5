import pytest
from selenium.webdriver.support.ui import WebDriverWait
from credentials import EMAIL, PASSWORD, BASE_URL
from test.helpers import is_user_authorized, login, skip_if_empty


class TestLoginUser:
    def test_user_can_login(self, driver):
        skip_if_empty(
            (EMAIL, PASSWORD),
            'Заполните EMAIL и PASSWORD в credentials.py',
            pytest
        )

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)
        login(wait, EMAIL, PASSWORD)

        assert is_user_authorized(wait), (
            'После входа не отображаются элементы авторизованного пользователя'
        )
