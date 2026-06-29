import random

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC

from credentials import BASE_URL
from test.locators import LoginPageLocators


SCROLL_TO_CENTER_SCRIPT = "arguments[0].scrollIntoView({block: 'center'});"


def skip_if_empty(required_values, message, pytest_module):
    if not all(required_values):
        pytest_module.skip(message)


def open_login_form(wait):
    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)
    ).click()


def login(wait, email, password):
    open_login_form(wait)
    email_input = wait.until(
        EC.element_to_be_clickable(LoginPageLocators.EMAIL_INPUT)
    )
    email_input.clear()
    email_input.send_keys(email)

    password_input = wait.until(
        EC.element_to_be_clickable(LoginPageLocators.PASSWORD_INPUT)
    )
    password_input.clear()
    password_input.send_keys(password)

    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.LOGIN_SUBMIT_BUTTON)
    ).click()


def open_registration_form(wait):
    open_login_form(wait)
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


def fill_registration_email(wait, email):
    email_input = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
    )
    email_input.clear()
    email_input.send_keys(email)


def click_create_account(wait):
    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.CREATE_ACCOUNT_BUTTON)
    ).click()


def open_post_ad_form(wait):
    try:
        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.MODAL_POST_ADD)
        ).click()
    except StaleElementReferenceException:
        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.MODAL_POST_ADD)
        ).click()


def fill_product_form(driver, wait, title, description, price):
    product_name = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.PRODUCT_NAME)
    )
    product_name.send_keys(title)

    category_dropdown = wait.until(
        EC.element_to_be_clickable(LoginPageLocators.ADD_CATEGORY)
    )
    driver.execute_script(SCROLL_TO_CENTER_SCRIPT, category_dropdown)
    category_dropdown.click()
    random.choice(visible_dropdown_options(driver, wait)).click()

    city_dropdown = wait.until(
        EC.element_to_be_clickable(LoginPageLocators.CITY_DROPDOWN)
    )
    driver.execute_script(SCROLL_TO_CENTER_SCRIPT, city_dropdown)
    city_dropdown.click()
    random.choice(visible_dropdown_options(driver, wait)).click()

    product_description = wait.until(
        EC.visibility_of_element_located(
            LoginPageLocators.PRODUCT_DESCRIPTION
        )
    )
    product_description.send_keys(description)

    price_input = wait.until(
        EC.element_to_be_clickable(LoginPageLocators.PRICE_INPUT)
    )
    price_input.send_keys(price)

    condition_radio = random.choice(wait.until(radio_options_available))
    driver.execute_script('arguments[0].click();', condition_radio)
    wait.until(lambda browser: condition_radio.is_selected())

    return product_name, price_input, condition_radio


def publish_ad(wait):
    wait.until(
        EC.element_to_be_clickable(LoginPageLocators.PUBLISH_BUTTON)
    ).click()


def visible_dropdown_options(driver, wait):
    return wait.until(
        lambda browser: [
            option for option in browser.find_elements(
                *LoginPageLocators.DROPDOWN_OPTIONS
            )
            if option.is_displayed()
            and option.is_enabled()
            and option.text.strip()
        ]
    )


def radio_options_available(driver):
    radio_options = driver.find_elements(*LoginPageLocators.CONDITION_RADIO)
    return radio_options if radio_options else False


def is_user_authorized(wait):
    try:
        user_name = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        avatar = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )
        post_button = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.POST_ADD_BUTTON)
        )
        return all(
            element.is_displayed()
            for element in (user_name, avatar, post_button)
        )
    except TimeoutException:
        return False


def is_user_logged_out(wait):
    try:
        user_name_hidden = wait.until(
            EC.invisibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        avatar_hidden = wait.until(
            EC.invisibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )
        login_button = wait.until(
                EC.visibility_of_element_located(
                    LoginPageLocators.LOGIN_REG_BUTTON
                )
        )
        return (
            user_name_hidden
            and avatar_hidden
            and login_button.is_displayed()
        )
    except TimeoutException:
        return False


def is_posted_ad_visible(wait, ad_title):
    try:
        wait.until(EC.url_to_be(BASE_URL))
        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.USER_AVATAR)
        ).click()
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.MY_ADS_TITLE)
        )
        return wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.created_ad_title(ad_title)
            )
        ).is_displayed()
    except TimeoutException:
        return False


def wait_error_message(wait):
    return wait.until(
        EC.visibility_of_element_located(LoginPageLocators.ERROR_MESSAGE)
    )


def is_registration_error_shown(wait):
    try:
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
        return error.is_displayed() and all(
            is_field_highlighted_red(el)
            for el in (email_el, pass_el, confirm_el)
        )
    except TimeoutException:
        return False


def is_field_highlighted_red(element):
    for node in [
        element,
        *element.find_elements(*LoginPageLocators.FIELD_ANCESTORS)
    ]:
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
