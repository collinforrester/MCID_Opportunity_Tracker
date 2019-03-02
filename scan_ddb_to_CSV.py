#!/usr/bin/env python

import boto3
from pprint import pprint
import csv

ssmclient = boto3.client('ssm')
ssmresponse = ssmclient.get_parameter(
    Name='DynamoDB_Reader_User_Creds',
    WithDecryption=True
)

ddb_access_key_id = ssmresponse['Parameter']['Value']

ddbclient = boto3.client(
    'dynamodb',
    aws_access_key_id="<access key>",
    aws_secret_access_key="<secret access key>",
    region_name='us-east-1'
    )

response = client.scan(TableName='<Table Name>')

if response['Count'] > 0:

    table_header=list(response['Items'][0].keys())

    # open a file for writing
    data = open('ddb_output.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(data)
    count = 0
    for item in response['Items']:
        if count == 0:
            header = table_header
            csvwriter.writerow(header)
            count += 1
        row = [item[attrib]['S'] for attrib in table_header]
        csvwriter.writerow(row)
    data.close()

    print('Success! DDB table written to ddb_output.csv')

else:
    print('Dynamo table is empty. No output written to disk.')
