from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from locators import LoginPageLocators


def main():
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get('https://qa-desk.education-services.ru/')
        wait = WebDriverWait(driver, 15)

        # 1. Нажать кнопку «Разместить объявление» без авторизации
        post_button = wait.until(EC.element_to_be_clickable(LoginPageLocators.POST_ADD_BUTTON))
        post_button.click()
        time.sleep(2)
        
        # 2. Проверить, что появилось модальное окно с заголовком
        modal = wait.until(EC.visibility_of_element_located(LoginPageLocators.MODAL_UNAUTHORIZED))
        modal_title = wait.until(EC.visibility_of_element_located(LoginPageLocators.MODAL_TITLE_UNAUTHORIZED))
        
        if modal.is_displayed() and modal_title.is_displayed():
            expected_text = "Чтобы разместить объявление, авторизуйтесь"
            actual_text = modal_title.text
            if expected_text in actual_text:
                print('Модальное окно отображается с корректным заголовком:')
                print(f'  "{actual_text}"')
            else:
                print(f'Заголовок не совпадает. Ожидается: "{expected_text}", получено: "{actual_text}"')
        else:
            print('Модальное окно не отображается')
        
        time.sleep(3)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
