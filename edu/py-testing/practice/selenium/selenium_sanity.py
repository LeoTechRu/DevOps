from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")      # без окна
opts.add_argument("--window-size=1920,1080")
# На Windows иногда помогает ↓ (если корпоративные политики/антивирус мешают)
# opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)
driver.get("https://example.com")
print("TITLE:", driver.title)
driver.quit()