import random  # Добавили импорт для рандома
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from credentials import EMAIL, PASSWORD
from locators import LoginPageLocators


def login_and_add_product(): 
    email = EMAIL
    password = PASSWORD
    if not email or not password:
        print('Ошибка: заполните EMAIL и PASSWORD в credentials.py')
        return

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
    
    # 4. Проверить результат: переход на главную страницу и видимость имени User
    time.sleep(2)  # Ждем, чтобы страница успела обновиться
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
    
    # 5. Открытие модалки добавления поста
    wait.until(EC.element_to_be_clickable(LoginPageLocators.MODAL_POST_ADD)).click()

    # 6. Ввод имени товара
    product_name = wait.until(EC.visibility_of_element_located(LoginPageLocators.PRODUCT_NAME))
    product_name.send_keys("Тестовый товар")

    # --- БЛОК ВЫБОРА СЛУЧАЙНОЙ КАТЕГОРИИ ---
    # 7. Открываем выпадающее меню
    dropdown_trigger = wait.until(EC.element_to_be_clickable(LoginPageLocators.ADD_CATEGORY))
    dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_trigger)
    time.sleep(0.5) # Небольшая пауза после скролла
    dropdown_trigger.click()

    # 8. Ждем появления опций (ВНИМАНИЕ: проверьте класс optionsMobile для десктопа!)
    # Замените селектор на актуальный для десктопной версии, если потребуется
    menu_locator = (By.CSS_SELECTOR, "div[class^='dropDownMenu_options']") 
    wait.until(EC.visibility_of_element_located(menu_locator))
    time.sleep(1) # Ждем завершения CSS-анимации появления меню
    
    # 9. Находим все доступные кнопки внутри меню
    buttons = dr.find_elements(By.CSS_SELECTOR, "div[class^='dropDownMenu_options'] button")
    
    if not buttons:
        raise Exception("Кнопки в выпадающем меню не найдены!")
        
    # 10. Выбираем случайную кнопку
    random_button = random.choice(buttons)
    chosen_text = dr.execute_script("return arguments[0].textContent;", random_button)
    print(f"Пытаемся выбрать категорию: {chosen_text}")
    
    # 11. Скроллим к нужной опции внутри меню (если оно со скроллом)
    dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_button)
    time.sleep(0.5) 
    
    # 12. КЛИК ЧЕРЕЗ JAVASCRIPT (Самый надежный метод для React-селектов)
    dr.execute_script("arguments[0].click();", random_button)


    city_trigger = wait.until(EC.element_to_be_clickable(LoginPageLocators.CITY_DROPDOWN)).click()
    time.sleep(2)  # Ждем появления опций города

    



    # --- БЛОК ВЫБОРА СЛУЧАЙНОГО ГОРОДА (ОБНОВЛЕННЫЙ) ---
    print("Открываем выпадающий список городов...")
    
    # 12a. Ищем ЛЮБОЙ элемент, содержащий текст "Москва", который служит триггером
    # city_trigger = wait.until(EC.element_to_be_clickable(LoginPageLocators.CITY_DROPDOWN)).click()
    dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_trigger)
    time.sleep(2)
    
    # Кликаем через JavaScript, чтобы обойти любые невидимые перекрытия
    dr.execute_script("arguments[0].click();", city_trigger)

    # 12b. Ждем, пока откроется список городов (используем универсальный поиск по классу меню)
    menu_locator = (By.CSS_SELECTOR, "div[class*='options'], div[class*='dropDownMenu']")
    wait.until(EC.visibility_of_element_located(menu_locator))
    time.sleep(0.5)
    
    # 12c. Собираем все доступные кнопки городов внутри этого меню
    city_buttons = dr.find_elements(By.CSS_SELECTOR, "div[class*='options'] button, div[class*='dropDownMenu'] button")
    if not city_buttons:
        # Альтернативный поиск, если города лежат в других тегах
        city_buttons = dr.find_elements(By.XPATH, "//div[contains(@class, 'options')]//*")
        
    if not city_buttons:
        raise Exception("Города в выпадающем меню не найдены!")
        
    # 12d. Выбираем случайный город
    random_city_button = random.choice(city_buttons)
    city_text = dr.execute_script("return arguments[0].textContent;", random_city_button)
    print(f"Выбираем город: {city_text}")
    
    # 12e. Кликаем по выбранному городу
    dr.execute_script("arguments[0].click();", random_city_button)
    time.sleep(1)












    # 13. Ввод описания товара
    product_description = wait.until(EC.visibility_of_element_located(LoginPageLocators.PRODUCT_DESCRIPTION))
    product_description.send_keys("Это тестовое описание товара. Полностью соответствует всем характеристикам.")
    

    # 14. Ввод стоимости товара
    prince_input= wait.until(EC.element_to_be_clickable(LoginPageLocators.PRICE_INPUT))
    prince_locator = (By.CSS_SELECTOR, 'input[placeholder="Стоимость"]') 
    wait.until(EC.visibility_of_element_located(prince_locator))
    prince_input.send_keys("1000")  # Ввод стоимости товара

    # 15. Открытие выпадающего меню категорий (для проверки)
    # wait.until(EC.element_to_be_clickable(LoginPageLocators.CATEGORY_DROPDOWN)).click()  

    time.sleep(5)  # Задержка для визуальной проверки результатов перед закрытием браузера

if __name__ == '__main__':
    login_and_add_product()