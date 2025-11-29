from selenium import webdriver
import pickle
import time

driver = webdriver.Chrome()
driver.get("https://valueconn-staging.arhamsoft.org/login")

# Fill the login form
driver.find_element(By.XPATH, '//input[@placeholder="Enter your email/username"]').send_keys("seller@yopmail.com")
driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("Usa@12345")
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(5)

# Save cookies to file
with open("cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

driver.quit()
