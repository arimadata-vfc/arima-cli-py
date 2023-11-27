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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

load_dotenv()
ARIMA_USER = os.getenv("ARIMA_USER")
ARIMA_PASS = os.getenv("ARIMA_PASS")

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("user-data-dir=selenium")
# chrome_options.add_argument("--headless")

prefs = {"download.default_directory" : "C:\\Users\\MSadm\\Documents\\Sadman\\code\\arima\\arima-cli\\data"}
chrome_options.add_experimental_option("prefs",prefs)
print("Setup options")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get("https://arimadata.com/account")

time.sleep(1)

wait = WebDriverWait(driver, 180)

if driver.current_url == "https://arimadata.com/account":
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

        print("Clicked login button")

time.sleep(1)

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
print("4")

click_with_custom_wait(driver, wait, "//div[contains(text(), 'General')]")
print("5")

general_audience = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'General')]")))
general_audience.click()
print("5")

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

def get_theme_or_cat(driver, wait, theme_name):
    theme_found = False
    while not theme_found:
        try:
            theme = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@class, 'MuiGrid-container') and contains(@class, 'MuiGrid-wrap-xs-nowrap') and contains(@class, 'css-7ftst8')]//p[contains(text(), '" + theme_name + "')]")))
            theme.click()
            theme_found = True
        except StaleElementReferenceException:
            continue

# get_theme_or_cat(driver, wait, "Demography")
# print("7")

# get_theme_or_cat(driver, wait, "Household Status")
# print("8")

def build_var_lists(driver, base_xpath, vars, start, initial = True):
    if initial:
        try:
            element = driver.find_element(By.XPATH, f"{base_xpath}")
            if element.text != "":
                vars.append(element.text)
        except NoSuchElementException:
            pass

    i = start
    invalid_count = 0
    while True:
        try:
            element = driver.find_element(By.XPATH, f"{base_xpath}[{i}]")
            if element.text != "":
                vars.append(element.text)
        except NoSuchElementException:
            invalid_count += 1
            if invalid_count > 10:
                return None
            continue
        i += 1

themes = []
build_var_lists(driver, "//div[1]/div/div", themes, start = 3, initial = False)
print("themes = ", themes)

time.sleep(10)

for theme in themes:
    print("theme = ", theme)
    get_theme_or_cat(driver, wait, theme)
    categories = []
    build_var_lists(driver, "//div[2]/div[2]/div", themes, start = 1)
    print("categories = ", themes)

time.sleep(10)

from selenium.webdriver.common.by import By

def find_nth_child_with_text(driver, base_selector, text):
    i = 1
    while True:
        try:
            element = driver.find_element(By.CSS_SELECTOR, f"{base_selector}:nth-child({i})")
            print("i = ", i)
            print("element.text = ", element.text)
            if text in element.text:
                return element
        except:
            return None
        i += 1

def click_nth_child_with_text(driver, base_selector, text):
    element = find_nth_child_with_text(driver, base_selector, text)
    if element is not None:
        print("Element found: ", text)
        element.click()
    else:
        print("Element not found")

click_nth_child_with_text(driver, ".css-wo8ext", "Head of Household")

click_nth_child_with_text(driver, ".css-wo8ext", "Grandparent")

print("BOTH CHECKBOXES CLICKED")
time.sleep(3)

analyze_button = driver.find_element(By.CSS_SELECTOR, ".MuiButton-contained")
analyze_button.click()
print("11")
print("CLICKED ANALYZE BUTTON")
time.sleep(3)

try:
    WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Please wait while we compile your audience')]")))
except TimeoutException:
    print("Timed out waiting for 'Please wait' text to disappear")

import datetime

# check if `data/Demographic_Deep_Dive_All_Tables.csv` exists
# if it does, append current timestamp to end of filename
old_file_name = "data/Demographic_Deep_Dive_All_Tables.csv"
timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
new_file_name = "data/Demographic_Deep_Dive_All_Tables_" + timestamp + ".csv"

if os.path.exists(old_file_name):
    os.rename(old_file_name, new_file_name)
else:
    print(f"{old_file_name} not found.")

extract_all_tables = driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .MuiButton-root")
extract_all_tables.click()
print("CLICKED EXPORT BUTTON")

extract_all_tables = driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root > a")
extract_all_tables.click()
print("CLICKED DOWNLOAD BUTTON")

old_file_name = "data/Demographic_Deep_Dive_All_Tables.csv"

timestamp = datetime.datetime.now().strftime("%Y\_%m\_%d-%H\_%M\_%S")
new_file_name = f"data/data_{timestamp}.csv"

if os.path.exists(old_file_name):
    os.rename(old_file_name, new_file_name)
else:
    print(f"{old_file_name} not found.")

time.sleep(1)

# click on edit table variables
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-outlined")))

driver.execute_script("arguments[0].click();", button)

# button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-outlined")))
# button.click()

# button = driver.find_element(By.CSS_SELECTOR, ".MuiButton-outlined")
# button.click()

# wait to go back to variable selection screen
try:
    WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Please wait while we compile your audience')]")))
except TimeoutException:
    print("Timed out waiting for 'Please wait' text to disappear")

time.sleep(1)

from selenium.common.exceptions import NoSuchElementException

def find_div_with_text(driver, base_xpath, text):
    try:
        element = driver.find_element(By.XPATH, f"{base_xpath}")
        print("0 ", element.text)
        if text in element.text:
            return element
    except NoSuchElementException:
        pass

    i = 2
    while True:
        try:
            element = driver.find_element(By.XPATH, f"{base_xpath}[{i}]")
            print(i, " ", element.text)
            if text in element.text:
                return element
        except NoSuchElementException:
            return None
        i += 1

def click_div_with_text(driver, base_xpath, text):
    element = find_div_with_text(driver, "//div[3]/div[3]/div", text)
    if element is not None:
        print("Element found: ", text)
        element.click()
    else:
        print("Element not found")

print("preclick")
click_div_with_text(driver, "//div[3]/div[3]/div", "Grandparent")
click_div_with_text(driver, "//div[3]/div[3]/div", "Head of Household")

time.sleep(30)

driver.close()
driver.quit()

# <a download="Demographic_Deep_Dive_All_Tables.csv" target="_self" href="blob:" style="color: inherit; text-decoration: none;">Extract All Tables to CSV</a>