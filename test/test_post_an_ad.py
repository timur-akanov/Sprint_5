from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginPageLocators
from credentials import BASE_URL


class TestPostAnAdUnauthorized:
    def test_unauthorized_user_sees_auth_modal(self, driver):
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        post_button = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.POST_ADD_BUTTON)
        )
        post_button.click()

        modal = wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.MODAL_UNAUTHORIZED
            )
        )
        modal_title = wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.MODAL_TITLE_UNAUTHORIZED
            )
        )

        assert modal.is_displayed(), (
            'Модальное окно авторизации не отображается'
        )
        assert modal_title.is_displayed(), (
            'Заголовок модального окна не отображается'
        )
        assert 'Чтобы разместить объявление, авторизуйтесь' in modal_title.text
