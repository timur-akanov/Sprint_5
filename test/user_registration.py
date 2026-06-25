from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD


def main():
    email = EMAIL
    password = PASSWORD
    if not email or not password:
        print('Ошибка: заполните EMAIL и PASSWORD в credentials.py')
        return

    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get('https://qa-desk.education-services.ru/')
        wait = WebDriverWait(driver, 15)

        # 1. Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)).click()

        # 2. Нажать кнопку «Нет аккаунта»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.REG_NO_ACCOUNT)).click()

        # 3. Заполнить форму регистрации
        email_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
        try:
            email_input.send_keys(email)
        except StaleElementReferenceException:
            email_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
            email_input.send_keys(email)

        time.sleep(1)
        password_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
        try:
            password_input.send_keys(password)
        except StaleElementReferenceException:
            password_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
            password_input.send_keys(password)

        time.sleep(1)
        password_confirm = wait.until(EC.visibility_of_element_located(LoginPageLocators.SUBMIT_PASSWORD_BUTTON))
        try:
            password_confirm.send_keys(password)
        except StaleElementReferenceException:
            password_confirm = wait.until(EC.visibility_of_element_located(LoginPageLocators.SUBMIT_PASSWORD_BUTTON))
            password_confirm.send_keys(password)

        # 4. Нажать кнопку «Создать аккаунт»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.CREATE_ACCOUNT_BUTTON)).click()

        # 5. Проверить результат: переход на главную страницу и видимость имени User
        time.sleep(3)
        success = False
        current = driver.current_url.lower()
        if 'qa-desk.education-services.ru' in current:
            try:
                driver.find_element('xpath', "//*[contains(text(), 'User')]")
                success = True
            except Exception:
                success = False

        if success:
            print('Регистрация прошла: пользователь User отображается на главной странице.')
        else:
            print('Регистрация выполнена, но не удалось найти имя User на странице.')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
