from selenium.webdriver.common.by import By
class LoginPageLocators:

    # Кнопка открытия формы (на главной странице)
    LOGIN_MAIN_BUTTON = (By.XPATH, "//button[text()='Вход и регистрация']")
    
    REG_NO_ACCOUNT = (By.XPATH, "//button[text()='Нет аккаунта']")

    EMAIL_INPUT = (By.CSS_SELECTOR, '[name="email"]')
    
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[name="password"]')

    SUBMIT_PASSWORD_BUTTON = (By.CSS_SELECTOR, '[name="submitPassword"]')
    
    # Кнопка входа на странице логина
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    
    # Кнопка выхода
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выйти')]")
    

    POST_ADD_BUTTON = (By.CSS_SELECTOR, 'button.buttonPrimary')
    
    # Модальное окно для неавторизованного пользователя
    MODAL_UNAUTHORIZED = (By.XPATH, "//div[contains(@class, 'homePage_modal')]")
    
    # Заголовок модального окна
    MODAL_TITLE_UNAUTHORIZED = (By.XPATH, "//h1[contains(text(), 'авторизуйтесь')]")

    # Разместить объявление

    MODAL_POST_ADD = (By.XPATH, "//button[contains(text(), 'Разместить объявление')]")

    PRODUCT_NAME = (By.CSS_SELECTOR, 'input[placeholder="Название"]')

    ADD_CATEGORY = (By.XPATH, "(//button[contains(@class, 'dropDownMenu_arrowDown')])[1]")


    CITY_DROPDOWN = (By.XPATH, "(//button[contains(@class, 'dropDownMenu_arrowDown')])[2]")


    PRICE_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Стоимость"]')

    PRODUCT_DESCRIPTION = (By.XPATH, "//textarea[@name='description']")
    
    # Дополнительные локаторы, используемые в тестах
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(), 'Создать аккаунт')]")
    # Альясы для согласованности: иногда в скриптах используются разные имена
    LOGIN_REG_BUTTON = (By.XPATH, "//button[text()='Вход и регистрация']")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
