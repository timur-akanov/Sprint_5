import uuid

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from credentials import EMAIL, PASSWORD, BASE_URL
from test.helpers import (
    fill_product_form,
    is_posted_ad_visible,
    login,
    open_post_ad_form,
    publish_ad,
    skip_if_empty,
)


class TestPostAd:
    def test_authorized_user_can_post_ad(self, driver):
        skip_if_empty(
            (EMAIL, PASSWORD),
            'Заполните EMAIL и PASSWORD в credentials.py',
            pytest
        )
        ad_title = f'Тестовое объявление {uuid.uuid4().hex[:8]}'

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)
        login(wait, EMAIL, PASSWORD)
        open_post_ad_form(wait)
        fill_product_form(
            driver,
            wait,
            ad_title,
            'Это тестовое описание объявления.',
            '1000'
        )
        publish_ad(wait)

        assert is_posted_ad_visible(wait, ad_title), (
            'Созданное объявление не отображается в блоке Мои объявления'
        )
