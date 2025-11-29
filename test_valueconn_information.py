import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os


@pytest.fixture(scope="session")
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Optional: run without UI
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()

def test_create_information(driver):
    driver.get("https://valueconn-staging.arhamsoft.org/login")

    # Login
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email/username"]').send_keys("member@yopmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("Usa@12345")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    # Go to Profile
    driver.find_element(By.XPATH, '//a[@href="/profile"]').click()
    time.sleep(2)

    # Create Information
    driver.find_element(By.XPATH, '//a[@href="/dashboard/create"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@placeholder="Enter title"]').send_keys("title test removed content")

    # Tags input
    tag_input = driver.find_element(By.XPATH, '//input[@placeholder="Type and press enter"]')
    for tag in ["qa", "test", "sfdg", "kjh", "las"]:
        tag_input.send_keys(tag)
        tag_input.send_keys(Keys.ENTER)
        time.sleep(0.5)

    # Upload visible image
    upload_button = driver.find_element(By.XPATH, '//input[@type="file"]')
    file_path = os.path.abspath("C:/Users/ArhamSoft/Downloads/sdvhjvn.jpg")

    upload_button.send_keys(file_path)

    # Description
    desc_input = driver.find_element(By.XPATH, '//textarea[@placeholder="Write here..."]')
    long_text = "https://valueconn-staging.arhamsoft.org/login" * 7
    desc_input.clear()
    desc_input.send_keys(long_text)

    # Amount
    amount_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter amount"]')
    amount_input.send_keys("100")

    # Currency Dropdown
    currency_select = driver.find_element(By.NAME, "pricingCurrency")
    for option_value in ["USD"]:
        currency_select.send_keys(option_value)

    # Hidden Information Section
    driver.find_element(By.XPATH, '//button[contains(text(), "Hidden Information")]').click()
    time.sleep(1)

    hidden_upload = driver.find_element(By.XPATH, '//input[@type="file"]')
    file_path_2 = os.path.abspath("C:/Users/ArhamSoft/Downloads/686fd220f8d692bcfcfc1d1c_1754575057369_upperImage_cycle.png")   
    hidden_upload.send_keys(file_path_2)

    hidden_desc = driver.find_element(By.XPATH, '//textarea[@placeholder="Write here..."]')
    hidden_desc.send_keys("this is testing " * 10)
    time.sleep(4)
    # Publish
    driver.find_element(By.XPATH, '//button[contains(text(), "Publish")]').click()
    time.sleep(10)

    # Optional: Assert something happened (like success toast or redirect)

