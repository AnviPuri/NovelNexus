import json
import boto3

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

    table = dynamodb_client.create_table(
        TableName=table_name,
        AttributeDefinitions=attribute_definitions,
        KeySchema=key_schema,
        ProvisionedThroughput=provisioned_throughput
    )

    dynamodb_client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table {table_name} created successfully.")
    return table

def insert_data(dynamodb_resource, table_name, data):
    table = dynamodb_resource.Table(table_name)
    for item in data:
        table.put_item(Item=item)
    print("Data inserted successfully.")

def query_data(dynamodb_resource, table_name, key):
    table = dynamodb_resource.Table(table_name)
    response = table.get_item(Key=key)
    item = response.get('Item')
    if item:
        print("Query succeeded:")
        print(json.dumps(item, indent=4))
    else:
        print("Item not found.")

def add_incremental_ids(data):
    for idx, item in enumerate(data, start=1):
        item['id'] = str(idx)
    return data

def main():
    region_name = 'us-west-2'
    dynamodb_resource = boto3.resource('dynamodb', region_name=region_name)
    dynamodb_client = boto3.client('dynamodb', region_name=region_name)

    # Create table
    create_table(dynamodb_client)

    # Load data from JSON file
    with open('books_data.json') as json_file:
        data = json.load(json_file)

    # Add incremental IDs
    data_with_ids = add_incremental_ids(data)

    # Insert data
    insert_data(dynamodb_resource, 'NovelNexus', data_with_ids)

    # Query data
    query_data(dynamodb_resource, 'NovelNexus', {'id': '1'})

if __name__ == "__main__":
    main()
