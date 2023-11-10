import time
from bs4 import BeautifulSoup as bs
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

def parse_egbc_url(url): 
	# get the first url 
	url = url.split(', ')[0] 
	# split it by '/' 
	splitted_url = url.split('/') 
	# loop over the elements to find where 'cloudfront' url begins 
	for idx, part in enumerate(splitted_url): 
		if 'cloudfront' in part: 
			# add the HTTP scheme and concatenate the rest of the URL 
			# then return the processed url 
			return 'https://' + '/'.join(splitted_url[idx:]) 
	# as we don't know if that's the only measurement to take, 
	# return None if the cloudfront couldn't be found 
	return None

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
time.sleep(1)

# Pass the dialog box
acknowledge_checkbox = driver.find_element(By.ID,'acknowledgeCheckBox')
disclaimer_button = driver.find_element(By.ID,"disclaimerSubmitBtn")
ActionChains(driver).move_to_element(acknowledge_checkbox).click(acknowledge_checkbox).perform()
ActionChains(driver).move_to_element(disclaimer_button).click(disclaimer_button).perform()
time.sleep(1)


table = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table")
num_row = len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr"))
num_col = int(len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr/td"))/num_row)


# rows = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr[1]")
# altrows = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[5]/div/div")

# table = driver.find_element(By.CSS_SELECTOR,"tbody[role='rowgroup'")
# row_count = len(driver.find_elements_by_xpath("//table[@role='rowgroup']/tbody/tr"))
# column_count = len(driver.find_elements_by_xpath("//tabel[@role='rowgroup']/tbody/tr/td"))

# for index in enumerate(rows):
#     print(altrows[index[0]].text)
# 

# df = pd.read_html(table)[0]
# df.columns = ['Date','Value']

# soup = bs(table,'lxml')
# print(soup)

# print(firms)

# names = element.find_elements(By.CSS_SELECTOR,"")
#     element.find_element(By.TAG_NAME, "img").get_attribute("srcset") 
