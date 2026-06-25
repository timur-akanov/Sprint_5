from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD, BASE_URL


def main():
    email = EMAIL
    password = PASSWORD
    if not email or not password:
        print('Ошибка: заполните EMAIL и PASSWORD в credentials.py')
        return

    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        # Авторизуемся
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)).click()
        time.sleep(1)
        email_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        password_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_SUBMIT_BUTTON)).click()
        time.sleep(2)

        # Нажать кнопку «Выйти»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGOUT_BUTTON)).click()
        time.sleep(2)

        # Проверка: аватар и имя User больше не отображаются, кнопка входа видна
        user_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'User')]")
        try:
            login_button = driver.find_element(*LoginPageLocators.LOGIN_REG_BUTTON)
            login_button_visible = login_button.is_displayed()
        except Exception:
            login_button_visible = False

        if len(user_elements) == 0 and login_button_visible:
            print('Выход успешен: аватар User исчез и кнопка "Вход и регистрация" отображается.')
        else:
            print(f'Выход не полный: найдено User элементов {len(user_elements)}, кнопка входа видна: {login_button_visible}')

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
