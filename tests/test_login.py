import pytest
import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.common_locators import *
from locators.login_locators import *
from locators.registration_locators import BUTTON_CREATE_ACCOUNT, BUTTON_NO_ACCOUNT, FIELD_CONFIRM_PASSWORD


class TestLogin:
    def test_login_success(self, driver):
        random_part = ''.join(random.choices(string.digits, k=6))
        email = f"test{random_part}@test.ru"
        password = "Pass-123"

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
            EC.element_to_be_clickable(("xpath", BUTTON_LOGOUT))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_LOGIN_REGISTER))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", FIELD_EMAIL))
        ).send_keys(email)
        driver.find_element("xpath", FIELD_PASSWORD).send_keys(password)
        driver.find_element("xpath", BUTTON_LOGIN).click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", USER_AVATAR))
        )
        user_avatar = driver.find_element("xpath", USER_AVATAR)
        assert user_avatar.is_displayed(), "Аватар пользователя не отображается."

        post_ad_button = driver.find_element("xpath", BUTTON_POST_AD)
        assert post_ad_button.is_displayed(), "Кнопка 'Разместить объявление' не отображается."

        user_name = driver.find_element("xpath", USER_NAME).text
        assert user_name == "User.", f"Ожидаемое значение имени пользователя - 'User.', фактическое - '{user_name}'"

class TestLogout:
    def test_logout_success(self, driver):
        random_part = ''.join(random.choices(string.digits, k=6))
        email = f"test{random_part}@test.ru"
        password = "Pass-123"

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
            EC.element_to_be_clickable(("xpath", BUTTON_LOGOUT))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", BUTTON_LOGIN_REGISTER))
        )
        post_ad_button = driver.find_element("xpath", BUTTON_POST_AD)
        assert post_ad_button.is_displayed(), "Кнопка 'Разместить объявление' не отображается."

        login_btn = driver.find_element("xpath", BUTTON_LOGIN_REGISTER)
        assert login_btn.is_displayed(), "Кнопка 'Вход и регистрация' не отображается после выхода пользователя из аккаунта"
        assert not driver.find_elements("xpath", USER_AVATAR), "Аватар пользователя отображается после выхода пользователя из аккаунта"
        assert not driver.find_elements("xpath", USER_NAME), "Имя пользователя отображается после выхода пользователя из аккаунта"        
