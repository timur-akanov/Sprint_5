from selenium import webdriver
from selenium.webdriver.common.by import By
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

        # 1. Авторизоваться под заранее созданным пользователем
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)).click()
        time.sleep(2)
        
        email_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
        email_input.send_keys(email)
        time.sleep(1)
        
        password_input = wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT))
        password_input.send_keys(password)
        time.sleep(1)
        
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_SUBMIT_BUTTON)).click()
        time.sleep(3)

        # 2. Нажать кнопку «Выйти»
        wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGOUT_BUTTON)).click()
        time.sleep(3)

        # 3. Проверить результат
        current_url = driver.current_url.lower()
        
        # Проверяем, что мы вернулись на главную страницу
        if 'qa-desk.education-services.ru' not in current_url or 'login' in current_url:
            print('Не удалось вернуться на главную страницу после выхода.')
        else:
            # Проверяем, что аватар и имя User больше не отображаются
            user_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'User')]")
            
            # Проверяем, что кнопка «Вход и регистрация» отображается
            try:
                login_button = driver.find_element(*LoginPageLocators.LOGIN_REG_BUTTON)
                login_button_visible = login_button.is_displayed()
            except Exception:
                login_button_visible = False

            if len(user_elements) == 0 and login_button_visible:
                print('Выход успешен: аватар User исчезнул и кнопка "Вход и регистрация" отображается.')
            else:
                print(f'Выход не полный: User элементов найдено {len(user_elements)}, кнопка входа видна: {login_button_visible}')

        time.sleep(3)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
