from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD, EXISTING_EMAIL, EXISTING_PASSWORD, BASE_URL


def open_registration_form(wait):
    wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(LoginPageLocators.REG_NO_ACCOUNT)).click()


def fill_registration_form(wait, email, password, confirm=None):
    email_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
    try:
        email_input.clear()
        email_input.send_keys(email)
    except StaleElementReferenceException:
        email_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)

    password_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
    password_input.clear()
    password_input.send_keys(password)

    confirm_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.SUBMIT_PASSWORD_BUTTON))
    confirm_input.clear()
    confirm_input.send_keys(confirm or password)


def click_create_account(wait):
    wait.until(EC.element_to_be_clickable(LoginPageLocators.CREATE_ACCOUNT_BUTTON)).click()


def find_error_message(driver):
    try:
        el = driver.find_element(By.XPATH, "//*[contains(text(), 'Ошибка')]")
        return el.text
    except Exception:
        return None


def is_field_highlighted_red(element):
    cls = element.get_attribute('class') or ''
    aria = element.get_attribute('aria-invalid') or ''
    style = element.get_attribute('style') or ''
    if 'error' in cls.lower() or 'invalid' in cls.lower() or aria == 'true' or 'red' in style.lower():
        return True
    return False


def register_success():
    if not EMAIL or not PASSWORD:
        print('Пропускаю успешную регистрацию — EMAIL/PASSWORD не заданы в credentials.py')
        return

    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        open_registration_form(wait)
        fill_registration_form(wait, EMAIL, PASSWORD)
        click_create_account(wait)

        time.sleep(2)
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'User')]")
            print('Успешная регистрация: пользователь отображается как User')
        except Exception:
            print('Провал: при регистрации пользователь не отобразился как User')
    finally:
        driver.quit()


def register_invalid_email(invalid_email):
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        open_registration_form(wait)
        fill_registration_form(wait, invalid_email, 'SomePass123')
        click_create_account(wait)

        time.sleep(1)
        err = find_error_message(driver)
        email_el = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
        pass_el = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
        confirm_el = wait.until(EC.visibility_of_element_located(LoginPageLocators.SUBMIT_PASSWORD_BUTTON))
        highlighted = any([is_field_highlighted_red(el) for el in (email_el, pass_el, confirm_el)])

        if err and highlighted:
            print('ОК: при некорректном email поля выделены красным и показана ошибка.')
        else:
            print(f'FAIL: ошибка не найдена (err={err}, highlighted={highlighted})')
    finally:
        driver.quit()


def register_existing_user():
    email = EXISTING_EMAIL or EMAIL
    password = EXISTING_PASSWORD or PASSWORD
    if not email or not password:
        print('Пропускаю проверку существующего пользователя — EXISTING_EMAIL/EXISTING_PASSWORD не заданы')
        return

    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        open_registration_form(wait)
        fill_registration_form(wait, email, password)
        click_create_account(wait)

        time.sleep(1)
        err = find_error_message(driver)
        email_el = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
        pass_el = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
        confirm_el = wait.until(EC.visibility_of_element_located(LoginPageLocators.SUBMIT_PASSWORD_BUTTON))
        highlighted = any([is_field_highlighted_red(el) for el in (email_el, pass_el, confirm_el)])

        if err and highlighted:
            print('ОК: регистрация существующего пользователя выдала ошибку и поля выделены красным.')
        else:
            print(f'FAIL: не обнаружена ожидаемая ошибка (err={err}, highlighted={highlighted})')
    finally:
        driver.quit()


def main():
    if len(sys.argv) < 2:
        print('Использование: python user_registration.py [success|invalid_email|existing_user] [email]')
        return

    cmd = sys.argv[1]
    if cmd == 'success':
        register_success()
    elif cmd == 'invalid_email':
        invalid = sys.argv[2] if len(sys.argv) > 2 else 'invalid-email'
        register_invalid_email(invalid)
    elif cmd == 'existing_user':
        register_existing_user()
    else:
        print('Неизвестная команда')


if __name__ == '__main__':
    main()
