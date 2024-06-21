import json
from decimal import Decimal, getcontext, Context
from random import random
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError

import boto3
import json
import time
import re
import hashlib
import random
import string


def create_custom_id(title, timestamp):
    """
    Function to create a custom unique ID for each book using the title, timestamp, and a random string.
    """
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    unique_string = f"{title}-{timestamp}-{random_text}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def create_table(dynamodb_client, table_name, key_schema, attribute_definitions):
    """ Function to create DynamoDB table """
    try:
        table = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        dynamodb_client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully.")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")
            return dynamodb_client.describe_table(TableName=table_name)['Table']
        else:
            raise e


def insert_book_data(dynamodb_client, dynamodb_resource, table_name, data):
    table = dynamodb_resource.Table(table_name)
    for item in data:
        key = {
            'id': item['id'],
            'title': item['title']
        }
        response = table.get_item(Key=key)
        if "Item" not in response:
            category_name = item['category']
            category_id = insert_category_data(dynamodb_client, dynamodb_resource, category_name)
            item['category'] = category_id
            item['price'] = Decimal(str(item['price']))
            table.put_item(Item=item)
            print(f"Inserted item with id: {item['id']}")
        else:
            print(f"Item with id: {item['id']} already exists. Skipping insertion.")
    print("Data insertion completed.")


def insert_category_data(dynamodb_client, dynamodb_resource, category_name):
    table_name = "categories"
    if not does_category_exist(dynamodb_client, table_name, category_name):
        category_id = None
        timestamp = int(time.time())

        table = dynamodb_resource.Table(table_name)

        category_id = create_custom_id(category_name, timestamp)
        item = {
            'id': category_id,
            'category_name': category_name
        }
        table.put_item(Item=item)
        print(f"Inserted item with id: {item['id']}")
        return category_id
    else:
        return query_category_by_name(dynamodb_client, 'categories', category_name)


def query_data(dynamodb_resource, table_name, key):
    table = dynamodb_resource.Table(table_name)
    response = table.get_item(Key=key)
    item = response.get('Item')
    if item:
        print("Query succeeded:")
        deserialized_item = deserialize_item(item)
        print(json.dumps(deserialized_item, indent=4))
    else:
        print("Item not found.")


def query_sorted_data(dynamodb_client, table_name):
    try:
        query = f"""
            SELECT * FROM {table_name}
            WHERE price>30
            """

        response = dynamodb_client.execute_statement(Statement=query)

        for item in response['Items']:
            print(item)
    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")


def query_category_by_name(dynamodb_client, table_name, category_name):
    category_name = category_name
    try:
        query = f"""
                    SELECT * FROM {table_name}
                    WHERE category_name = ?
                """

        # Execute the PartiQL query with parameterized expression
        response = dynamodb_client.execute_statement(
            Statement=query,
            Parameters=[
                {'S': category_name}  # Pass category_name directly as a string ('S' type)
            ]
        )

        # Check if there are any matching items
        items = response['Items']
        if items:
            category_id = items[0]['id']['S']
            print(f"Category '{category_name}' exists with ID: {category_id}")
            return category_id
        else:
            print(f"Category '{category_name}' does not exist.")
            return None

    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")
        return None


def does_category_exist(dynamodb_client, table_name, category_name):
    category_name = category_name
    try:
        query = f"""
            SELECT * FROM {table_name}
            WHERE category_name = ?
        """

        # Execute the PartiQL query with parameterized expression
        response = dynamodb_client.execute_statement(
            Statement=query,
            Parameters=[
                {'S': category_name}  # Pass category_name directly as a string ('S' type)
            ]
        )

        # Check if there are any matching items
        items = response['Items']
        if items:
            print(f"Category '{category_name}' exists.")
            return True
        else:
            print(f"Category '{category_name}' does not exist.")
            return False

    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")
        return False


def deserialize_item(item):
    deserializer = TypeDeserializer()
    deserialized_item = {}
    for key, value in item.items():
        if isinstance(value, Decimal):
            deserialized_item[key] = str(value)  # Convert Decimal to string for JSON serialization
        elif isinstance(value, bool):
            deserialized_item[key] = value  # Handle boolean values directly
        elif isinstance(value, (dict, list)):
            deserialized_item[key] = deserializer.deserialize(value)
        else:
            deserialized_item[key] = value  # Fallback to the original value if not deserializable
    return deserialized_item


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

    # Query data
    query_data(dynamodb_resource, 'books', {'id': '4eb5a11d3cb71f5bec815c5b950bc2d8', 'title' : 'Tipping the '
                                                                                                     'Velvet'})
    query_sorted_data(dynamodb_client, 'books')


if __name__ == "__main__":
    main()
