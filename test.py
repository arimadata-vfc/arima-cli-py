from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
from dotenv import load_dotenv
import os
import requests
import pickle
import os
from selenium.common.exceptions import StaleElementReferenceException

load_dotenv()
ARIMA_USER = os.getenv("ARIMA_USER")
ARIMA_PASS = os.getenv("ARIMA_PASS")

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_argument("--headless")
print("a1")

prefs = {"download.default_directory" : "C:\\Users\\MSadm\\Documents\\Sadman\\code\\arima\\arima-cli"}
chrome_options.add_experimental_option("prefs",prefs)
print("a2")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
print("a2")
driver.get("https://arimadata.com/account")
print("a3")

cookies_file = "cookies.pkl"
if os.path.isfile(cookies_file):
    cookies = pickle.load(open(cookies_file, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
else:
    print("Cookies file not found.")

# Wait until "Log In" text is found
wait = WebDriverWait(driver, 180)
login_found = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'Log In')]")))

if login_found:
    print("Login screen found")
    # Find the input field and type "user"
    input_field = driver.find_element(By.ID, "outlined-email")
    input_field.send_keys(ARIMA_USER)

    # Find the password field and type "password"
    password_field = driver.find_element(By.ID, "outlined-password")
    password_field.send_keys(ARIMA_PASS)

    # Find the login button and click it
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    login_button.click()
print("2")

# After logging in, save the cookies to a file
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

time.sleep(2)

# Find the Dashboard button and click it
# dashboard_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Dashboard')]")
# dashboard_button.click()
print("3")

driver.get("https://arimadata.com/dashboard/module")

def click_with_custom_wait(driver, wait, xpath):
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()
            print("Clicked on element with XPath:", xpath)
            break
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:  # Re-raise the last exception if max attempts reached
                raise
            continue

# Wait for "Persona Builder" to show up and then click on it
click_with_custom_wait(driver, wait, "//div[contains(text(), 'Persona Builder')]")
# persona_builder = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Persona Builder')]")))
# persona_builder.click()
print("4")

click_with_custom_wait(driver, wait, "//div[contains(text(), 'General')]")
print("5")

# general_audience = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'General')]")))
# general_audience.click()
# print("5")

select_audience = driver.find_element(By.XPATH, "//button[contains(text(), 'Select Audience')]")
select_audience.click()
print("6")

audience_crosstab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Audience Crosstab')]")))
audience_crosstab.click()
print("1")

try:
    WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Please wait while we compile your audience')]")))
except TimeoutException:
    print("Timed out waiting for 'Please wait' text to disappear")

# TEST
element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@class, 'MuiGrid-container') and contains(@class, 'MuiGrid-wrap-xs-nowrap') and contains(@class, 'css-7ftst8')]//p[contains(text(), 'Demography')]")))
element.click()
print("7")

element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@class, 'MuiGrid-container') and contains(@class, 'MuiGrid-wrap-xs-nowrap') and contains(@class, 'css-7ftst8')]//p[contains(text(), 'Household Status')]")))
element.click()
print("8")

# element = driver.find_element(By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@class, 'css-wo8ext')]//p[contains(text(), 'Head of Household')]")
# driver.execute_script("arguments[0].click();", element)
element = driver.find_element(By.CSS_SELECTOR, ".css-wo8ext:nth-child(2)")
element.click()
print("9")

time.sleep(3)

# grandparent_checkbox = driver.find_element(By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@class, 'css-wo8ext')]//p[contains(text(), 'Grandparent')]")
# driver.execute_script("arguments[0].click();", grandparent_checkbox)
grandparent_checkbox = driver.find_element(By.CSS_SELECTOR, ".css-wo8ext:nth-child(3)")
grandparent_checkbox.click()
print("14")
print("BOTH CHECKBOXES CLICKED")
time.sleep(3)

analyze_button = driver.find_element(By.CSS_SELECTOR, ".MuiButton-contained")
analyze_button.click()
# driver.execute_script("arguments[0].click();", d)
print("11")
print("CLICKED ANALYZE BUTTON")
time.sleep(3)

try:
    WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Please wait while we compile your audience')]")))
except TimeoutException:
    print("Timed out waiting for 'Please wait' text to disappear")

time.sleep(3)

# Find and click on the element
# target_element = driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .MuiButton-root")
# target_element = driver.find_element(By.CSS_SELECTOR, ".MuiButton-contained")
# target_element.click()

# export_button = driver.find_element(By.XPATH, "//button[contains(@class, 'MuiButton-root') and contains(@class, 'MuiButton-text') and contains(@class, 'MuiButton-textPrimary') and contains(@class, 'MuiButton-sizeMedium') and contains(@class, 'MuiButton-textSizeMedium') and contains(@class, 'MuiButtonBase-root') and contains(@class, 'css-tflhij')]")
# export_button.click()
print("15")

time.sleep(3)

# extract_all_tables = driver.find_element(By.XPATH, "//button[contains(text(),'Export')]")
extract_all_tables = driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .MuiButton-root")
extract_all_tables.click()
print("13")
print("CLICKED EXPORT BUTTON")

time.sleep(3)

# extract_all_tables = driver.find_element(By.XPATH, "//a[contains(text(),'Extract All Tables to CSV')]")
extract_all_tables = driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root > a")
extract_all_tables.click()
print("CLICKED DOWNLOAD BUTTON")

print("130")

# export_button = driver.find_element(By.XPATH, "//button[contains(@class, 'MuiButton-root') and contains(@class, 'MuiButton-text') and contains(@class, 'MuiButton-textPrimary') and contains(@class, 'MuiButton-sizeMedium') and contains(@class, 'MuiButton-textSizeMedium') and contains(@class, 'MuiButtonBase-root') and contains(@class, 'css-tflhij')]")
# export_button.click()
# print("15")

# # Find and click on the element
# extract_all_tables = driver.find_element(By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(@class, 'MuiMenuItem-gutters') and contains(@class, 'MuiButtonBase-root') and contains(@class, 'css-7w1seg')]//a[contains(text(), 'Extract All Tables to CSV')]")
# # extract_all_tables.click()
# driver.execute_script("arguments[0].click();", extract_all_tables)
# print("13")

time.sleep(2)

# driver_cookies = driver.get_cookies()
# cookies_copy = {}
# for driver_cookie in driver_cookies:
#     cookies_copy[driver_cookie["name"]] = driver_cookie["value"]
# r = requests.get('url',cookies = cookies_copy)
# print r.text

driver.close()
driver.quit()

# <a download="Demographic_Deep_Dive_All_Tables.csv" target="_self" href="blob:" style="color: inherit; text-decoration: none;">Extract All Tables to CSV</a>