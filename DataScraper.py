import json
import time
import re
import hashlib
import random
import string

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setting up ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


books_data = []
book_number = 1

# Mapping for rating conversion
rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}


def create_custom_id(title, timestamp):
    """
    Function to create a custom unique ID for each book using the title, timestamp, and a random string.
    """
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    unique_string = f"{title}-{timestamp}-{random_text}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def scrape_page(page_url):
    # Open the webpage
    driver.get(page_url)
    time.sleep(2)

    global book_number

    # get all elements which are articles with class - product pod
    book_elements = driver.find_elements(By.XPATH, '//article[@class="product_pod"]')

    for book in book_elements:

        title_element = book.find_element(By.XPATH, './/h3/a')
        title = title_element.get_attribute('title')

        price_numeric = 0.0
        price = book.find_element(By.XPATH, './/div[@class="product_price"]/p[@class="price_color"]').text
        match = re.search(r'[\d,\.]+', price)
        if match:
            price_numeric = float(match.group().replace(",", ""))

        rating_class = book.find_element(By.XPATH, './/p[contains(@class, "star-rating")]').get_attribute(
            'class')
        rating_text = rating_class.split()[-1]
        rating = rating_map.get(rating_text, 0)

        img_url = book.find_element(By.XPATH, './/img').get_attribute('src')

        # Get the link to the book's detail page
        detail_page_url = title_element.get_attribute('href')

        # Open the book's detail page
        driver.get(detail_page_url)
        time.sleep(2)

        description_element = driver.find_element(By.XPATH, '//meta[@name="description"]')
        description = description_element.get_attribute('content').strip()

        category = driver.find_element(By.XPATH, '//ul[@class="breadcrumb"]/li[3]/a').text

        try:
            in_stock_element = driver.find_element(By.XPATH, '//p[@class="instock availability"]')
            in_stock = in_stock_element.text.strip().split('\n')[0]
            is_in_stock = "In stock" in in_stock

            # Extract availability count using regex
            availability_count = re.search(r'\d+', in_stock)
            availability_count = availability_count.group() if availability_count else "0"
        except:
            is_in_stock = False
            availability_count = "0"

        # Generating a custom ID for the book
        timestamp = int(time.time())  # Current timestamp
        custom_id = create_custom_id(title, timestamp)

        book_number += 1

        # Collect the data in a dictionary
        book_data = {
            'id': custom_id,
            'title': title,
            'price': price_numeric,
            'rating': rating,
            'is_in_stock': is_in_stock,
            'availability_count': availability_count,
            'description': description,
            'category': category,
            'book_cover_url': img_url
        }

        books_data.append(book_data)
        # Return to the main page
        driver.back()
        time.sleep(2)


url = 'https://books.toscrape.com/catalogue/page-1.html'

try:
    while True:
        scrape_page(url)

        # Find the "Next" button
        try:
            next_button = driver.find_element(By.XPATH, '//li[@class="next"]/a')
            next_url = next_button.get_attribute('href')
            url = next_url
        except NoSuchElementException:
            # When no "Next" button is found, end the loop
            break

finally:
    # Close the WebDriver
    driver.quit()

    # Write the data to a JSON file
    with open('books_data.json', 'w') as json_file:
        json.dump(books_data, json_file, indent=4)
