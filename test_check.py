import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    # Setup: Start the browser before each test
    driver = webdriver.Firefox()
    yield driver
    # Teardown: Close the browser after each test
    driver.quit()

def test_python_org_search(driver):
    driver.get("http://www.python.org")
    assert "Python" in driver.title

    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys("pycon")
    search_box.send_keys(Keys.RETURN)

    assert "No results found." not in driver.page_source
