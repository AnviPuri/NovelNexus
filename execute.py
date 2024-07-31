import json
import os

import boto3

import xml_converter
from awsquery import create_table, query_books_by_price, query_books_by_availability, \
    query_books_by_rating, query_books_grouped_by_category, query_category_data, insert_book_data
from xml_validator import validate_xml
from xsltfiles.convert import convert_xml_to_html_single_page, choose_selection, \
    convert_xml_to_html_book_category

global_category_list = []


def get_dir_path(dir_name):
    return os.path.join(os.getcwd(), rf'{dir_name}')


def execute_book_rating_operations(dynamodb_client):
    """
        function to execute operation related to book rating
    """
    global xml_file_name, page_title
    print("Choose which operation you want to carry out.")
    print("1. = for equals to")
    print("2. >= for greater than or equals to")
    print("3. <= for lesser than or equals to")
    operation = input("Enter here:")
    rating = int(input("Enter the rating:"))
    if operation == "=":
        books_by_rating_equal = query_books_by_rating(dynamodb_client, 'books', rating, "=")
        xml_output = xml_converter.convert_books_to_xml(books_by_rating_equal, global_category_list)
        with open("books_by_rating_equal.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_rating_equal.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_rating_equal.xml')
        page_title = f"Books with rating equal to {rating}"
    if operation == ">=":
        books_by_rating_greater = query_books_by_rating(dynamodb_client, 'books', rating, ">=")
        xml_output = xml_converter.convert_books_to_xml(books_by_rating_greater, global_category_list)
        with open("books_by_rating_greater.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_rating_greater.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_rating_greater.xml')
        page_title = f"Books with rating greater than {rating}"
    if operation == "<=":
        books_by_rating_lesser = query_books_by_rating(dynamodb_client, 'books', rating, "<=")
        xml_output = xml_converter.convert_books_to_xml(books_by_rating_lesser, global_category_list)
        with open("books_by_rating_lesser.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_rating_lesser.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_rating_lesser.xml')
        page_title = f"Books with rating less than {rating}"
    choose_selection(xml_file_name, page_title)


def execute_book_availability_operations(dynamodb_client):
    """
            function to execute operation related to book availability
    """
    global xml_file_name, page_title
    print("Choose which operation you want to carry out.")
    print("1. [] for between")
    print("2. >= for greater than or equals to")
    print("3. <= for lesser than or equals to")
    operation = input("Enter here:")
    if operation == "[]":
        max_availability_count = int(input("Enter the maximum availability count:"))
        min_availability_count = int(input("Enter the minimum availability count:"))
        books_by_availability_between = query_books_by_availability(dynamodb_client, 'books', max_availability_count,
                                                                    min_availability_count, 0, "[]")
        xml_output = xml_converter.convert_books_to_xml(books_by_availability_between, global_category_list)
        with open("books_by_availability_between.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_availability_between.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_availability_between.xml')
        page_title = f"Books with availability between {min_availability_count} and {max_availability_count}"
    if operation == ">=":
        availability_count = int(input("Enter the availability count:"))
        books_by_availability_greater = query_books_by_availability(dynamodb_client, 'books', 0, 0, availability_count,
                                                                    ">=")
        xml_output = xml_converter.convert_books_to_xml(books_by_availability_greater, global_category_list)
        with open("books_by_availability_greater.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_availability_greater.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_availability_greater.xml')
        page_title = f"Books with availability greater than {availability_count}"
    if operation == "<=":
        availability_count = int(input("Enter the availability count:"))
        books_by_availability_lesser = query_books_by_availability(dynamodb_client, 'books', 0, 0, availability_count,
                                                                   "<=")
        xml_output = xml_converter.convert_books_to_xml(books_by_availability_lesser, global_category_list)
        with open("books_by_availability_lesser.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_availability_lesser.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_availability_lesser.xml')
        page_title = f"Books with availability less than {availability_count}"
    choose_selection(xml_file_name, page_title)


def execute_book_price_operations(dynamodb_client):
    """
                function to execute operation related to book price
    """
    global xml_file_name, page_title
    print("Choose which operation you want to carry out.")
    print("1. [] for between")
    print("2. >= for greater than or equals to")
    print("3. <= for lesser than or equals to")
    operation = input("Enter here:")
    if operation == "[]":
        max_price = float(input("Enter the maximum price:"))
        min_price = float(input("Enter the minimum price:"))
        books_by_price_between = query_books_by_price(dynamodb_client, 'books', max_price, min_price, 0, "[]")
        xml_output = xml_converter.convert_books_to_xml(books_by_price_between, global_category_list)
        with open("books_by_price_between.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_price_between.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_price_between.xml')
        page_title = f"Books with price between {min_price} and {max_price}"
    if operation == ">=":
        price = float(input("Enter the price:"))
        books_by_price_greater = query_books_by_price(dynamodb_client, 'books', 0, 0, price, ">=")
        xml_output = xml_converter.convert_books_to_xml(books_by_price_greater, global_category_list)
        with open("books_by_price_greater.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_price_greater.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_price_greater.xml')
        page_title = f"Books with price greater than {price}"
    if operation == "<=":
        price = float(input("Enter the price:"))
        books_by_price_lesser = query_books_by_price(dynamodb_client, 'books', 0, 0, price, "<=")
        xml_output = xml_converter.convert_books_to_xml(books_by_price_lesser, global_category_list)
        with open("books_by_price_lesser.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_price_lesser.xml', 'library.xsd')
        xml_file_name = get_dir_path('books_by_price_lesser.xml')
        page_title = f"Books with price less than {price}"
    choose_selection(xml_file_name, page_title)


def execute_books_by_category_operations(dynamodb_client):
    """
                function to execute operation related to books by category
    """
    category_dict = {item['id']: item['category_name'] for item in global_category_list}
    books_grouped_by_category = query_books_grouped_by_category(dynamodb_client, 'books', category_dict)
    if books_grouped_by_category:
        xml_output = xml_converter.convert_books_to_xml_by_category(books_grouped_by_category)
        with open("books_by_category.xml", "w") as xml_file:
            xml_file.write(xml_output)
        validate_xml('books_by_category.xml', 'book_by_category.xsd')
        xml_file_name = get_dir_path('books_by_category.xml')
        convert_xml_to_html_book_category(get_dir_path('output2_html'), xml_file_name, get_dir_path('xsltfiles/books_by_category.xslt'))
    else:
        print("No items found.")


def main():
    # Load AWS credentials from the configuration file
    with open('aws_config.json') as config_file:
        config = json.load(config_file)

    aws_access_key_id = config['aws_access_key_id']
    aws_secret_access_key = config['aws_secret_access_key']
    region_name = config['region_name']

    dynamodb_resource = boto3.resource(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    dynamodb_client = boto3.client(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Create books table
    create_table(
        dynamodb_client,
        'books',
        [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        [
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ]
    )

    # Create categories table
    create_table(
        dynamodb_client,
        'categories',
        [
            {'AttributeName': 'id', 'KeyType': 'HASH'}  # Partition key
        ],
        [
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ]
    )

    # Load data from JSON file
    with open('books_data.json') as json_file:
        data = json.load(json_file)

    # Insert data
    insert_book_data(dynamodb_client, dynamodb_resource, 'books', data)

    # queries the category data and stores it in global_category_list
    query_category_data(dynamodb_client, 'categories', global_category_list)

    print("Choose which function to perform:")
    print("Select A to fetch books based on rating.")
    print("Select B to fetch books based on availability count.")
    print("Select C to fetch books based on price.")
    print("Select D to fetch books grouped by category.")
    print("Select any other key to Exit.")
    selection = input("Enter here:").upper()

    if selection == "A":
        execute_book_rating_operations(dynamodb_client)
    elif selection == "B":
        execute_book_availability_operations(dynamodb_client)
    elif selection == "C":
        execute_book_price_operations(dynamodb_client)
    elif selection == "D":
        execute_books_by_category_operations(dynamodb_client)
    else:
        print('Exiting...')


if __name__ == "__main__":
    main()
