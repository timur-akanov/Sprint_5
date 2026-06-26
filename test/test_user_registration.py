import uuid

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginPageLocators
from credentials import (
    EMAIL,
    PASSWORD,
    EXISTING_EMAIL,
    EXISTING_PASSWORD,
    BASE_URL,
)


def open_registration_form(wait):
    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)
    ).click()
    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.REG_NO_ACCOUNT)
    ).click()


def fill_registration_form(wait, email, password, confirm=None):
    email_input = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
    )
    try:
        email_input.clear()
        email_input.send_keys(email)
    except StaleElementReferenceException:
        email_input = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(email)

    password_input = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
    )
    password_input.clear()
    password_input.send_keys(password)

    confirm_input = wait.until(
        EC.visibility_of_element_located(
            LoginPageLocators.SUBMIT_PASSWORD_BUTTON
        )
    )
    confirm_input.clear()
    confirm_input.send_keys(confirm or password)


def click_create_account(wait):
    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.CREATE_ACCOUNT_BUTTON)
    ).click()


def wait_error_message(wait):
    error_locator = (By.XPATH, "//*[contains(text(), 'Ошибка')]")
    return wait.until(EC.visibility_of_element_located(error_locator))


def assert_user_is_authorized(driver, wait):
    user_name = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.USER_NAME)
    )
    avatar = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.USER_AVATAR)
    )
    post_button = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.POST_ADD_BUTTON)
    )

    assert user_name.is_displayed(), 'Имя User не отображается в шапке'
    assert avatar.is_displayed(), 'Аватар пользователя не отображается'
    assert post_button.is_displayed(), (
        'Кнопка Разместить объявление не отображается'
    )


def is_field_highlighted_red(element):
    for node in [element, *element.find_elements(By.XPATH, './ancestor::*')]:
        cls = node.get_attribute('class') or ''
        aria = node.get_attribute('aria-invalid') or ''
        style = node.get_attribute('style') or ''
        border_color = element.parent.execute_script(
            'return getComputedStyle(arguments[0]).borderColor;',
            node
        )
        color_markers = ('rgb(255', 'rgb(204', 'rgb(220', 'red')
        if (
            'error' in cls.lower()
            or 'invalid' in cls.lower()
            or aria == 'true'
            or 'red' in style.lower()
            or any(marker in border_color.lower() for marker in color_markers)
        ):
            return True
    return False


class TestUserRegistration:
    def test_user_can_register_successfully(self, driver):
        assert PASSWORD, 'Заполните PASSWORD в credentials.py'
        email = f'autotest_{uuid.uuid4().hex[:8]}@mail.ru'

        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        open_registration_form(wait)
        fill_registration_form(wait, email, PASSWORD)
        click_create_account(wait)

        assert_user_is_authorized(driver, wait)

    def test_invalid_email_registration_shows_error(self, driver):
        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        open_registration_form(wait)
        email_el = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
        )
        email_el.clear()
        email_el.send_keys('invalid-email')
        click_create_account(wait)

        error = wait_error_message(wait)
        pass_el = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
        )
        confirm_el = wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.SUBMIT_PASSWORD_BUTTON
            )
        )
        highlighted = all(
            is_field_highlighted_red(el)
            for el in (email_el, pass_el, confirm_el)
        )

        assert error.is_displayed(), 'Ошибка под полем Email не отображается'
        assert highlighted, (
            'Поля при некорректном email не выделены как ошибочные'
        )

    def test_existing_user_registration_shows_error(self, driver):
        email = EMAIL or EXISTING_EMAIL
        password = PASSWORD or EXISTING_PASSWORD
        assert email and password, (
            'Заполните EMAIL/PASSWORD для существующего пользователя'
        )

        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        open_registration_form(wait)
        fill_registration_form(wait, email, password)
        click_create_account(wait)

        error = wait_error_message(wait)
        email_el = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
        )
        pass_el = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
        )
        confirm_el = wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.SUBMIT_PASSWORD_BUTTON
            )
        )
        highlighted = all(
            is_field_highlighted_red(el)
            for el in (email_el, pass_el, confirm_el)
        )

        assert error.is_displayed(), (
            'Ошибка при регистрации существующего пользователя не отображается'
        )
        assert highlighted, (
            'Поля при регистрации существующего пользователя не выделены'
        )
