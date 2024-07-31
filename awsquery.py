import hashlib
import json
import string
import time
from decimal import Decimal
import random

from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError


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
    """ Function to insert data in DynamoDB tables """
    table = dynamodb_resource.Table(table_name)
    for item in data:
        key = {
            'id': item['id'],
            'title': item['title']
        }
        response = table.get_item(Key=key)
        # adding data if item does not already exist
        if "Item" not in response:
            category_name = item['category']
            # adding category to category table if it does not exist
            category_id = insert_category_data(dynamodb_client, dynamodb_resource, category_name)
            item['category'] = category_id
            item['price'] = Decimal(str(item['price']))
            item['availability_count'] = int(item['availability_count'])
            table.put_item(Item=item)
            print(f"Inserted item with id: {item['id']}")
        else:
            print(f"Item with id: {item['id']} already exists. Skipping insertion.")
    print("Data insertion completed.")


def insert_category_data(dynamodb_client, dynamodb_resource, category_name):
    table_name = "categories"
    # category is only added if it does not already exist in the category table
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


def query_category_data(dynamodb_client, table_name, global_category_list):
    """
        query to fetch all categories from the category table
    """
    try:
        query = f"""
            SELECT * FROM {table_name}
            """
        response = dynamodb_client.execute_statement(Statement=query)

        for item in response['Items']:
            deserialized_item = deserialize_item(item)
            global_category_list.append(deserialized_item)

    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")


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


def query_books_grouped_by_category(dynamodb_client, table_name, category_dict):
    try:
        # query to fetch all books
        query = f"""
            SELECT * FROM {table_name}
            """

        response = dynamodb_client.execute_statement(Statement=query)

        books_by_category = {}
        # traversing fetched books
        for item in response['Items']:
            deserialized_item = deserialize_item(item)
            category_id = deserialized_item['category']
            deserialized_item['category_name'] = category_dict[category_id]
            if category_id not in books_by_category:
                books_by_category[category_id] = []
            # book added to the category it belongs to
            books_by_category[category_id].append(deserialized_item)

        return books_by_category
    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")
        return None


def query_books_by_availability(dynamodb_client, table_name, max_availability_count, min_availability_count,
                                availability_count, operation):
    """
            Query to fetch books based on availability
    """
    books = []
    global query, parameters
    try:
        if operation == "<=":
            print(f"Query for availability Count <= {availability_count}")
            query = f"""
                        SELECT * FROM {table_name}
                        WHERE availability_count <= ?
                    """
            parameters = [
                {'N': str(availability_count)}
            ]
        elif operation == ">=":
            print(f"Query for availability Count >= {availability_count}")
            query = f"""
                        SELECT * FROM {table_name}
                        WHERE availability_count >= ?
                    """
            parameters = [
                {'N': str(availability_count)}
            ]
        elif operation == "[]":
            print(f"Query for availability Count between {min_availability_count} and {max_availability_count}")
            query = f"""
                        SELECT * FROM {table_name}
                        WHERE availability_count BETWEEN ? AND ?
                    """
            parameters = [
                {'N': str(min_availability_count)},
                {'N': str(max_availability_count)}
            ]
        response = dynamodb_client.execute_statement(
            Statement=query,
            Parameters=parameters
        )
        for item in response['Items']:
            deserialized_item = deserialize_item(item)
            books.append(deserialized_item)

    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")

    return books


def query_books_by_price(dynamodb_client, table_name, max_price, min_price,
                         price, operation):
    """
                Query to fetch books based on price
    """
    books = []
    global query, parameters
    try:
        if operation == "<=":
            print(f"Query for price <= {price}")
            query = f"""
                            SELECT * FROM {table_name}
                            WHERE price <= ?
                        """
            parameters = [
                {'N': str(price)}
            ]
        elif operation == ">=":
            print(f"Query for price >= {price}")
            query = f"""
                            SELECT * FROM {table_name}
                            WHERE price >= ?
                        """
            parameters = [
                {'N': str(price)}
            ]
        elif operation == "[]":
            print(f"Query for price between {min_price} and {max_price}")
            query = f"""
                            SELECT * FROM {table_name}
                            WHERE price BETWEEN ? AND ?
                        """
            parameters = [
                {'N': str(min_price)},
                {'N': str(max_price)}
            ]
        response = dynamodb_client.execute_statement(
            Statement=query,
            Parameters=parameters
        )
        for item in response['Items']:
            deserialized_item = deserialize_item(item)
            books.append(deserialized_item)

    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")

    return books


def query_books_by_rating(dynamodb_client, table_name,
                          rating, operation):
    """
                Query to fetch books based on rating
    """
    books = []
    global query, parameters
    try:
        if operation == "<=":
            print(f"Executing query for rating <= {rating}")
            query = f"""
                                SELECT * FROM {table_name}
                                WHERE rating <= ?
                            """
            parameters = [
                {'N': str(rating)}
            ]
        elif operation == ">=":
            print(f"Executing query for rating >= {rating}")
            query = f"""
                                SELECT * FROM {table_name}
                                WHERE rating >= ?
                            """
            parameters = [
                {'N': str(rating)}
            ]
        elif operation == "=":
            print(f"Executing query for rating = {rating}")
            query = f"""
                                SELECT * FROM {table_name}
                                WHERE rating = ?
                            """
            parameters = [
                {'N': str(rating)}
            ]
        response = dynamodb_client.execute_statement(
            Statement=query,
            Parameters=parameters
        )
        for item in response['Items']:
            deserialized_item = deserialize_item(item)
            books.append(deserialized_item)

    except dynamodb_client.exceptions.ClientError as e:
        print(f"An error occurred: {e}")

    return books


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
    """
        function to check if category already exists
    """
    category_name = category_name
    try:
        # query to fetch category by category name
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
