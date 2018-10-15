#!/usr/bin/env python

import boto3
from pprint import pprint
import csv
client = boto3.client(
    'dynamodb',
    aws_access_key_id="AKIAJ6CFJHUVHZL7MAOQ",
    aws_secret_access_key="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"
    )

response = client.scan(TableName='awseb-e-fawmpbasuj-stack-StartupSignupsTable-1K4YIMBV9RRMD')

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
