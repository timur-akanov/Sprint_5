from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_MAIN_BUTTON = (By.XPATH, "//button[text()='Вход и регистрация']")
    REG_NO_ACCOUNT = (By.XPATH, "//button[text()='Нет аккаунта']")

    EMAIL_INPUT = (By.CSS_SELECTOR, '[name="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[name="password"]')
    SUBMIT_PASSWORD_BUTTON = (By.CSS_SELECTOR, '[name="submitPassword"]')

    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    LOGIN_SUBMIT_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Войти')]"
    )
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выйти')]")
    LOGIN_REG_BUTTON = (By.XPATH, "//button[text()='Вход и регистрация']")

    USER_NAME = (
        By.XPATH,
        "//h3[contains(@class, 'profileText') and contains(text(), 'User')]"
    )
    USER_AVATAR = (By.CSS_SELECTOR, 'button.circleSmall')

    POST_ADD_BUTTON = (By.CSS_SELECTOR, 'button.buttonPrimary')
    MODAL_UNAUTHORIZED = (
        By.XPATH,
        "//div[contains(@class, 'homePage_modal')]"
    )
    MODAL_TITLE_UNAUTHORIZED = (
        By.XPATH,
        "//h1[contains(text(), 'авторизуйтесь')]"
    )

    MODAL_POST_ADD = (
        By.XPATH,
        "//button[contains(text(), 'Разместить объявление')]"
    )
    PRODUCT_NAME = (By.CSS_SELECTOR, 'input[placeholder="Название"]')
    PRODUCT_DESCRIPTION = (By.XPATH, "//textarea[@name='description']")
    PRICE_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Стоимость"]')

    ADD_CATEGORY = (
        By.XPATH,
        "(//button[contains(@class, 'dropDownMenu_arrowDown')])[1]"
    )
    CITY_DROPDOWN = (
        By.XPATH,
        "(//button[contains(@class, 'dropDownMenu_arrowDown')])[2]"
    )
    CONDITION_RADIO = (By.CSS_SELECTOR, 'input[name="condition"]')
    PUBLISH_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    CREATE_ACCOUNT_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Создать аккаунт')]"
    )
    MY_ADS_TITLE = (By.XPATH, "//*[contains(text(), 'Мои объявления')]")
