import time
from datetime import datetime
from csv import writer
from bs4 import BeautifulSoup as bs
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
time.sleep(1)

# Pass the dialog box
acknowledge_checkbox = driver.find_element(By.ID,'acknowledgeCheckBox')
disclaimer_button = driver.find_element(By.ID,"disclaimerSubmitBtn")
ActionChains(driver).move_to_element(acknowledge_checkbox).click(acknowledge_checkbox).perform()
ActionChains(driver).move_to_element(disclaimer_button).click(disclaimer_button).perform()
time.sleep(1)

def add_values():
    table = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table")
    num_row = len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr"))
    cells = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr/td")
    num_col = int(len(cells)/num_row)

    # create output file
    outputcolumns = ["Unknown", "Permit Number", "Legal Name", "Also doing business as", "Status", "Main Location"]
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M")
    filename = current_datetime +" - Selenium.csv"

    with open(filename,'w',newline='') as f:
        csv_writer = writer(f)
        for i in range(0, num_row, 6):
            out_row = []
            for j in range(1,6):
                value = cells[i+j].text
                out_row.append(value)
                # print(out_row)
            csv_writer.writerow(out_row)

time.sleep(5)

next_page = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/a[3]")
ActionChains(driver).move_to_element(next_page).click(next_page).perform()


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
