from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD



def login(): 
    email = EMAIL
    password = PASSWORD
    if not email or not password:
        print('Ошибка: заполните EMAIL и PASSWORD в credentials.py')
        return

    try:
        dr = webdriver.Chrome()
        dr.maximize_window()
        dr.get('https://qa-desk.education-services.ru/')
        wait = WebDriverWait(dr, 10)
        # 1. Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)).click()
        assert dr.current_url.lower() == 'https://qa-desk.education-services.ru/login', "Не удалось перейти на страницу входа"
        # 2. Ввод пароля и email
        email_input = wait.until(EC.element_to_be_clickable(LoginPageLocators.EMAIL_INPUT))
        email_input.send_keys(email)
        assert email_input.get_attribute('value') == email, "Email не был введен корректно"
        password_input = wait.until(EC.element_to_be_clickable(LoginPageLocators.PASSWORD_INPUT))
        password_input.send_keys(password)
        assert password_input.get_attribute('value') == password, "Пароль не был введен корректно"
        # 3. Нажать кнопку «Войти»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)).click()
                # 5. Проверить результат: переход на главную страницу и видимость имени User
        time.sleep(3)
        success = False
        current = dr.current_url.lower()
        if 'qa-desk.education-services.ru' in current:
            try:
                dr.find_element('xpath', "//*[contains(text(), 'User')]")
                success = True
            except Exception:
                success = False

        if success:
            print('Пользователь User отображается на главной странице.')
        else:
            print('Не удалось найти имя User на странице.')
    
    finally:
        dr.quit()

    time.sleep(3)  # Задержка для визуальной проверки результатов перед закрытием браузера
if __name__ == '__main__':
    login()