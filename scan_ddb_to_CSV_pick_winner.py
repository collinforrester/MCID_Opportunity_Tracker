import boto3
from pprint import pprint
import csv
import json
import random

# Update the DynamoDB table information after it's created by Elastic Beanstalk
ddb_table = 'awseb-e-2zknm3vxyy-stack-MCIDIdeasTable-118YLCBRAY0E5'


# Get access credentials for Dynamo
ssmclient = boto3.client(
    'ssm',
    region_name='us-east-2'
)
ssmresponse = ssmclient.get_parameter(
    Name='DynamoDB_Reader_User_Creds',
    WithDecryption=True
)

ddb_creds = json.loads(ssmresponse['Parameter']['Value'])
ddb_access_key = ddb_creds['Access key ID']
ddb_secret_key = ddb_creds['Secret access key']


# Scan the Dynamo table
ddbclient = boto3.client(
    'dynamodb',
    aws_access_key_id=ddb_access_key,
    aws_secret_access_key=ddb_secret_key,
    region_name='us-east-2'
    )

ddbresponse = ddbclient.scan(TableName=ddb_table)


# Write output from table to CSV
if ddbresponse['Count'] > 0:

    table_header=list(ddbresponse['Items'][0].keys())

    # open a file for writing
    data = open('ddb_output.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(data)
    count = 0
    for item in ddbresponse['Items']:
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



# Select random winner
winner = random.choice(range(ddbresponse['Count']))

print('Winner is Idea #' + str(winner))
print(ddbresponse['Items'][winner]['Name']['S'])
