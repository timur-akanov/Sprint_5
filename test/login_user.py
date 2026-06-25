from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD, BASE_URL


def login():
    email = EMAIL
    password = PASSWORD
    if not email or not password:
        print('Ошибка: заполните EMAIL и PASSWORD в credentials.py')
        return

    dr = webdriver.Chrome()
    try:
        dr.maximize_window()
        dr.get(BASE_URL)
        wait = WebDriverWait(dr, 30)
        # 1. Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)).click()
        # Переход на страницу логина может быть асинхронным
        time.sleep(1)
        # 2. Ввод пароля и email
        email_input = wait.until(EC.element_to_be_clickable(LoginPageLocators.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        password_input = wait.until(EC.element_to_be_clickable(LoginPageLocators.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)
        # 3. Нажать кнопку «Войти»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_SUBMIT_BUTTON)).click()

        # 4. Проверка: ожидание редиректа и наличия User
        time.sleep(2)
        success = False
        current = dr.current_url.lower()
        if 'qa-desk.education-services.ru' in current:
            try:
                dr.find_element(By.XPATH, "//*[contains(text(), 'User')]")
                success = True
            except Exception:
                success = False

        if success:
            print('Пользователь User отображается на главной странице.')
        else:
            print('Не удалось найти имя User на странице.')

    finally:
        dr.quit()


if __name__ == '__main__':
    login()