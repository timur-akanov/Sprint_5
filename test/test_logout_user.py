from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginPageLocators
from credentials import EMAIL, PASSWORD, BASE_URL


class TestLogoutUser:
    def test_user_can_logout(self, driver):
        assert EMAIL and PASSWORD, (
            'Заполните EMAIL и PASSWORD в credentials.py'
        )

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_MAIN_BUTTON)
        ).click()

        email_input = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(EMAIL)

        password_input = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_SUBMIT_BUTTON)
        ).click()
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGOUT_BUTTON)
        ).click()
        assert wait.until(
            EC.invisibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        assert wait.until(
            EC.invisibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )

        login_button = wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.LOGIN_REG_BUTTON
            )
        )
        assert login_button.is_displayed(), (
            'Кнопка входа не отображается после выхода'
        )
