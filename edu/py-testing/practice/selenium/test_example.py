from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_example_domain_title(driver):
    driver.get("https://example.com")
    assert "Example Domain" in driver.title

def test_click_more_information(driver):
    driver.get("https://example.com")
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a"))
    )
    link.click()
    WebDriverWait(driver, 10).until(
        EC.title_contains("IANA")
    )
