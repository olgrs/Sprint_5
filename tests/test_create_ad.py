import pytest
import random
import string
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.common_locators import *
from locators.registration_locators import BUTTON_CREATE_ACCOUNT, BUTTON_NO_ACCOUNT, FIELD_CONFIRM_PASSWORD
from locators.ad_locators import *


class TestCreateAdUnauthorized:
    def test_create_ad_without_auth_shows_modal(self, driver):
        driver.get("https://qa-desk.education-services.ru/")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_POST_AD))
        ).click()
        
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", MODAL_TITLE_AUTH_REQUIRED))
        )
        assert modal.is_displayed(), "Модальное окно с требованием авторизации не появилось"


class TestCreateAdAuthorized:
    def test_create_ad_success(self, driver):
        random_part = ''.join(random.choices(string.digits, k=6))
        email = f"test{random_part}@test.ru"
        password = "Pass-123"
        ad_title = f"Товар_{random_part}"
        
        driver.get("https://qa-desk.education-services.ru/")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_LOGIN_REGISTER))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_NO_ACCOUNT))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", FIELD_EMAIL))
        ).send_keys(email)
        driver.find_element("xpath", FIELD_PASSWORD).send_keys(password)
        driver.find_element("xpath", FIELD_CONFIRM_PASSWORD).send_keys(password)
        driver.find_element("xpath", BUTTON_CREATE_ACCOUNT).click()
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", USER_AVATAR))
        )

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_POST_AD))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", FIELD_NAME))
        ).send_keys(ad_title)
        
        driver.find_element("xpath", FIELD_DESCRIPTION).send_keys("Описание тестового товара")
        driver.find_element("xpath", FIELD_PRICE).send_keys("1000")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", DROPDOWN_CATEGORY))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", CATEGORY_OPTION.format("Хобби")))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(("xpath", CATEGORY_OPTION.format("Хобби")))
        )

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", DROPDOWN_CITY))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", CITY_OPTION.format("Санкт-Петербург")))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(("xpath", CITY_OPTION.format("Санкт-Петербург")))
        )

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", RADIO_CONDITION_NEW))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_PUBLISH))
        ).click()

        WebDriverWait(driver, 10, ignored_exceptions=(StaleElementReferenceException,)).until(
            lambda d: d.find_element("xpath", USER_AVATAR).click() or True
        )

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", "//h1[text()='Мой профиль']"))
        )

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", MY_ADS_BLOCK))
        )

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("xpath", "//div[@class='card']"))
        )

        ad_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(("xpath", MY_AD_HEADER.format(ad_title)))
        )
        assert ad_element.is_displayed(), f"Объявление '{ad_title}' не найдено в блоке 'Мои объявления'"
