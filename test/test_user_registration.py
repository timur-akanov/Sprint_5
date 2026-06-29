import uuid

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from credentials import (
    EMAIL,
    PASSWORD,
    EXISTING_EMAIL,
    EXISTING_PASSWORD,
    BASE_URL,
)
from test.helpers import (
    click_create_account,
    fill_registration_email,
    fill_registration_form,
    is_registration_error_shown,
    is_user_authorized,
    open_registration_form,
    skip_if_empty,
)


class TestUserRegistration:
    def test_user_can_register_successfully(self, driver):
        skip_if_empty(
            (PASSWORD,),
            'Заполните PASSWORD в credentials.py',
            pytest
        )
        email = f'autotest_{uuid.uuid4().hex[:8]}@mail.ru'

        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        open_registration_form(wait)
        fill_registration_form(wait, email, PASSWORD)
        click_create_account(wait)

        assert is_user_authorized(wait), (
            'После регистрации не отображаются элементы пользователя'
        )

    def test_invalid_email_registration_shows_error(self, driver):
        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        open_registration_form(wait)
        fill_registration_email(wait, 'invalid-email')
        click_create_account(wait)

        assert is_registration_error_shown(wait), (
            'Поля при некорректном email не выделены как ошибочные'
        )

    def test_existing_user_registration_shows_error(self, driver):
        email = EMAIL or EXISTING_EMAIL
        password = PASSWORD or EXISTING_PASSWORD
        skip_if_empty(
            (email, password),
            'Заполните EMAIL/PASSWORD для существующего пользователя',
            pytest
        )

        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        open_registration_form(wait)
        fill_registration_form(wait, email, password)
        click_create_account(wait)

        assert is_registration_error_shown(wait), (
            'Поля при регистрации существующего пользователя не выделены'
        )
