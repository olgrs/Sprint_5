import pytest
import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.common_locators import *
from locators.login_locators import BUTTON_LOGOUT
from locators.registration_locators import *


class TestRegistrationSuccess:
    def test_register_new_user_success(self, driver):
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
            EC.visibility_of_element_located(("xpath", USER_AVATAR))
        )
        user_avatar = driver.find_element("xpath", USER_AVATAR)
        assert user_avatar.is_displayed(), "Аватар пользователя не отображается."

        #Сейчас не происходит редиректа на главную, поэтому тесты падают. 
        #Пользователь остается на странице https://qa-desk.education-services.ru/regiatration - баг (+опечатка).
        assert driver.current_url == "https://qa-desk.education-services.ru/", "Не произошел переход на главную страницу."

        post_ad_button = driver.find_element("xpath", BUTTON_POST_AD)
        assert post_ad_button.is_displayed(), "Кнопка 'Разместить объявление' не отображается."

        user_name = driver.find_element("xpath", USER_NAME).text
        assert user_name == "User.", f"Ожидаемое значение имени пользователя - 'User.', фактическое - '{user_name}'"


class TestRegistrationNegative:
    def test_register_invalid_email(self, driver):
        driver.get("https://qa-desk.education-services.ru/")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_LOGIN_REGISTER))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", BUTTON_NO_ACCOUNT))
        ).click()

        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", FIELD_EMAIL))
        )
        email_field.send_keys("not-email")

        driver.find_element("xpath", BUTTON_CREATE_ACCOUNT).click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", ERROR_MESSAGE_EMAIL))
        )

        error_msg = driver.find_element("xpath", ERROR_MESSAGE_EMAIL)
        assert error_msg.text == "Ошибка", f"Ожидаемое сообщение об ошибке - 'Ошибка', фактическое - '{error_msg.text}'"

        email_div = driver.find_element("xpath", f"{FIELD_EMAIL}/..")
        password_div = driver.find_element("xpath", f"{FIELD_PASSWORD}/..")
        confirm_div = driver.find_element("xpath", f"{FIELD_CONFIRM_PASSWORD}/..")

        assert ERROR_CLASS_HIGHLIGHT in email_div.get_attribute("class"), "Поле Email не подсвечено красным"
        assert ERROR_CLASS_HIGHLIGHT in password_div.get_attribute("class"), "Поле 'Пароль' не подсвечено красным"
        assert ERROR_CLASS_HIGHLIGHT in confirm_div.get_attribute("class"), "Поле 'Повторите пароль' не подсвечено красным"

    def test_register_existing_user(self, driver):
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
            EC.element_to_be_clickable(("xpath", BUTTON_NO_ACCOUNT))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", FIELD_EMAIL))
        ).send_keys(email)
        driver.find_element("xpath", FIELD_PASSWORD).send_keys(password)
        driver.find_element("xpath", FIELD_CONFIRM_PASSWORD).send_keys(password)
        driver.find_element("xpath", BUTTON_CREATE_ACCOUNT).click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(("xpath", ERROR_MESSAGE_EMAIL))
        )

        error_msg = driver.find_element("xpath", ERROR_MESSAGE_EMAIL)
        assert error_msg.text == "Ошибка", f"Ожидаемое сообщение об ошибке - 'Ошибка', фактическое - '{error_msg.text}'"

        email_div = driver.find_element("xpath", f"{FIELD_EMAIL}/..")
        password_div = driver.find_element("xpath", f"{FIELD_PASSWORD}/..")
        confirm_div = driver.find_element("xpath", f"{FIELD_CONFIRM_PASSWORD}/..")

        assert ERROR_CLASS_HIGHLIGHT in email_div.get_attribute("class"), "Поле Email не подсвечено красным"
        assert ERROR_CLASS_HIGHLIGHT in password_div.get_attribute("class"), "Поле 'Пароль' не подсвечено красным"
        assert ERROR_CLASS_HIGHLIGHT in confirm_div.get_attribute("class"), "Поле 'Повторите пароль' не подсвечено красным"