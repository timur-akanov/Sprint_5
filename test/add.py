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
    wait = WebDriverWait(dr, 30)
    
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


    # Получаем триггер для выбора города (не присваиваем результат .click())
    city_trigger = wait.until(EC.element_to_be_clickable(LoginPageLocators.CITY_DROPDOWN))
    # Кликаем по триггеру после скролла ниже
    time.sleep(0.5)  # Ждем небольшую паузу

    



    # --- БЛОК ВЫБОРА СЛУЧАЙНОГО ГОРОДА (ОБНОВЛЕННЫЙ) ---
    print("Открываем выпадающий список городов...")

    # Открываем список городов
    dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_trigger)
    time.sleep(0.5)
    try:
        dr.execute_script("arguments[0].click();", city_trigger)
    except Exception:
        try:
            city_trigger.click()
        except Exception:
            pass

    # Ждём появления меню городов
    menu_locator = (By.CSS_SELECTOR, "div[class*='options'], div[class*='dropDownMenu'], div[class^='dropDownMenu_options']")
    wait.until(EC.visibility_of_element_located(menu_locator))
    time.sleep(0.5)

    # Собираем кандидатов: кнопки, li, a и любые элементы внутри меню
    candidates = []
    selectors = [
        "div[class*='options'] button",
        "div[class*='dropDownMenu'] button",
        "div[class*='dropDownMenu_options'] button",
        "div[class*='options'] li",
        "div[class*='dropDownMenu'] li",
        "div[class*='options'] a",
        "div[class*='dropDownMenu'] a",
        "div[class*='dropDownMenu_options'] li",
        "div[class*='dropDownMenu_options'] a",
    ]
    for sel in selectors:
        try:
            elems = dr.find_elements(By.CSS_SELECTOR, sel)
        except Exception:
            elems = []
        for el in elems:
            try:
                text = el.text.strip()
            except Exception:
                text = dr.execute_script("return (arguments[0].textContent||'').trim();", el)
            if text:
                candidates.append((el, text))

    # Если кандидаты не найдены, попробуем собрать любую текстовую информацию из контейнера меню
    if not candidates:
        try:
            menu = dr.find_element(*menu_locator)
            lines = dr.execute_script("return (arguments[0].innerText||'').split('\n').map(s=>s.trim()).filter(Boolean);", menu)
            for ln in lines:
                if ln:
                    # Попытка найти элемент по тексту внутри меню
                    try:
                        el = menu.find_element(By.XPATH, ".//*[normalize-space(text())='{}']".format(ln))
                        candidates.append((el, ln))
                    except Exception:
                        pass
        except Exception:
            pass

    if not candidates:
        raise Exception("Города в выпадающем меню не найдены!")

    # Выбираем случайный город из видимых кандидатов, если есть
    visible_candidates = []
    for el, text in candidates:
        try:
            if el.is_displayed() and el.is_enabled():
                visible_candidates.append((el, text))
        except Exception:
            # если is_displayed упало, всё равно добавим
            visible_candidates.append((el, text))

    if visible_candidates:
        el, city_text = random.choice(visible_candidates)
    else:
        el, city_text = random.choice(candidates)

    city_text = city_text.strip()
    print(f"Выбираем город: {city_text}")
    try:
        dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    except Exception:
        pass
    time.sleep(0.3)
    dr.execute_script("arguments[0].click();", el)
    time.sleep(0.8)












    # 13. Ввод описания товара
    product_description = wait.until(EC.visibility_of_element_located(LoginPageLocators.PRODUCT_DESCRIPTION))
    product_description.send_keys("Это тестовое описание товара. Полностью соответствует всем характеристикам.")
    

    # 14. Ввод стоимости товара
    prince_input= wait.until(EC.element_to_be_clickable(LoginPageLocators.PRICE_INPUT))
    prince_locator = (By.CSS_SELECTOR, 'input[placeholder="Стоимость"]') 
    wait.until(EC.visibility_of_element_located(prince_locator))
    prince_input.send_keys("1000")  # Ввод стоимости товара

    # 14a. Случайный выбор состояния товара (radio buttons)
    # Попытаемся найти стандартные input[type=radio]
    radios_visible = []
    try:
        radios = dr.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        radios_visible = [r for r in radios if (r.is_displayed() and r.is_enabled())]
    except Exception:
        radios_visible = []

    # Альтернативные селекторы для кастомных радио-кнопок (div/label/button с классом radio или role=radio)
    if not radios_visible:
        alt_selectors = [
            "*[role='radio']",
            "label[class*='radio']",
            "div[class*='radio']",
            "button[class*='radio']",
            "div[class*='Radio']",
            "label[class*='Radio']",
        ]
        alt_candidates = []
        for sel in alt_selectors:
            try:
                elems = dr.find_elements(By.CSS_SELECTOR, sel)
            except Exception:
                elems = []
            for el in elems:
                try:
                    if el.is_displayed() and el.is_enabled():
                        alt_candidates.append(el)
                except Exception:
                    alt_candidates.append(el)

        # Уберём дубликаты (по id или по объекту)
        radios_visible = []
        seen = set()
        for el in alt_candidates:
            key = None
            try:
                key = el.get_attribute('id') or el.get_attribute('class') or el.text
            except Exception:
                key = None
            if key in seen:
                continue
            seen.add(key)
            radios_visible.append(el)

    if radios_visible:
        chosen_radio = random.choice(radios_visible)
        try:
            dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", chosen_radio)
        except Exception:
            pass
        time.sleep(0.2)
        clicked = False
        try:
            dr.execute_script("arguments[0].click();", chosen_radio)
            clicked = True
        except Exception:
            try:
                chosen_radio.click()
                clicked = True
            except Exception:
                clicked = False

        if clicked:
            print('Случайно выбран radio-button для состояния товара')
        else:
            print('Не удалось кликнуть по radio-button для состояния товара')
    else:
        print('Радио-кнопки состояния товара не найдены')

    # 15. Открытие выпадающего меню категорий (для проверки)
    # wait.until(EC.element_to_be_clickable(LoginPageLocators.CATEGORY_DROPDOWN)).click()  

    time.sleep(5)  # Задержка для визуальной проверки результатов перед закрытием браузера

if __name__ == '__main__':
    login_and_add_product()