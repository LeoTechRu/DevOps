from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com/")
q = driver.find_element(By.ID, "searchbox_input")
q.send_keys("pytest fixtures", Keys.ENTER)

results = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']"))
)
assert len(results) > 0
driver.quit()
