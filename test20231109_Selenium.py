import time 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

# Define the Chrome webdriver options
options = webdriver.ChromeOptions() 
# options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

# By default, Selenium waits for all resources to download before taking actions.
# However, we don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver 
driver = Chrome(options=options) 
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

url = "https://tools.egbc.ca/Registrant-Directory/Firms/SearchResult" 
 
driver.get(url) 
time.sleep(5)


# parentWindow = driver.getWindowHandle()
# parentWindow = driver.current_window_handle
# print(parentWindow)
# windowhandles = driver.window_handles

# for winHandle in driver.windowhandles:
#     if not  winHandle == parentWindow:
#         driver.switchTo().window(winHandle)
        
acknowledge_checkbox = driver.find_element(By.ID,'acknowledgeCheckBox')
disclaimer_button = driver.find_element(By.ID,"disclaimerSubmitBtn")



# Pass the dialog box
# <input id="acknowledgeCheckBox" name="acknowledgeCheckBox" type="checkbox" value="true">
# driver.move_to_element(acknowledge_checkbox)

# ActionChains(driver).move_to_element(button).click(button).perform()
ActionChains(driver).move_to_element(acknowledge_checkbox).click(acknowledge_checkbox).perform()
ActionChains(driver).move_to_element(disclaimer_button).click(disclaimer_button).perform()
time.sleep(5)
# <input id="disclaimerSubmitBtn" type="button" class="button" value="OK">
