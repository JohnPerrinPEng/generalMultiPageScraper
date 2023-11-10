import requests
from bs4 import BeautifulSoup

# Function to scrape data from a single page
base_url = 'https://tools.egbc.ca/Registrant-Directory/Firms/SearchResult'
# num_pages = 5  # Set the total number of pages

# scrape_multiple_pages(base_url, num_pages)

response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Replace 'table_selector' with the actual CSS selector of the table
table = soup.select_one('table_selector')

if table:
    # Extract and process data from the table
    for row in table.find_all('tr'):
        for cell in row.find_all(['td', 'th']):
            print(cell.text.strip())  # Print or process the data as needed

# Function to iterate through multiple pages
def scrape_multiple_pages(base_url, num_pages):
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}?page={page_number}"
        scrape_page(url)

# Example usage
# base_url = 'https://tools.egbc.ca/Registrant-Directory/Firms/SearchResult'
# num_pages = 5  # Set the total number of pages

# scrape_multiple_pages(base_url, num_pages)