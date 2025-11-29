from selenium import webdriver
import pickle
import time

driver = webdriver.Chrome()
driver.get("https://valueconn-staging.arhamsoft.org/login")  # Go to the base domain first

# Load cookies from file
with open("cookies.pkl", "rb") as file:
    cookies = pickle.load(file)

for cookie in cookies:
    driver.add_cookie(cookie)

# Now go to dashboard (should be logged in already)
driver.get("https://valueconn-staging.arhamsoft.org/dashboard/profile")
time.sleep(5)

# Do your dashboard tests here...
assert "Dashboard" in driver.title

driver.quit()
