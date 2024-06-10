import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Automatically download and set up the ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
books_data = []
book_number = 1
try:

    #instead of having range use next to get the page of the next page if next is not available then stop the loop
    for i in range(1,51):
        # Open the webpage
        url = f'https://books.toscrape.com/catalogue/page-{i}.html'
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Scrape book titles and prices
        # get all which are articles with class product pod
        book_elements = driver.find_elements(By.XPATH, '//article[@class="product_pod"]')

        for book in book_elements:
            title_element = book.find_element(By.XPATH, './/h3/a')
            title = title_element.get_attribute('title')
            price = book.find_element(By.XPATH, './/div[@class="product_price"]/p[@class="price_color"]').text
            rating_class = book.find_element(By.XPATH, './/p[contains(@class, "star-rating")]').get_attribute('class')
            rating = rating_class.split()[-1]  # Get the last class name which represents the rating
            # In-stock availability is represented by the presence of "In stock" text
            instock = book.find_element(By.XPATH, './/p[@class="instock availability"]').text.strip()

            # Get the link to the book's detail page
            detail_page_url = title_element.get_attribute('href')

            # Open the book's detail page
            driver.get(detail_page_url)

            # Wait for the detail page to load
            time.sleep(2)

            # Scrape the book description
            description_element = driver.find_element(By.XPATH, '//meta[@name="description"]')
            description = description_element.get_attribute('content').strip()

            category = driver.find_element(By.XPATH, '//ul[@class="breadcrumb"]/li[3]/a').text

            print(f'Details for Book {book_number}')
            print(f'Title: {title}')
            print(f'Price: {price}')
            print(f'Rating: {rating}')
            print(f'In stock: {instock}')
            print(f'Description: {description}')
            print(f'Category: {category}')
            book_number += 1

            # Collect the data in a dictionary
            book_data = {
                'title': title,
                'price': price,
                'rating': rating,
                'in_stock': instock,
                'description': description,
                'category': category
            }

            # Add the dictionary to the list
            books_data.append(book_data)
            # Return to the main page
            driver.back()

            # Wait for the main page to load
            time.sleep(2)
finally:
    # Close the WebDriver
    driver.quit()
    with open('books_data.json', 'w') as json_file:
        json.dump(books_data, json_file, indent=4)
