from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://arimadata.com/account")

# Find the input field and type "user"
time.sleep(2)
input_field = driver.find_element(By.ID, "outlined-email")
time.sleep(2)
input_field.send_keys("user")
time.sleep(2)

elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Log In')]")

if elements:
    print("hello")

driver.close()
driver.quit()