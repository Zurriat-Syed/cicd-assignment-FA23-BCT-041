import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

BASE_URL = os.environ.get("BASE_URL", "http://localhost")
RESULTS_DIR = os.environ.get("RESULTS_DIR", "results")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    drv.get(BASE_URL)
    yield drv
    drv.quit()


def test_title(driver):
    assert driver.title == "CI/CD Pipeline Assignment - FA23-BCT-041"


def test_heading_shows_name_and_roll(driver):
    heading = driver.find_element(By.ID, "heading").text
    assert heading == "CI/CD Pipeline Assignment"
    assert driver.find_element(By.ID, "name").text == "Syed Zurriat Hussain"
    assert driver.find_element(By.ID, "roll").text == "FA23-BCT-041"


def test_button_click_shows_message(driver):
    assert driver.find_element(By.ID, "message").text == ""
    driver.find_element(By.ID, "msg-btn").click()
    assert driver.find_element(By.ID, "message").text == "Button clicked successfully!"


def test_text_box_submit_displays_text(driver):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    driver.find_element(By.ID, "text-input").send_keys("Hello from Selenium")
    driver.find_element(By.ID, "submit-btn").click()
    assert driver.find_element(By.ID, "output").text == "You entered: Hello from Selenium"
    driver.save_screenshot(os.path.join(RESULTS_DIR, "test_site.png"))


def test_empty_submit_shows_empty_value(driver):
    driver.find_element(By.ID, "submit-btn").click()
    assert driver.find_element(By.ID, "output").text == "You entered:"
