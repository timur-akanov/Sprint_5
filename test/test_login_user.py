from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD, BASE_URL


class TestLoginUser:
    def test_user_can_login(self, driver):
        assert EMAIL and PASSWORD, (
            'Заполните EMAIL и PASSWORD в credentials.py'
        )

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)
        ).click()

        email_input = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(EMAIL)

        password_input = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.PASSWORD_INPUT)
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_SUBMIT_BUTTON)
        ).click()

        user_name = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        avatar = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )
        post_button = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.POST_ADD_BUTTON)
        )

        assert user_name.is_displayed(), 'Имя User не отображается в шапке'
        assert avatar.is_displayed(), 'Аватар пользователя не отображается'
        assert post_button.is_displayed(), (
            'Кнопка Разместить объявление не отображается'
        )
