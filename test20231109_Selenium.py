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

# def add_values():
# table = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table")
# num_row = len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr"))
# cells = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr/td")
# num_col = int(len(cells)/num_row)

# create output filename
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M")
filename = current_datetime +" - Selenium.csv"

# format storage dataframe
outputcolumns = [ "Permit Number", "Legal Name", "Also doing business as", "Status", "Main Location"]
big_df =  pd.DataFrame(columns=outputcolumns)
# df_row = pd.Series([], dtype=str)

def scrape_page_to_df(df_columns):
    # df = pd.DataFrame(columns=df_columns)
    df = pd.DataFrame()
    # set up the lists
    unknowns = []
    permits = []
    legal_names = []
    also_knowns = []
    status = []
    locations = []

    # populate the lists
    for i, row in enumerate(driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr/td")):
        rest = i % 6
        if (rest == 0):
                unknowns.append(row.text)
        if (rest == 1):
                permits.append(row.text)
        if (rest == 2):
            legal_names.append(row.text)
        if (rest == 3):
            also_knowns.append(row.text)
        if (rest == 4):
            status.append(row.text)
        if (rest == 5):
            locations.append(row.text)

    # list into dataframe
    df = pd.DataFrame(list(zip(*[permits, legal_names, also_knowns,status,locations])),columns=df_columns)
    # df.rename(columns=df_columns)
    # df = pd.DataFrame(list(zip(*[permits, legal_names, also_knowns,status,locations]))).add_prefix('Col')
    return df

for i in range(1,60):
        time.sleep(5)
        
        df_new = scrape_page_to_df(outputcolumns)
        print(df_new)
        big_df = pd.concat([big_df,df_new])
        # print(big_df)
        # dataframe to csv
        next_page = driver.find_element(By.CLASS_NAME, "k-i-arrow-60-right")
        # next_page = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/a[3]")
        ActionChains(driver).move_to_element(next_page).click(next_page).perform()
        print("Total Records = "+str(len(big_df)))
        # big_df.to_csv(filename, index=False)

print(len(big_df))
big_df.to_csv(filename, index=False)