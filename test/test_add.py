import random
import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from credentials import EMAIL, PASSWORD, BASE_URL
from locators import LoginPageLocators


class TestAddProduct:
    def test_authorized_user_can_fill_product_form(self, driver):
        assert EMAIL and PASSWORD, (
            'Заполните EMAIL и PASSWORD в credentials.py'
        )
        product_title = f'Тестовое объявление {uuid.uuid4().hex[:8]}'

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)
        scroll_script = "arguments[0].scrollIntoView({block: 'center'});"

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
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
        ).click()
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_NAME)
        )
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.USER_AVATAR)
        )

        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.MODAL_POST_ADD)
        ).click()

        product_name = wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PRODUCT_NAME)
        )
        product_name.send_keys(product_title)

        category_dropdown = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.ADD_CATEGORY)
        )
        driver.execute_script(scroll_script, category_dropdown)
        category_dropdown.click()
        category_options = self._visible_dropdown_options(driver, wait)
        category_option = random.choice(category_options)
        category_option.click()

        city_dropdown = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.CITY_DROPDOWN)
        )
        driver.execute_script(scroll_script, city_dropdown)
        city_dropdown.click()
        city_options = self._visible_dropdown_options(driver, wait)
        city_option = random.choice(city_options)
        city_option.click()

        product_description = wait.until(
            EC.visibility_of_element_located(
                LoginPageLocators.PRODUCT_DESCRIPTION
            )
        )
        product_description.send_keys('Это тестовое описание товара.')

        price_input = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.PRICE_INPUT)
        )
        price_input.send_keys('1000')

        radio_options = wait.until(self._radio_options_available)
        condition_radio = random.choice(radio_options)
        driver.execute_script("arguments[0].click();", condition_radio)
        wait.until(lambda browser: condition_radio.is_selected())

        assert product_name.get_attribute('value') == product_title
        assert price_input.get_attribute('value') == '1000'

        publish_button = wait.until(
            EC.element_to_be_clickable(LoginPageLocators.PUBLISH_BUTTON)
        )
        driver.execute_script(scroll_script, publish_button)
        publish_button.click()

        wait.until(EC.url_to_be(BASE_URL))
        wait.until(
            EC.element_to_be_clickable(LoginPageLocators.USER_AVATAR)
        ).click()
        wait.until(
            EC.visibility_of_element_located(LoginPageLocators.MY_ADS_TITLE)
        )

        created_ad = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{product_title}')]")
            ),
            'Созданное объявление не отображается в блоке Мои объявления'
        )
        assert created_ad.is_displayed(), (
            'Созданное объявление не отображается в блоке Мои объявления'
        )

    @staticmethod
    def _visible_dropdown_options(driver, wait):
        options_locator = (
            By.CSS_SELECTOR,
            "div[class^='dropDownMenu_options'] button"
        )
        return wait.until(
            lambda browser: [
                option for option in browser.find_elements(*options_locator)
                if option.is_displayed()
                and option.is_enabled()
                and option.text.strip()
            ]
        )

    @staticmethod
    def _radio_options_available(driver):
        radio_options = driver.find_elements(
            *LoginPageLocators.CONDITION_RADIO
        )
        return radio_options if radio_options else False
