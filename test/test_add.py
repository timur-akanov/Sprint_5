import uuid

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from credentials import EMAIL, PASSWORD, BASE_URL
from test.helpers import (
    fill_product_form,
    is_user_authorized,
    login,
    open_post_ad_form,
    skip_if_empty,
)


class TestAddProduct:
    def test_authorized_user_can_fill_product_form(self, driver):
        skip_if_empty(
            (EMAIL, PASSWORD),
            'Заполните EMAIL и PASSWORD в credentials.py',
            pytest
        )
        product_title = f'Тестовое объявление {uuid.uuid4().hex[:8]}'

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)
        login(wait, EMAIL, PASSWORD)
        is_user_authorized(wait)
        open_post_ad_form(wait)
        product_name, price_input, condition_radio = fill_product_form(
            driver,
            wait,
            product_title,
            'Это тестовое описание товара.',
            '1000'
        )

        actual_product_name = product_name.get_attribute('value')
        actual_price = price_input.get_attribute('value')
        is_condition_selected = condition_radio.is_selected()

        assert (
            actual_product_name == product_title
            and actual_price == '1000'
            and is_condition_selected
        )
