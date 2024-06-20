import json
from decimal import Decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError


def create_table(dynamodb_client):
    table_name = 'NovelNexus'
    attribute_definitions = [
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
    ]
    key_schema = [
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
    ]
    provisioned_throughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
    try:
        table = dynamodb_client.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
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


def insert_data(dynamodb_resource, table_name, data):
    table = dynamodb_resource.Table(table_name)
    for item in data:
        key = {'id': item['id']}
        response = table.get_item(Key=key)
        if 'Item' not in response:
            table.put_item(Item=item)
            print(f"Inserted item with id: {item['id']}")
        else:
            print(f"Item with id: {item['id']} already exists. Skipping insertion.")
    print("Data insertion completed.")


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

    # Create table
    create_table(dynamodb_client)

    # Load data from JSON file
    with open('books_data.json') as json_file:
        data = json.load(json_file)

    # Insert data
    insert_data(dynamodb_resource, 'NovelNexus', data)

    # Query data
    query_data(dynamodb_resource, 'NovelNexus', {'id': 'cd046b3efd6f201bfaa22513d1a5fe49'})


if __name__ == "__main__":
    main()
