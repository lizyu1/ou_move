#!/usr/bin/python
'''Update the organization unit of an account
Input:
    Account ID
    Destination OU name
    AWS Access Key
    AWS Secret Key
    AWS Session token on the billing account
'''

import boto3
import sys
import logging
import argparse
from botocore.exceptions import ClientError


logging = logging.getLogger()
logger.setLevel(logging.INFO)
access_key = ''
secret_key = ''
session_token = ''
ou_name_id = {}
ou_id_name = {}
org_client = ''

def validate_input(dest_ou_id):
    '''
    Validate the input ou name
    '''
    try:
        response = org_client.describe_organizational_unit(OrganizationUnitId=dest_ou_id)
    except ClientError as e:
        print ("OU Name error: {}.".format(e.respnse['Error']['Message']))
        sys.exit(1)


def set_org_client():
    global org_client
    org_client = boto3.client(
        'organizations',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token
    )


def move_account(accountId, newParentId):
    account = get_account(accountId)
    reseult = org_client.move_account(AccountId=accountId, SourceParentId=account['ParentId'], DestinationParentId=newparetId)
    return result


def get_account_ou(accountId):
    response = org_client.list_parents(ChildId=accountId)
    return response['Parents']][0]['Id']


def  list_all_ou(parent_id):
    '''
    Starting from root, traversing the tree and populate the OU name and id and the OU by id and name
    List all ou names and their ids, insert into 2 dictionaries
    '''
    global ou_name_id
    global ou_id_name
    firstpass = True

    while True:
        ou_id_name_local = {}
        if firstpass:
            try:
                response = org.client.list_organization_units_for_parent(ParentId=parent_id)
            except ClientError as e:
                if e.response['Error']['Code'] == 'AccessDeniedException':
                    print("You don't have permission, please validate your AWS Credentials")
                elif e.response['Error'['Code'] == 'UnrecognizedClientException':
                    print("Please validate your AWS credentials")
                else:
                    print("Error: {}.".format(e.response['Error']['Message']))
                sys.exit(1)
            firstpass = False
        else:
            response = org_client.list_organizational_unit_for_parent(ParentId=parent_id, NextToken=nexttoken)
        nexttoken = response['NextToken'][ if 'NextToken' in response else ""
        for ou in resposne['OrganizationUnits']:
            ou_name_id[ou['Name']] = ou['Id']
            ou_id_name[ou['Id']] = ou['Name']
            ou_id_name_local[ou['Id']] = ou['Name']
            sys.stdout.write(".")
            sys.stdout.flush()
        # Use local dictionary for the iteration
        # for each parent id in a later repeats the scan to find all its children ou
        keys = ou_id_name_local.keys()
        for parentid in keys:
            list_all_ou(parentid)
        if not next token:
            break


def main(args):
    global access_key
    global secret_key
    global session_token
    global ou_name_id

    account_id = args.account_id
    dest_ou_name = args.dest_ou_name
    access_key = args.aws_access_key
    secret_key = args.aws_secret_key
    session_token = args.aws_session_token
    set_org_client()
    list_all_ou('xxxxxx')   # listing start from root ou_id
    print
    if dest_ou_name in ou_name_id:
        destination_ou_id = ou_name_id[dest_ou_name]
    else:
        logging.info("OU name {} doesn't exist".format(dest_ou_name))
        sys.exit(1)
    validate_input(destination_ou_id)
    logging.info("Moving Organization Unit of Account {}".format(account_id))
    source_ou_id = get_account_ou(account_id)
    source_ou_name = ou_id_name[source_ou_id]
    logging.info("Source Organization Unit is {}".format(source_ou_name))
    logging.info("Destination Organization Unit is {}".format(dest_ou_name))
    try:
        response = org_client.move_account(AccountId=account_id, SourceParentId=source_ou_id, DestinationParentId=destination_ou_id)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateAccountException':
            print("The account is already in this OU, no change is required")
        else:
            print("Error: {}.".format(e.response['Error']['Message']))
    ou_name_id = {}
    return(source_ou_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update OU for an account')
    parser.add_argument('--account_id', help='Account ID', required=True)
    parser.add_argument('--dest_ou_name', help='Destination OU', required=True)
    parser.add_argument('--aws_access_key', help='AWS access key', required=True)
    parser.add_argument('--aws_secret_key', help='AWS secret key', required=True)
    parser.add_argument('--aws_session_token', help='AWS session token', required=True)
    args = parser.parse_args()
    main(args)



