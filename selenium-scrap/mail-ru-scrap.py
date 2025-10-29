import time
from typing import Final


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import secret


def start_page_login(driver) -> None:
    '''
    стратовая страничка mail.ru имеет кнопку "Войти"
    снимаем checkbox 
    кликаем по кнопке "Войти"
    '''

    login_btn_xpath: Final[str] = '//div[@id="mailbox"]//a[text()="Войти"]'

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, login_btn_xpath)))

    login_btn = driver.find_element(By.XPATH, login_btn_xpath)

    time.sleep(3)
    login_btn.click()
    time.sleep(3)


def send_login_form(driver) -> None:
    '''
    форма логина
    заполняем логин
    снимаем галочку "save user"
    жмём кнопку "sign in"
    '''

    # сначала нужно перейти в iframe и уже потом в нём искать элементы
    iframe_path = '//iframe[starts-with(@src,"https://account.mail.ru/login")]'
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, iframe_path)))

    iframe_inp = driver.find_element(By.XPATH, iframe_path)
    driver.switch_to.frame(iframe_inp)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'email')))
    email_inp = driver.find_element(By.ID, 'email')

    # save_chk_xpath: Final[str] = '//input[@type="checkbox"][@name="save_user"]/following-sibling::div[1]//*[name()="svg"]'
    save_chk_xpath: Final[str] = '//input[@type="checkbox"][@name="save_user"]'

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, save_chk_xpath)))
    save_chk = driver.find_element(By.XPATH, save_chk_xpath)

    time.sleep(3)
    email_inp.send_keys(secret.LOGIN)

    if save_chk.is_selected():
        time.sleep(2)
        save_chk.click()

    submit_btn_path: Final[str] = '//button[@type="submit"]'
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, submit_btn_path)))
    submit_btn = driver.find_element(By.XPATH, submit_btn_path)

    time.sleep(2)
    submit_btn.click()

    driver.switch_to.default_content()

    # здесь ввод кода из sms
    # переходим на страничку other method
    other_method_btn_path: Final[str] = '//span[text()="Confirm using other method"]'
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, other_method_btn_path)))
    other_method_btn = driver.find_element(By.XPATH, other_method_btn_path)

    time.sleep(2)
    other_method_btn.click()

    time.sleep(100)


driver = webdriver.Chrome()
driver.get("https://mail.ru")

start_page_login(driver)

send_login_form(driver)

# login.send_keys('admin')
# password.send_keys('admin')


# secret.LOGIN
# secret.PASS

time.sleep(30)

driver.quit()
